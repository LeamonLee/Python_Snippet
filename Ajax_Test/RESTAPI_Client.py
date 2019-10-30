# import requests
# from requests.auth import HTTPDigestAuth
# import json

# # Replace with the correct URL
# url = "http://127.0.0.1:8000/api/music/2"

# # It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime

# # myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("username: "), raw_input("Password: ")), verify=True)
# myResponse = requests.get(url)
# print("The response of requests: ", myResponse)
# print("The response of request's status: ", myResponse.status_code)

# # For successful API call, response code will be 200 (OK)
# if(myResponse.ok):

#     # Loading the response data into a dict variable
#     # json.loads takes in only binary or string variables so using content to fetch binary content
#     # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
#     jsonData = json.loads(myResponse.content)
#     print("JsonData: ", jsonData)
#     print("The response contains {0} properties".format(len(jsonData)))
#     print("\n")
    
#     for key, value in jsonData.items():
#         print(key, value)

#     Datakeys = list(jsonData.keys())
#     for key in Datakeys:
#         print(key, " : ",  jsonData[key])
# else:
#   # If response code is not ok (200), print the resulting http error code with description
#     myResponse.raise_for_status()



# =============================================================================

import requests
url = 'http://127.0.0.1:8000/api/music/'
data = {
    "song": "TestSong",
    "singer": "TestSinger"
}
# response = requests.post(url, json=data)      # Both this line and next line work, but gotta figure out the difference
response = requests.post(url, data=data)
print(response.json())
print(response.ok, response.status_code)
print(response.content)

# =============================================================================

# import requests

# url = 'http://www.whoscored.com/stageplayerstatfeed'
# params = {
#     'field': '1',
#     'isAscending': 'false',
#     'orderBy': 'Rating',
#     'playerId': '-1',
#     'stageId': '9155',
#     'teamId': '32'
# }
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
#            'X-Requested-With': 'XMLHttpRequest',
#            'Host': 'www.whoscored.com',
#            'Referer': 'http://www.whoscored.com/Teams/32/'}

# response = requests.get(url, params=params, headers=headers)

# fixtures = response.json()
# print(fixtures)