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

def determine_LETTER_Size(LETTERVal):
    if LETTERVal < MICRO:
        return "MICRO"
    elif LETTERVal >= MICRO and LETTERVal < SMALL:
        return "SMALL"
    elif LETTERVal >= SMALL and LETTERVal < MEDIUM:
        return "MEDIUM"
    elif LETTERVal >= MEDIUM and LETTERVal < LARGE:
        return "LARGE"
    elif LETTERVal >= LARGE:
        return "EXTRA LARGE"

# The rest of this file is adapted from this: https://developers.google.com/sheets/api/quickstart/python 

def main():
    creds = None

# We take data from these ranges 
# There are 2 sheets: Beta Live Partners and Notify Usage Data Total Letters
# Beta live partners contains service IDs and total intended Letter annual volumes (used to categorise services)
# Notify Usage Data Total Letters contains monthly SMS transaction volumes for each service
# These ranges are contained in the following 2 arrays 

    bplRanges = [
        "LIVE!C2:C",
        "LIVE!N2:N"
    ]

    nudlsRanges = [
        "[DATA]Total-Letters!A3:A",
        "[DATA]Total-Letters!C3:ZZ",
        "[DATA]Total-Letters!C2:ZZ2",
    ]

# We use these dictionaries to map the following 
# The idLetterSizeMap is used to store the mapping of service IDs to their size categorisations 
# The monthlySizeCountMap is used to store the mapping of monthly Letter transactions per each service size

    idLETTERSizeMap = {}
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

    nudls = service.spreadsheets().values().batchGet(spreadsheetId="1PEhXtaO5NUS-rKWGylx2ax4bNpkH41U3tCMKBTJ-vWw", ranges=nudlsRanges).execute()
    nudlsResults = nudls.get('valueRanges', [])
   
    if not bplResults:
        print('No data found from bpl sheet.')
    else:

# This extracts the values from the data returned from the API call of the Beta Live Partners sheet

        serviceIDs = bplResults[0]["values"]
        LETTERVols = bplResults[1]["values"]

        i = 0
        for id in serviceIDs:
            if len(LETTERVols[i]) > 0:
                LETTERVal = int(LETTERVols[i][0].replace(",", ""))
                idLETTERSizeMap[id[0]] = determine_LETTER_Size(LETTERVal)
            else:
                idLETTERSizeMap[id[0]] = "Unknown"
            i += 1

    if not nudlsResults:
        print('No data found from nudls sheet.')
    else:
        serviceIDs = nudlsResults[0]["values"]
        monthlyCounts = nudlsResults[1]["values"]
        dates = nudlsResults[2]["values"]
        unregisteredIDs = []
        i = 0

        for id in serviceIDs:
            if id[0] in idLETTERSizeMap:
                LETTERSize = idLETTERSizeMap[id[0]]
                if i < len(monthlyCounts):
                    month = monthlyCounts[i]
                    monthIndex = 0 
                    for mVal in month: 
                        if monthIndex not in monthlySizeCountMap:
                            monthlySizeCountMap[monthIndex] = MonthlySizeCount()
                        if mVal != "":
                            if LETTERSize == "MICRO":
                                monthlySizeCountMap[monthIndex].micro += int(mVal.replace(",", ""))
                            elif LETTERSize == "SMALL":
                                monthlySizeCountMap[monthIndex].small += int(mVal.replace(",", ""))
                            elif LETTERSize == "MEDIUM":    
                                monthlySizeCountMap[monthIndex].medium += int(mVal.replace(",", ""))
                            elif LETTERSize == "LARGE":
                                monthlySizeCountMap[monthIndex].large += int(mVal.replace(",", ""))
                            elif LETTERSize == "EXTRA LARGE":
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
                'range': "[Raw Data] Letter!B2:ZZ",
                'values': values
            },
        ]
        body = {
            'valueInputOption': "RAW",
            'data': data
        }

        result = service.spreadsheets().values().batchUpdate(spreadsheetId="16r3DlJv6qkXzPJI3bjyXIeRB6ybtcCE2Mx89YMKd5rg", 
            body=body).execute()

        print("\nWrote LETTER Values to spreadsheet.\n")

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Program took ", end - start, " seconds.\n")