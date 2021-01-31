import json

def read_into_buffer(data):
    data = json.loads(data.decode("ascii"))
    data = data.split("}{")
    messages = []
    for string in data:
        string = string.replace("{", "")
        string = string.replace("}", "")
        string = "{" + string + "}"
        messages.append(string)
    return messages
