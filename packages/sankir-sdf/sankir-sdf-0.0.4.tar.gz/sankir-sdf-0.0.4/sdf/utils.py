import csv
import io
import json
import os
import sys
from datetime import datetime


def get_config(path):
    if not os.path.exists(path):
        print("config file not found")
        return False

    with open(path, "r") as f:
        return json.load(f)


def get_filename(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_output_path(blob_name, output_path):
    filename = get_filename(blob_name)
    op_path = os.path.join(output_path, f"{filename}.json")
    print(f"Writing to {op_path}")
    return op_path


def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %X")

def get_fields(data):
    return data.splitlines()[0].decode("utf-8").split(",")
