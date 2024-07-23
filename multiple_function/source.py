import json

response = await chat(
    conversation=CURRENT_CONVERSATION + [
        {
        "role": "system",
        "content": "Only use the functions you have been provided with."
        }
    ],
    functions=[
        {
            "name": "summarization",
            "description": "summarize the conversation",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "the summary of the conversation"
                    }
                },
                "required": ["summary"]
            }
        },
        {
            "name": "extract_keywords",
            "description": "extracting from the conversation",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "one keyword extracted from the conversation"
                        }
                    }
                },
                "required": ["keywords"]
            }
        }
    ]
)

if 'function_call' in response:
    if response['function_call']['name'] == 'save_summarization':
        print("The summary of the converstaion is ", json.loads(response['function_call']['arguments'])['summary'])
    elif response['function_call']['name'] == 'save_extracted_keywords':
        print("The keywords of the converstaion are ", json.loads(response['function_call']['arguments'])['keywords'])
else:
    print(response['content'])