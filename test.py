from PIInterface import PIInterface
from QSeeIntegrator import QSeeIntegrator

import json
import pandas as pd
from datetime import datetime

def get_config_from_file(filepath):
  try:
    with open(filepath, 'r') as j:
      json_data = json.load(j)
      return json_data
  except FileNotFoundError as e:
    print("No configuration found")
    raise(e)

def print_as_table(arr):
  for data in arr:
    print("-"*45)
    print(data)
    print("|{:<20} | {:<20}|".format('Key','Number'))
    print("-"*45)
    for k,v in arr[data].items():
      print(k,v)

def save_buffer(dict):
  date_now = datetime.now().strftime("%Y%m%d")
  for key in dict:
    formatted_csv = "backup\\{}..{}.csv".format(key.replace("\\","."),date_now)
    df = pd.DataFrame(dict[key])
    df.to_csv(formatted_csv, mode='a+', index=False,header=False)

def main():
  print("****************************************************")
  print("{} : Running Integrator".format(datetime.now()))
  #Initialize PI Interface and QSeeIntegrator  Configurations
  pi_config = get_config_from_file("configurations/pi.json")
  qsee_config = get_config_from_file("configurations/qsee.json")

  #Collect PI Data
  pi_interface = PIInterface(pi_config)
  pi_data = pi_interface.collect_data(params=pi_config.get("StreamSetParameters"))

  #Transform PI Data for QSEE Analytics POST API Request
  qsee_integrator = QSeeIntegrator(qsee_config)
  transform_data = qsee_integrator.transform_data(pi_data)
  save_buffer(transform_data)


  for path in transform_data:
    print(transform_data[path])
    qsee_integrator.post_analysis(transform_data[path])
    #get_config_from_file("configurations/sample_qsee_response.json") #sample response
    print("{} : Integrator run finished".format(datetime.now()))
    print("****************************************************")

if __name__ == "__main__":
  main()