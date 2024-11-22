import os


def get_files(directory):
    json_list = []

    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path) and item.endswith(".json"):
            json_list.append(item.replace(".json", ""))

    return json_list
