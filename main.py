import json
import os

FOLDER_NAME = "advancements"
FOLDER_PATH = os.path.join(os.path.dirname(__file__), FOLDER_NAME)
MOD_ID = input("please tell me your the modid of your mod.\n")

def load_all_json_from_folder(folder_path: str) -> dict[str, dict]:
    """
    Iterates through all JSON files in the specified folder and loads them as a Python dictionary, using the filename as the key.

    Args:
        folder_path (str): Folder directory.

    Returns:
        dict[str, dict]: A dictionary of filenames (without extensions) mapped to JSON content.
    """
    result = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            name_without_ext = os.path.splitext(filename)[0]
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                result[name_without_ext] = json.load(f)

    return result


if __name__ == '__main__':
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
        print("Please put your advancement jsons in this " + '"' + FOLDER_NAME + '"' + " folder.")

    else:
        loaded: dict[str, dict] = load_all_json_from_folder(FOLDER_PATH)

        result_dict: dict[str, dict] = {}

        for advancement_name, advancement in loaded.items():
            criteria = advancement["criteria"]
            for criterion_name, criterion in criteria.items():
                if criterion["trigger"] == 'minecraft:inventory_changed':
                    conditions: dict[str, dict] = criterion["conditions"]
                    items: list = list(conditions["items"])
                    for item in items:
                        if "name" in dict(item).keys():
                            if not result_dict.keys().__contains__(MOD_ID + ":" + advancement_name):
                                result_dict[MOD_ID + ":" + advancement_name] = {}
                            new_entry = result_dict[MOD_ID + ":" + advancement_name]
                            new_entry[criterion_name] = MOD_ID + ".template.inv_change.text;" + "item." + item["name"] + ".name"
                        elif "item" in dict(item).keys() and "data" in dict(item).keys():
                            if not result_dict.keys().__contains__(MOD_ID + ":" + advancement_name):
                                result_dict[MOD_ID + ":" + advancement_name] = {}
                            new_entry: dict[str, str] = result_dict[MOD_ID + ":" + advancement_name]
                            new_entry[criterion_name] = MOD_ID + ".template.inv_change.text;" + item["item"] + ":" + str(item["data"])
                elif criterion["trigger"] == 'lastsmith:has_advancement':
                    conditions: dict[str, str] = criterion["conditions"]
                    if not result_dict.keys().__contains__(MOD_ID + ":" + advancement_name):
                        result_dict[MOD_ID + ":" + advancement_name] = {}
                    new_entry = result_dict[MOD_ID + ":" + advancement_name]
                    new_entry[criterion_name] = MOD_ID + ".template.has_advancement.text;" + "advancement." + conditions["advancement"].replace(":", ".", -1) + ".title"
                elif criterion["trigger"] == 'minecraft:player_killed_entity':
                    conditions = criterion["conditions"]
                    if not result_dict.keys().__contains__(MOD_ID + ":" + advancement_name):
                        result_dict[MOD_ID + ":" + advancement_name] = {}
                    new_entry = result_dict[MOD_ID + ":" + advancement_name]
                    entityType: str = conditions["entity"]["type"]
                    if entityType is not None:
                        new_entry[criterion_name] = MOD_ID + ".template.kill_entity.text;" + "entity." + \
                                                entityType.replace(":", ".") + ".name"
                else:
                    if not result_dict.keys().__contains__(MOD_ID + ":" + advancement_name):
                        result_dict[MOD_ID + ":" + advancement_name] = {}
                    new_entry = result_dict[MOD_ID + ":" + advancement_name]
                    new_entry[criterion_name] = MOD_ID + "." + criterion_name + ".text"

        json.dump(result_dict, open(MOD_ID + ".json", "w", encoding="utf-8"))
