import json


def load_json_file(name, formating=True):
    with open(name, mode="r", encoding="utf-8") as file:
        data_file = json.loads(file.read())
    if formating:
        text = ["    ".join([row[0].ljust(22, " "), row[1]]) for row in data_file.items()]
        return text
    return data_file


def save_json_file(arg):
    with open("users.json", mode="w", encoding="utf-8") as file:
        file.write(json.dumps(arg))


def load_data_file(name):
    with open(name, mode="r", encoding="utf-8") as file:
        text = file.read().split("\n")
    return text


def formating(arr):
    if not arr:
        return ""
    text = ["    ".join([row[0].ljust(22, " "), str(row[1])]) for row in arr]
    return text
