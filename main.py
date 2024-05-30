from g4f.client import Client
from flask import Flask, request

def generateString(items:dict[str, int]) -> str:
    item_string = ""
    for item, count in items.items():
        item_string += f"{count} {item}s, "
    item_string = item_string[:-2]
    # https://stackoverflow.com/a/59082116/17242873
    item_string = " and ".join(item_string.rsplit(", ", 1))

    return f"I am creating a mod for minecraft that adds recipes to a lot of items. If you were to theoretically put the following items into a crafting table, what should it create if I had {item_string}. Respond with just the item id, and nothing else, no explanations, no context, literally just the item id, one word. Think of what it should be, but only respond with items that are in minecraft, and make it make somewhat sense - don't respond with a completely unrelated item unless in real life the items given could make the resulting item. Make sure the recipe is realistic as well - don't just always give out overpowered items that are better than the item that's given in."

def askGPT(string) -> str:
    print("asking gpt...")
    response = client.chat.completions.create(
        [
            {
                "role": "user",
                "content": string
            }
        ],
        "gpt-3.5-turbo"
    )

    return response.choices[0].message.content



app = Flask(__name__)
client = Client()

@app.route("/")
def generic_route():
    return "<html style=\"height:100%\"><head></head><body style=\"height:100%;margin:0\"><div style=\"height:100%;display:flex;justify-content:center;align-items:center;font-family:sans-serif;\">Skibidi toilet</div></body></html>"

@app.route("/craft")
def gpt_route():
    print("Detected get request...")

    if "items" not in request.args:
        return "-1"
    
    # items is formatted like
    # items=tl,tm,tr,ml,mm,mr,bl,bm,br
    # so

    items = request.args.get("items").split(",")
    if len(items) != 9:
        return "-1"

    # then count everything
    counted_items = {}

    for item in items:
        if item not in counted_items:
            counted_items[item] = 0
        counted_items[item] += 1
    
    # then ask gpt what the result should be
    gpt_string = generateString(counted_items)
    print(gpt_string)

    response = askGPT(gpt_string)

    response = response.lower()
    response = response.replace(" ", "_")
    print(f"GPT responded with: {response}")
    return response

app.run("0.0.0.0", 1000)
