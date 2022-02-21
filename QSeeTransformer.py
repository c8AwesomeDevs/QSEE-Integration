import json

class QSeeTransformer():
	def __init__(self):

	def transform_pi_responses_data(self,resps_data):
		try:
			for data in resps_data:
				#for attribute in each element
				for item in data.get("Items"):
					#TODO

		except Exception as e:
			print("An error occured during runtime. Please see error logs")
			raise(e)

	def get_all_unique_timestamp(self,resps_data):
		pass