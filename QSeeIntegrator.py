import requests
import json
from datetime import datetime as datetime
import pandas as pd
import numpy as np

class QSeeIntegrator():
  def __init__(self,config):
    self.company_id = config.get("Company_ID")
    self.products = config.get("Products")

  def transform_data(self,pi_data):
    transformed_data = {}
    try:
      for path in pi_data:
        element_data = pi_data.get(path).get("Items")
        readings = [{}]
        try:
          readings[0]["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #element_data[0].get("Value").get("Timestamp")
        except Exception as e:
          raise(e)

        for attribute_data in element_data:
          attribute = attribute_data.get("Name")
          value = None
          try:
            value = float(attribute_data.get("Value").get("Value"))
          except Exception as e:
            print(e)
          readings[0][attribute] = value
        transformed_data[path] = readings
      return transformed_data
    except Exception as e:
      print("{} : An error occured during runtime. Please see error logs".format(datetime.now()))
      raise(e)

  def post_analysis(self,readings,params={}):
    url_endpoint = "http://osi.qsee.io/api/product_score"#"http://analytics.qsee.io/api/product_score"
    headers = {
      "Content-Type" : "application/json",
      "Accept" : "application/vnd.qsee-soap.v1"
    }
    responses = []
    for product in self.products:
      data = {
        "Company_ID": self.company_id,
        "Product_ID": product,
        "Readings": readings
      }
      print("{} : Performing a POST Request for {} with Product_ID: {} ".format(datetime.now(),url_endpoint,product))
      # print(data)
      resp = requests.post(url_endpoint,headers=headers,data=json.dumps(data))
      if resp.status_code == 200:
        resp_data =  resp.json()
        print(resp_data)
      else:
        print("{} : API Request Failed".format(datetime.now()))
