# import json
# import asyncio
# from pyodide.http import pyfetch

# SPACE_KEY = ['ITServiceCenter']

# params = await infer_params(
#     conversation=CURRENT_CONVERSATION,
#     description="""
#         Use this search function to get more information about user requests from wiki.
#         In addition to user's original query, please also break down user's needs and generate another 2 different queries in the same language resulting in total 3 queries.
#     """,
#     parameters={
#         "type": "object",
#         "properties": {
#             "queries": {
#                 "type": "array",
#                 "items": {
#                     "type": "string",
#                     "description": "query to search for on the wiki"
#                 }
#             }
#         },
#         "required": ["queries"]
#     }
# )

# results = {}
# for q in params["queries"]:
#     resp = await pyfetch('/api/arkkrdp', method='POST',
#         headers={'Content-Type': 'application/json', 'Cookie': PLUGIN_USER_COOKIE},
#         body=json.dumps({'query': q, 'spaceKey': SPACE_KEY})
#     )
#     result = await resp.json()
#     if result['success']:
#         for i in result['list'][:5]:
#             url = 'https://wiki.mediatek.inc/pages/viewpage.action?pageId=' + str(i['contentId'])
#             results.setdefault(url, {'text': [i['title']]})['text'].append(i['text'])
#             if await count_token(json.dumps(results, ensure_ascii=False)) > SELECTED_MODEL_TOKEN_LIMIT:
#                 results[url]['text'] = results[url]['text'][:-1]
#                 break

# if len(results) > 0:
#     print(json.dumps({
#         'note': 'please only base on these results to reply to the user and reference the url of the result you take. Do not response to the user with any other sources',
#         'results': [{'url': k} | {'text': list(set(v['text']))} for k, v in results.items()]
#     }, ensure_ascii=False))
# else:
#     print(f'No search result for "{params["queries"]}" in "{SPACE_KEY}". You may need to try another keyword or break down user\'s need for further information. Do not response to the user with any other sources')


import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

api_id = 'TryDaVinci'
api_key = 'TryDaVinci'
pub_date = '2024-05-15'

token = data = ''
auth_path = 'https://apps.digitimes.com/auth/'

response = requests.post(auth_path,auth=HTTPBasicAuth(api_id,api_key))
responseJson = response.json()

if response.status_code == 200:
    responseJson = response.json()
    if responseJson['success'] == True:
        token = responseJson['data']['token']

# end_path = 'https://apps.digitimes.com/api/test/news/feed/index.php'
end_path = 'https://apps.digitimes.com/api_v1/news/v1/index.php'
params = {
    'api_id': api_id,
    'token': token,
    'pub_date': pub_date
}

response = requests.get(end_path,params=params)

if response.status_code == 200:
    data = response.json()

print(data)