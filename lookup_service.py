import requests
import xmltodict
import json

from flask import Flask, request
app = Flask(__name__)

name_map = {"01ALLIANCE_COCC": "Central Oregon Community College",
            "01ALLIANCE_CWU": "Central Washington University",
            "01ALLIANCE_CHEMEK": "Chemeketa Community College",
            "01ALLIANCE_CCC": "Clackamas Community College",
            "01ALLIANCE_CC": "Clark College",
            "01ALLIANCE_CONC": "Concordia University",
            "01ALLIANCE_EOU": "Eastern Oregon University",
            "01ALLIANCE_EWU": "Eastern Washington University",
            "01ALLIANCE_GFU": "George Fox University",
            "01ALLIANCE_LANECC": "Lane Community College",
            "01ALLIANCE_LCC": "Lewis & Clark",
            "01ALLIANCE_LINF": "Linfield College",
            "01ALLIANCE_MHCC": "Mt Hood Community College",
            "01ALLIANCE_OHSU": "Oregon Health & Science University",
            "01ALLIANCE_OIT": "Oregon Institute of Technology",
            "01ALLIANCE_OSU": "Oregon State University",
            "01ALLIANCE_PU": "Pacific University",
            "01ALLIANCE_PCC": "Portland Community College",
            "01ALLIANCE_PSU": "Portland State University",
            "01ALLIANCE_REED": "Reed College",
            "01ALLIANCE_STMU": "Saint Martin's University",
            "01ALLIANCE_SPU": "Seattle Pacific University",
            "01ALLIANCE_SEAU": "Seattle University",
            "01ALLIANCE_SOU": "Southern Oregon University",
            "01ALLIANCE_EVSC": "The Evergreen State College",
            "01ALLIANCE_UID": "University of Idaho",
            "01ALLIANCE_UO": "University of Oregon",
            "01ALLIANCE_UPORT": "University of Portland",
            "01ALLIANCE_UPUGS": "University of Puget Sound",
            "01ALLIANCE_UW": "University of Washington",
            "01ALLIANCE_WALLA": "Walla Walla University",
            "01ALLIANCE_WPC": "Warner Pacific College",
            "01ALLIANCE_WSU": "Washington State University",
            "01ALLIANCE_WOU": "Western Oregon University",
            "01ALLIANCE_WWU": "Western Washington University",
            "01ALLIANCE_WHITC": "Whitman College",
            "01ALLIANCE_WW": "Whitworth University",
            "01ALLIANCE_WU": "Willamette University"
            }

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_holdings')
def get_holdings():
      try:
            oclc_num = request.args["oclc_num"]
      except KeyError as e:
            return "no OCLC num supplied"

      api_url_template = "https://na01.alma.exlibrisgroup.com/view/sru/01ALLIANCE_NETWORK?version=1.2&operation=searchRetrieve&query=alma.other_system_number=(OCoLC){}".format(oclc_num)

      res = requests.get(api_url_template)
      dict_response = xmltodict.parse(res.text)
      record_set = dict_response["searchRetrieveResponse"]["records"]["record"]["recordData"]["record"]["datafield"]
      libraries_that_have = []
      for record in record_set:
            if record["@tag"] == "852":
                  libraries_that_have.append(name_map[record["subfield"][0]["#text"]])

      if len(libraries_that_have) == 0:
            return "Nowhere in Summit"

      return ", ".join(libraries_that_have)




