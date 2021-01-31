import json

def read_into_buffer(data):
    if not data:
        return []
    # data = json.loads(data.decode("ascii"))
    data = data.decode("ascii")
    print(data)
    data = data.split("}{")
    messages = []
    for string in data:
        string = string.replace("{", "")
        string = string.replace("}", "")
        string = "{" + string + "}"
        message = json.loads(string)
        messages.append(message)
    return messages
