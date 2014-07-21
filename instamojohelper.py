import conf
import csv
from instamojo import Instamojo
from datetime import datetime
class InstamojoHelper:


	def __init__(self):

		self.api = Instamojo(api_id=conf.api_id, token=conf.token)
		
		self.TITLE = 0
		self.BASE_PRICE = 1
		self.CURRENCY = 2
		self.DESCRIPTION = 3
		self.QUANTITY = 4
		self.START_DATE = 5
		self.END_DATE = 6
		self.VENUE = 7
		self.TIMEZONE = 8
		self.REDIRECT_URL = 9
		self.WEBHOOK_URL = 10
		self.NOTE = 11


	def create_offers_from_file(self,inp_file):

		status_list = []

		with open(inp_file,'r') as offer_file:

			reader = csv.reader(offer_file,delimiter=',')
			row_number = 1

			for row in reader:
				validated_line = self._validate_line(row,row_number)
				status_list.append(validated_line)

				if validated_line['status']:
					response = self._create_offer(row)
					print response

				row_number += 1

		print status_list


	def _validate_line(self,line,row_number):

		status_dict = {}

		CURRENCIES = ['INR','USD']
		MAX_COLUMN_LENGTH = 11

		status_dict['row_number'] = row_number

		# check if the row is empty
		if len(line) == 0: 
			status_dict['status'] = False 
			status_dict['message'] = 'offer line is empty '	


		# check if the all the columns are present
		elif len(line) < 12:
			status_dict['status'] = False 
			status_dict['message'] = 'offer line does not have all the columns '	

		# check if the all the columns are present
		elif len(line[self.TITLE]) == 0 or len(line[self.BASE_PRICE]) == 0 or len(line[self.CURRENCY]) == 0:

			status_dict['status'] = False 
			status_dict['message'] = 'required columns does not exist'	

		# check if the title has 200 characters
		elif len(line[self.TITLE].strip()) > 200:
			status_dict['status'] = False 
			status_dict['message'] = 'offer line does not have title or base price or currency type mentioned'	

		# check currency 
		elif line[self.CURRENCY] not in currencies:
			status_dict['status'] = False 
			status_dict['message'] = 'right currency is not mentioned'	

		# check quantity
		elif len(line[self.QUANTITY]) > 0 and int(line[self.QUANTITY]) < 0:
			status_dict['status'] = False 
			status_dict['message'] = 'Quantity mentioned is < than 0'	


		# check start date
		elif len(line[self.START_DATE]) > 0:
			try:
				check_start_date = datetime.strptime(line[self.START_DATE],'%Y-%m-%d %H:%M')
			except ValueError as e:
				status_dict['status'] = False 
				status_dict['message'] = 'start date in invalid format'

		# check end date
		elif len(line[self.END_DATE]) > 0:
			try:
				check_end_date = datetime.strptime(line[self.END_DATE],'%Y-%m-%d %H:%M')
			except ValueError as e:
				status_dict['status'] = False 
				status_dict['message'] = 'end date in invalid format'
		else:
			status_dict['status'] = True 
			status_dict['message'] = ''
		
		return status_dict 	

	def _create_offer(self,offer):

		title = offer[self.TITLE]
		base_price = offer[self.BASE_PRICE]
		currency = offer[self.CURRENCY]
		description = offer[self.DESCRIPTION]
		quantity = offer[self.QUANTITY]
		start_date = offer[self.START_DATE]
		end_date = offer[self.END_DATE]
		venue = offer[self.VENUE]
		timezone = offer[self.TIMEZONE]
		redirect_url = offer[self.REDIRECT_URL]
		webhook_url = offer[self.WEBHOOK_URL]
		note = offer[self.NOTE]
	
		api_response = self.api.offer_create(title,base_price,currency,description,quantity,start_date,end_date,venue,timezone,redirect_url,webhook_url,note)
		return api_response


