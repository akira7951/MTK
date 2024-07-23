from pyodide.http import pyfetch
import asyncio
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

params = await infer_params(
    conversation=CURRENT_CONVERSATION,
    description="""Using DALL·E to generate images based on the description provided by the user""",
    parameters={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Generate the prompt based on the user description with the the following guidelines: 1. If the description is not english, then translate it.\n2. Don't create images of politicians or other public figures.",
            },
            "n": {
                "type": "integer",
                "description": "The number of images to be generated requested by the user",
                "default": 1
            }
        },
        "required": ["prompt", "n"],
    },
)

async def do():
    try:
        resp = await pyfetch(
            "/api/dalle/latest",
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Cookie": PLUGIN_USER_COOKIE,
            },
            body=json.dumps({"prompt": params["prompt"]}),
        )
        if resp.status == 400:
            print('Your image generateion request was rejected due to azure content safety policy.')
            return
        result = await resp.json()
        if "error" in result:
            print(result["error"]["message"])
        else:
            img = await pyfetch(result["data"][0]["url"])
            i = io.BytesIO(await img.bytes())
            i = mpimg.imread(i, format="PNG")
            plt.axis('off')
            plt.tight_layout()
            plt.imshow(i, interpolation="nearest")
            plt.show()
            print("Image is generated with the revised prompt: " + result["data"][0]["revised_prompt"])
        return
    except Exception as e:
        print(e.message)


n = params["n"]
if n <= 0:
    n = 1
if n > 3:
    n = 3
    print("Sorry, I can only generate at most 3 images.")

await asyncio.gather(*[do() for _ in range(n)])
print("")