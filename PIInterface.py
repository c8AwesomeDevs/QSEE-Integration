import requests
import json
from datetime import datetime as datetime

class PIInterface():
  def __init__(self,config):
    print("{} : Initializing PI Collector Configurations".format(datetime.now()))
    self.host = config.get("PIWebAPIHost","localhost")
    auth_json = config.get("Authentication")
    self.auth = (auth_json.get("username"),auth_json.get("password"))
    self.resource_paths = config.get("ResourcePaths")
    self.streamsets_parameters = config.get("StreamSetParameters")


  def collect_data(self,params=None):
    print("{} : Collecting Data".format(datetime.now()))
    resps_data = {}
    for path in self.resource_paths:
      try:
        print("{} : Collecting Recorded Attribute Data from {}".format(datetime.now(),path))
        resp = self.get_element_by_path(path)
        if resp.status_code == 200:
          content = resp.json()
          element_webid = content["WebId"]
          resp = self.get_values_streamset(element_webid,self.streamsets_parameters.get("GET"))
          resps_data[path] = resp.json()
        else:
          print("{} : API Request Unsucessful".format(datetime.now()))
      except Exception as e:
        print("{} : An error occured during runtime. Please see error logs".format(datetime.now()))
        raise(e)
    return resps_data


  def get_values_streamset(self,webid,params=None):
    url_endpoint = "https://{}/piwebapi/streamsets/{}/value".format(self.host,webid)
    return requests.get(url_endpoint,auth=self.auth,params=params,verify=False)


  def post_values_streamset(self,webid,data):
    url_endpoint = "https://{}/piwebapi/streamsets/{}/value".format(self.host,webid)
    return requests.post(url_endpoint,auth=self.auth,data=json.dumps(data),verify=False)

  def get_element_by_path(self,path):
    url_endpoint = "https://{}/piwebapi/elements?path={}".format(self.host,path)
    return requests.get(url_endpoint,auth=self.auth,verify=False)

  def get_attr_webid_map(self,webid):
    #get element attributes
    attr_webid_map = {} 
    try:
      url_endpoint = "https://{}/piwebapi/elements/{}/attributes".format(self.host,webid)
      resp = requests.get(url_endpoint,auth=self.auth,params=self.streamsets_parameters.get("POST"),verify=False)
      for item in resp.json().get("Items"):
        attr_webid_map[item.get("Name")] = item.get("WebId")
      return attr_webid_map
    except Exception as e:
      raise(e)

  def transform_data(self,attr_webid_map,resp_data):
    request_data = []
    for attr in resp_data:
      if "influencers" in attr:
        for child_attr in resp_data.get(attr):
          attr_webid = attr_webid_map.get("{}.{}".format(attr,child_attr))
          if attr_webid:
            pi_data = {
              "WebId": attr_webid,
              "Value": {
                "Timestamp": resp_data.get("timestamp"),
                "Value": float(resp_data.get(attr).get(child_attr))
              }
            }
            request_data.append(pi_data)          
      else:
        attr_webid = attr_webid_map.get(attr)
        if attr_webid:
          pi_data = {
            "WebId": attr_webid,
            "Value": {
              "Timestamp": resp_data.get("timestamp"),
              "Value": float(resp_data.get(attr))
            }
          }
          request_data.append(pi_data)
    return request_data

  def post_analytics_result(self,path,resp_data):
    try:
      resp = self.get_element_by_path(path)
      if resp.status_code == 200:
        content = resp.json()
        element_webid = content["WebId"]        
        attr_webid_map = self.get_attr_webid_map(element_webid)
        
        #Format QSEE Data to PI Data
        print("{} : Formatting QSEE Response to PI Data".format(datetime.now()))
        request_data = self.transform_data(attr_webid_map,resp_data)
        #Push Analytics Results Back to PI
        print("{} : Pushing analytics data to PI".format(datetime.now()))
        resp = self.post_values_streamset(element_webid,request_data)
        print(resp)


      else:
        print("{} : API Request Unsucessful".format())
    except Exception as e:
      print("{} : An error occured during runtime. Please see error logs".format())
      raise(e)  


