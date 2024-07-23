import urllib.parse
from pyodide.http import pyfetch

params = await infer_params(
    conversation=CURRENT_CONVERSATION,
    description="""create the diagram based on what user asked and pass it to the plugin API to render. Mermaid is the preferred language.
    """,
    parameters={
        "type": "object",
        "properties": {
            "diagram": {
                "type": "string",
                "description": "the graph representation in Mermaid",
                "examples": [
                    """
graph TB
  A["Web Browser"] -- "HTTP API Request" --> B["Load Balancer"]
  B -- "HTTP Request" --> C["Crossover"]
  C -- "Talks to" --> D["Redis"]
  C -- "Talks to" --> E["MySQL"]
  C -- "Downstream API Request" --> F["Multiplex"]
  F -- "Returns Job ID" --> C
  C -- "Long Poll API Request" --> G["Evaluator"]
  G -- "API Call" --> F
  G -- "API Call" --> H["Result-Fetcher"]
  H -- "Downloads Results" --> I["S3 or GCP Cloud Buckets"]
  I -- "Results Stream" --> G
  G -- "Results Stream" --> C
  C -- "API Response" --> A
""", """
@startuml
 left to right direction
 actor "Food Critic" as fc
 rectangle Restaurant {
     usecase "Eat Food" as UC1
 usecase "Pay for Food" as UC2
 usecase "Drink" as UC3
 }
 fc --> UC1
 fc --> UC2
 fc --> UC3
 @enduml
"""
                ]
            }
        },
        "required": ["diagram"]
    }
)

resp = await pyfetch('/api/kroki/render?diagramLanguage=mermaid&diagramType=graph&' + urllib.parse.urlencode(params))
result = await resp.json()
image = result['results'][0].pop('image')
edit = result['results'][0].pop('editDiagramOnline')
result['results'][0]['markdownImageURL'] = f'![image]({image})'
result['results'][0]['editDiagramOnlineURL'] = f'[edit online]({edit})'
print(result['results'][0])
