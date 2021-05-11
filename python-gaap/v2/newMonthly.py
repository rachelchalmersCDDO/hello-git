#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import statements (some used for google sheets API)

from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import time
import dateparser
import pprint

# Constant variables used to represent cut off for service size categorisation

MICRO = 50000
SMALL = 250000
MEDIUM = 1000000
LARGE = 5000000

seenIDs = {}
sanityCheck = {}

# This is an object which stores boolean values to represent whether the ID has already been seen for SMS, email and letters
# Additionally it stores the size categorisations for SMS, Email and Letter
# A new instance of the object is created for each ID (like a template)

class IDObj:
	def __init__(self):
		self.sms = False 
		self.email = False 
		self.both = False 
		self.smsSize = ''
		self.emailSize = ''

		self.letter = False 
		self.letterSize = ''

# Class object used to group data related to the same month
# This stores transaction volumes for each new service size classification for each month
# A dictionary is used with the type as the key and an array as the value 
# Each index of the array represents transaction volume thresholds for each size, eg index 0 = Micro, 1 = Small etc

class MonthlyCount:
	def __init__(self):
		self.date = ''
		self.sizeCounts = {}

		self.sizeCounts['sms'] = []
		self.sizeCounts['email'] = []
		self.sizeCounts['both'] = []
		self.sizeCounts['letter'] = []

		self.sizeCounts['sms'] = [0, 0, 0, 0, 0]
		self.sizeCounts['email'] = [0, 0, 0, 0, 0]
		self.sizeCounts['both'] = [0, 0, 0, 0, 0]
		self.sizeCounts['letter'] = [0, 0, 0, 0, 0]

	def addToCount(self, type, size):
		if size == 'MICRO':
			self.sizeCounts[type][0] += 1
		elif size == 'SMALL':
			self.sizeCounts[type][1] += 1
		elif size == 'MEDIUM':
			self.sizeCounts[type][2] += 1
		elif size == 'LARGE':
			self.sizeCounts[type][3] += 1
		else:
			self.sizeCounts[type][4] += 1

# This function passes in SMS Values and returns SMS sizes (one of five categories)
# Integer is passed in & a string is returned

def determineSize(SMSVal):
	if SMSVal < MICRO:
		return 'MICRO'
	elif SMSVal >= MICRO and SMSVal < SMALL:
		return 'SMALL'
	elif SMSVal >= SMALL and SMSVal < MEDIUM:
		return 'MEDIUM'
	elif SMSVal >= MEDIUM and SMSVal < LARGE:
		return 'LARGE'
	elif SMSVal > LARGE:
		return 'EXTRA LARGE'
	else:
		return 'MICRO'

# when an ID appears twice in the same month (sending SMS and email) we take the smaller size category
# this fundtion takes the SMS and email size and returns the smalller 

def takeSmallerSize(smsSize, emailSize):
	if smsSize == 'MICRO' or emailSize == 'MICRO':
		return 'MICRO'
	elif smsSize == 'SMALL' or emailSize == 'SMALL':
		return 'SMALL'
	elif smsSize == 'MEDIUM' or emailSize == 'MEDIUM':
		return 'MEDIUM'
	elif smsSize == 'LARGE' or emailSize == 'LARGE':
		return 'LARGE'
	elif smsSize == 'EXTRA LARGE' or emailSize == 'EXTRA LARGE':
		return 'EXTRA LARGE'
	else:
		return 'MICRO'

# The rest of this file is adapted from this: https://developers.google.com/sheets/api/quickstart/python

def main():
	creds = None

# We take data from these ranges
# There are 2 sheets: Beta Live Partners and Notify Usage Data Total SMS
# Beta live partners contains service IDs and total intended SMS annual volumes (used to categorise services)
# Notify Usage Data Total SMS contains monthly SMS transaction volumes for each service
# These ranges are contained in the following 2 arrays

	bpRanges = ['LIVE!C2:C', 'LIVE!L2:L', 'LIVE!M2:M', 'LIVE!N2:N']
	nudRanges = ['[IMPORT]RAW-DATA!A2:D']

# DO NOT DELETE lines 82 to 97
# These are taken from the google sheets API documentation and are used for authentication

	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	service = build('sheets', 'v4', credentials=creds)
	sheet = service.spreadsheets()

# This is calling the service ID and total intended SMS annual volumes from the Beta Live Partners sheet

	bp = service.spreadsheets().values().batchGet(spreadsheetId='1JYhE5sJaOJUVMPPDenO2eKqElC75Rygxb1_2mpRKy98', ranges=bpRanges).execute()
	bpResults = bp.get('valueRanges', [])

