# Import statements (some used for google sheets API)

from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import time

# Constant variables used to represent cut off for service size categorisation 

MICRO = 50000
SMALL = 250000
MEDIUM = 1000000
LARGE = 5000000

# Class object used to group data related to the same month 
# This stores transaction volumes for each serive size classification for each month

class MonthlySizeCount:
    def __init__(self):
        self.micro = 0 
        self.small = 0
        self.medium = 0
        self.large = 0
        self.xl = 0

# This function passes in SMS Values and returns SMS sizes (one of five categories)
# Integer is passed in & a string is returned 

def determine_SMS_Size(SMSVal):
    if SMSVal < MICRO:
        return "MICRO"
    elif SMSVal >= MICRO and SMSVal < SMALL:
        return "SMALL"
    elif SMSVal >= SMALL and SMSVal < MEDIUM:
        return "MEDIUM"
    elif SMSVal >= MEDIUM and SMSVal < LARGE:
        return "LARGE"
    elif SMSVal >= LARGE:
        return "EXTRA LARGE"

# The rest of this file is adapted from this: https://developers.google.com/sheets/api/quickstart/python 

def main():
    creds = None

# We take data from these ranges 
# There are 2 sheets: Beta Live Partners and Notify Usage Data Total SMS
# Beta live partners contains service IDs and total intended SMS annual volumes (used to categorise services)
# Notify Usage Data Total SMS contains monthly SMS transaction volumes for each service
# These ranges are contained in the following 2 arrays 

    bplRanges = [
        "LIVE!C2:C",
        "LIVE!L2:L"
    ]

    nudtsRanges = [
        "[DATA]Total-SMS!A3:A",
        "[DATA]Total-SMS!C3:ZZ",
        "[DATA]Total-SMS!C2:ZZ2",
    ]

# We use these dictionaries to map the following 
# The idSMSSizeMap is used to store the mapping of service IDs to their size categorisations 
# The monthlySizeCountMap is used to store the mapping of monthly SMS transactions per each service size

    idSMSSizeMap = {}
    monthlySizeCountMap = {}

# DO NOT DELETE lines 82 to 97
# These are taken from the google sheets API documentation and are used for authentication 

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

# This is calling the service ID and total intended SMS annual volumes from the Beta Live Partners sheet 

    bpl = service.spreadsheets().values().batchGet(spreadsheetId="1JYhE5sJaOJUVMPPDenO2eKqElC75Rygxb1_2mpRKy98", ranges=bplRanges).execute()
    bplResults = bpl.get('valueRanges', [])

# This is calling service ID and monthly SMS tranactions per service from the Notify Usage Data Total SMS sheet 

    nudts = service.spreadsheets().values().batchGet(spreadsheetId="1PEhXtaO5NUS-rKWGylx2ax4bNpkH41U3tCMKBTJ-vWw", ranges=nudtsRanges).execute()
    nudtsResults = nudts.get('valueRanges', [])
   
    if not bplResults:
        print('No data found from bpl sheet.')
    else:

# This extracts the values from the data returned from the API call of the Beta Live Partners sheet

        serviceIDs = bplResults[0]["values"]
        SMSVols = bplResults[1]["values"]

        i = 0
        for id in serviceIDs:
            if len(SMSVols[i]) > 0:
                SMSVal = int(SMSVols[i][0].replace(",", ""))
                idSMSSizeMap[id[0]] = determine_SMS_Size(SMSVal)
            else:
                idSMSSizeMap[id[0]] = "Unknown"
            i += 1

    if not nudtsResults:
        print('No data found from nudts sheet.')
    else:
        serviceIDs = nudtsResults[0]["values"]
        monthlyCounts = nudtsResults[1]["values"]
        dates = nudtsResults[2]["values"]
        unregisteredIDs = []
        i = 0

        for id in serviceIDs:
            if id[0] in idSMSSizeMap:
                SMSSize = idSMSSizeMap[id[0]]
                if i < len(monthlyCounts):
                    month = monthlyCounts[i]
                    monthIndex = 0 
                    for mVal in month: 
                        if monthIndex not in monthlySizeCountMap:
                            monthlySizeCountMap[monthIndex] = MonthlySizeCount()
                        if mVal != "":
                            if SMSSize == "MICRO":
                                monthlySizeCountMap[monthIndex].micro += int(mVal.replace(",", ""))
                            elif SMSSize == "SMALL":
                                monthlySizeCountMap[monthIndex].small += int(mVal.replace(",", ""))
                            elif SMSSize == "MEDIUM":    
                                monthlySizeCountMap[monthIndex].medium += int(mVal.replace(",", ""))
                            elif SMSSize == "LARGE":
                                monthlySizeCountMap[monthIndex].large += int(mVal.replace(",", ""))
                            elif SMSSize == "EXTRA LARGE":
                                monthlySizeCountMap[monthIndex].xl += int(mVal.replace(",", ""))
                            else: 
                                monthlySizeCountMap[monthIndex].micro += int(mVal.replace(",", ""))
                        monthIndex += 1
            else:
                unregisteredIDs.append(id[0])
            i += 1            

        values = []
        values.append(["Month", "Micro", "Small", "Medium", "Large", "Extra Large"])

        for x, y in monthlySizeCountMap.items():
            currentMonth = []
            currentMonth.append(dates[0][x])
            currentMonth.append(y.micro)
            currentMonth.append(y.small)
            currentMonth.append(y.medium)
            currentMonth.append(y.large)
            currentMonth.append(y.xl)
            values.append(currentMonth)

        data = [
            {
                'range': "[Raw Data] SMS!B2:ZZ",
                'values': values
            },
        ]
        body = {
            'valueInputOption': "RAW",
            'data': data
        }

        result = service.spreadsheets().values().batchUpdate(spreadsheetId="16r3DlJv6qkXzPJI3bjyXIeRB6ybtcCE2Mx89YMKd5rg", 
            body=body).execute()

        print("\nWrote SMS Values to spreadsheet.\n")

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Program took ", end - start, " seconds.\n")