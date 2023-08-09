import os
import re
import glob
import json
import uuid
import camelot
import pandas as pd
import warnings
import sys
sys.path.append(
    "/media/shadowmotion/0CD113590CD11359/code/demo/smp/GuaranteedDelivery")
# sys.path.append("d:\\code\\demo\\smp\\GuaranteedDelivery")
warnings.filterwarnings('ignore', category=ResourceWarning)


def load(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


# 源文件夹
CRAWL_DIRECTORY = "../data/chatglm_llm_fintech_raw_dataset/allcrawl"

file_names = glob.glob(CRAWL_DIRECTORY + '/**', recursive=True)

file_names = [e for e in file_names if 'json' in e]

crawl_data_list = [load(file_name) for file_name in file_names]

n = 0
error_data_list = []
for data in crawl_data_list:
    try:
        data["2019年报"]["SECURITY_NAME_ABBR"]
        # print(data["2019年报"]["SECURITY_NAME_ABBR"])
    except:
        error_data_list.append(data)
        n += 1


forrmated_crwal_data_dict = {}
for crawl_data in crawl_data_list:
    for year, report in crawl_data.items():
        company_name = report["SECURITY_NAME_ABBR"]

        forrmated_crwal_data_dict.setdefault(company_name, {})

        for k, v in report.items():
            forrmated_crwal_data_dict[company_name].setdefault(year, {})

            if k not in forrmated_crwal_data_dict[company_name][year]:
                forrmated_crwal_data_dict[company_name][year][k] = v
                continue
            if not v:
                continue
            forrmated_crwal_data_dict[company_name][year][k] = v

with open("../data/test_temp/all_crawl.json", "w") as f:
    json.dump(forrmated_crwal_data_dict, f, indent=2, ensure_ascii=False)
