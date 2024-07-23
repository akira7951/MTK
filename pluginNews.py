from pyodide.http import pyfetch
import asyncio
import base64
api_id = 'xxxxx' # hide
api_key = 'xxxxx' # hide
api_channel = 'CH003'
out_str = ''

token = data = ''
auth_path = 'https://xxxx.digitimes.com/api/auth/'

params = await infer_params(
    conversation=CURRENT_CONVERSATION,
    description="""
        Use this search function to get more information about user requests from wiki.
        In addition to user's original query, please also break down user's needs and generate another 2 different queries in the same language resulting in total 3 queries.
    """,
    parameters={
        "type": "object",
        "properties": {
            "queries": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "query to search for on the wiki"
                }
            }
        },
        "required": ["queries"]
    }
)

for q in params["queries"]:
    if ' ' in q:
        q = f'({q})'
    if q != '':
        out_str = out_str+q+' OR '

out_str = out_str.rstrip(' OR ')

def basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

async def authenticate():
    response = await pyfetch(auth_path,method="POST",headers={
        "Authorization": basic_auth(api_id, api_key)
    })
    if response.status == 200:
        response_json = await response.json()
        if response_json['success'] == True:
            return response_json['data']['token']
        return None

async def fetch_data(token,out_str):
    end_path = 'https://xxxx.digitimes.com/api/search/'
    api_params = {
        'api_id': api_id,
        'token': token,
        'channel': api_channel,
        'query': out_str,
        'scope': 0,
        'sort': 4,
        'start': '2023/01/01',
        'end': '2023/12/31',
        'items': 5
    }
    
    query_string = "&".join([f"{key}={value}" for key, value in api_params.items()])
    url = f"{end_path}?{query_string}"
    response = await pyfetch(url,method="GET")
    
    if response.status == 200:
        return await response.json()
    return None

async def main():
    token = await authenticate()
    if token:
        data = await fetch_data(token,out_str)
        if data:
            return data

await main()