# This is calling service ID and monthly SMS tranactions per service from the Notify Usage Data Total SMS sheet

	nud = service.spreadsheets().values().batchGet(spreadsheetId='1PEhXtaO5NUS-rKWGylx2ax4bNpkH41U3tCMKBTJ-vWw', ranges=nudRanges).execute()
	nudResults = nud.get('valueRanges', [])

	if not bpResults:
		print('No data found from bp sheet.')
	else:

# This extracts the values from the data returned from the API call of the Beta Live Partners sheet

		serviceIDs = bpResults[0]['values']
		smsVols = bpResults[1]['values']
		emailVols = bpResults[2]['values']
		letterVols = bpResults[3]['values']

# loop through each service ID returned from bpl results API call 

		for i in range(0, len(serviceIDs)):
			seenIDs[serviceIDs[i][0]] = IDObj()

 # if there is are SMS volumes returned (the cell wasnt blank)  
 # replaces all commas and converts from a string to an integer and then calls the size function to return the size 
 # if the value wsa blank then we assign MICRO by default

			if len(smsVols[i]) > 0:
				smsVal = int(smsVols[i][0].replace(',', ''))
				seenIDs[serviceIDs[i][0]].smsSize = determineSize(smsVal)
			else:
				seenIDs[serviceIDs[i][0]].smsSize = 'MICRO'

# if there is are EMAIL volumes returned (the cell wasnt blank)  
 # replaces all commas and converts from a string to an integer and then calls the size function to return the size 
 # if the value wsa blank then we assign MICRO by default
			
			if len(emailVols[i]) > 0:
				emailVal = int(emailVols[i][0].replace(',', ''))
				seenIDs[serviceIDs[i][0]].emailSize = determineSize(emailVal)
			else:
				seenIDs[serviceIDs[i][0]].emailSize = 'MICRO'
				
# if there is are LETTER volumes returned (the cell wasnt blank)  
 # replaces all commas and converts from a string to an integer and then calls the size function to return the size 
 # if the value wsa blank then we assign MICRO by default

			if len(letterVols[i]) > 0:
				letterVal = int(letterVols[i][0].replace(',', ''))
				seenIDs[serviceIDs[i][0]].letterSize = determineSize(letterVal)
			else:
				seenIDs[serviceIDs[i][0]].letterSize = 'MICRO'



# Processing NUD data:
# get the results from the google API from the notify usage sheet 

	if not nudResults:
		print('No data found from NUD sheet.')
	else:
		results = nudResults[0]['values']
		i = 0
		date = ''
		months = []
		currentMonth = {}

# loop through results 

		for row in results:

# row represents ID, for each ID get the current month, Id and communication type 

			curDate = row[0]
			curID = row[1]
			curCom = row[3]

# if we see a new date we need to restart the count as we are only counting the new services for the month 
# all values are stored in their own monthly count object 

			if date != curDate:
				if date != '':
					for key, value in currentMonth.items():
						sizeType = ''

						if ('sms' in value) and ('email' in value):
							sizeType = 'both'
							size = takeSmallerSize(seenIDs[key].smsSize, seenIDs[key].emailSize)
						
						elif 'sms' in value:
							sizeType = 'sms'
							size = seenIDs[key].smsSize
						
						elif 'email' in value:
							sizeType = 'email'
							size = seenIDs[key].emailSize
						
						if sizeType != '':
							curMonth.addToCount(sizeType, size)

						if 'letter' in value: 
							curMonth.addToCount('letter', seenIDs[key].letterSize)

					months.append(curMonth)
					currentMonth = {}
				
				date = curDate
				curMonth = MonthlyCount()
				curMonth.date = date


# update ID object to check whether they've been seen before and stores their value (Micro, Small etc) in the relevant objects 

			if curID in seenIDs:

				if curID not in sanityCheck:
					sanityCheck[curID] = [0, 0, 0]
				
				if curCom == 'sms':
					sanityCheck[curID][0] += 1
				elif curCom == 'email':
					sanityCheck[curID][1] += 1					
				elif curCom == 'letter':
					sanityCheck[curID][2] += 1

				if curID not in currentMonth:
					currentMonth[curID] = []

				if curCom == 'sms' and (seenIDs[curID].sms is False):
					currentMonth[curID].append(curCom)
					seenIDs[curID].sms = True

				elif curCom == 'email' and (seenIDs[curID].email is False):
					currentMonth[curID].append(curCom)
					seenIDs[curID].email = True

				elif curCom == 'letter' and (seenIDs[curID].letter is False):
					currentMonth[curID].append(curCom)
					seenIDs[curID].letter = True

