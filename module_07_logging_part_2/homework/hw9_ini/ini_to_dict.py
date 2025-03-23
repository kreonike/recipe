import configparser
import json

config_object = configparser.RawConfigParser()
with open("logging_conf.ini", "r") as file:
    config_object.read_file(file)
    output_dict = {s: dict(config_object.items(s)) for s in config_object.sections()}
print("Dictionary config:\n", json.dumps(output_dict, indent=4))
