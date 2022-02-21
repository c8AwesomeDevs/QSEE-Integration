from PIInterface import PIInterface
from QSeeIntegrator import QSeeIntegrator

import json

def get_config_from_file(filepath):
  try:
    with open(filepath, 'r') as j:
      json_data = json.load(j)
      return json_data
  except FileNotFoundError as e:
    print("No configuration found")
    raise(e)

def main():
  #Initialize PI Interface and QSeeIntegrator  Configurations
  pi_config = get_config_from_file("configurations/pi.json")
  qsee_config = get_config_from_file("configurations/qsee.json")

  #Collect PI Data
  pi_interface = PIInterface(pi_config)
  pi_data = pi_interface.collect_data(params=pi_config.get("StreamSetParameters"))

  #Transform PI Data for QSEE Analytics POST API Request
  qsee_integrator = QSeeIntegrator(qsee_config)
  transform_data = qsee_integrator.transform_data(pi_data)

  for readings in transform_data:
    print("Performing QSEE analytics api call")
    resp = qsee_integrator.post_analysis(transform_data[readings])
    resp_data = get_config_from_file("configurations/sample_qsee_response.json") #sample response
    if resp.status_code == 200:
      resp_data = resp.json()
      print("Pushing analytics data to PI")
      try:
        pi_interface.post_analytics_result(resp_data)
      except Exception as e:
        raise(e)
    else:
      pass #TODO Exception





if __name__ == "__main__":
  main()