# PRINTING VALUES TO TERMINAL: 
		for month in months:
			print('==================================================================================================')

			print('Date:')
			print(month.date)

			print('SMS Micro, \tSMS Small, \tSMS Medium, \tSMS Large, \tSMS XL')
			print(month.sizeCounts['sms'][0], '\t\t', month.sizeCounts['sms'][1], '\t\t', month.sizeCounts['sms'][2], '\t\t', month.sizeCounts['sms'][3], '\t\t', month.sizeCounts['sms'][4])

			print('Email Micro, \tEmail Small, \tEmail Medium, \tEmail Large, \tEmail XL')
			print(month.sizeCounts['email'][0], '\t\t', month.sizeCounts['email'][1], '\t\t', month.sizeCounts['email'][2], '\t\t', month.sizeCounts['email'][3], '\t\t', month.sizeCounts['email'][4])

			print('Both Micro, \tBoth Small, \tBoth Medium, \tBoth Large, \tBoth XL')
			print(month.sizeCounts['both'][0], '\t\t', month.sizeCounts['both'][1], '\t\t', month.sizeCounts['both'][2], '\t\t', month.sizeCounts['both'][3], '\t\t', month.sizeCounts['both'][4])

			print('Letter Micro, \tLetter Small, \tLetter Medium, \tLetter Large, \tLetter XL')
			print(month.sizeCounts['letter'][0], '\t\t', month.sizeCounts['letter'][1], '\t\t', month.sizeCounts['letter'][2], '\t\t', month.sizeCounts['letter'][3], '\t\t', month.sizeCounts['letter'][4])

			print('==================================================================================================\n')

# PRINTING VALUES TO SHEET: 
		values = []
		values.append(
			["Month", "",
			"SMS Micro", "SMS Small", "SMS Medium", "SMS Large", "SMS Extra Large", "",
			"Email Micro", "Email Small", "Email Medium", "Email Large", "Email Extra Large", "",
			"Both Micro", "Both Small", "Both Medium", "Both Large", "Both Extra Large", "",
			"Letter Micro", "Letter Small", "Letter Medium", "Letter Large", "Letter Extra Large"]
		)

		for month in months:
		    currentMonth = []
		    currentMonth.append(month.date)
		    currentMonth.append('')

		    currentMonth.append(month.sizeCounts['sms'][0])
		    currentMonth.append(month.sizeCounts['sms'][1])
		    currentMonth.append(month.sizeCounts['sms'][2])
		    currentMonth.append(month.sizeCounts['sms'][3])
		    currentMonth.append(month.sizeCounts['sms'][4])
		    currentMonth.append('')

		    currentMonth.append(month.sizeCounts['email'][0])
		    currentMonth.append(month.sizeCounts['email'][1])
		    currentMonth.append(month.sizeCounts['email'][2])
		    currentMonth.append(month.sizeCounts['email'][3])
		    currentMonth.append(month.sizeCounts['email'][4])
		    currentMonth.append('')

		    currentMonth.append(month.sizeCounts['both'][0])
		    currentMonth.append(month.sizeCounts['both'][1])
		    currentMonth.append(month.sizeCounts['both'][2])
		    currentMonth.append(month.sizeCounts['both'][3])
		    currentMonth.append(month.sizeCounts['both'][4])
		    currentMonth.append('')

		    currentMonth.append(month.sizeCounts['letter'][0])
		    currentMonth.append(month.sizeCounts['letter'][1])
		    currentMonth.append(month.sizeCounts['letter'][2])
		    currentMonth.append(month.sizeCounts['letter'][3])
		    currentMonth.append(month.sizeCounts['letter'][4])
		    currentMonth.append('')

		    values.append(currentMonth)

		data = [
		    {
		        'range': "[Raw Data] Monthly Service Additions!B2:ZZ",
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

# SANITY CHECK: 
		print('==================================================================================================\n')

		totalCount = 0
		for x, y in sanityCheck.items():
			print('ID: ', x, "\tseen for sms: ", y[0],  "\tseen for email: ", y[1], 
				"\tseen for letter: ", y[2], "\tfor a total of: ", (y[0] + y[1] + y[2]),"\ttimes.")
			totalCount += y[0]
			totalCount += y[1]
			totalCount += y[2]
		
		print('\n==================================================================================================')

		print('\nnumber of unique ids = ', len(sanityCheck))
		print('total count = ', totalCount)
		print('\n==================================================================================================\n')


if __name__ == '__main__':
	start = time.time()
	main()
	end = time.time()
	print('Program took ', end - start, ' seconds.\n')
