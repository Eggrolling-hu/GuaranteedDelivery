from multiprocessing import Pool
import pandas as pd
import argparse
import camelot
import json
import glob
import re
import os


# 源文件夹
PDF_DIRECTORY = "../data/chatglm_llm_fintech_raw_dataset/allpdf"
# 转化后文本文件夹
TXT_DIRECTORY = "../data/chatglm_llm_fintech_raw_dataset/alltxt"
# 转化后表格文件夹
TAB_DIRECTORY = "../data/chatglm_llm_fintech_raw_dataset/alltable"
# 转化后准备存入向量数据库文件夹
VEC_DIRECTORY = "../data/chatglm_llm_fintech_raw_dataset/alldata"


def worker_for_table(file_name):
    path = os.path.join(
        TAB_DIRECTORY, os.path.basename(file_name).split('.')[0])
    if not os.path.exists(path):
        os.makedirs(path)
    tables = camelot.read_pdf(file_name, pages='1-30', parallel=True)
    for i, t in enumerate(tables):
        with open(os.path.join(path, f"{i}.json"), "w") as f:
            json.dump(t.parsing_report, f)
        t.df.to_csv(os.path.join(path, f"{i}.csv"), index=False, sep='\x01')
    return tables


# 列名+是+信息
def row_column_data(df):
    m, n = df.shape
    res_list = []
    for i in range(1, m):
        for j in range(0, n):
            res_list.append(f"{df.loc[i, 0]}是{df.loc[i, j]}")
    return res_list


# 列名+的+行名+是+信息
def column_row_data(df):
    m, n = df.shape
    res_list = []
    for i in range(1, m):
        for j in range(1, n):
            res_list.append(f"{df.loc[i, 0]}的{df.loc[0, j]}是{df.loc[i, j]}")
            res_list.append(f"{df.loc[0, j]}的{df.loc[i, 0]}是{df.loc[i, j]}")
    return res_list


def ToTopic(path, tables):
    with open(path, "w", encoding='utf-8') as f:
        keyword = set()

        for t in tables:
            df = t.df
            if df.size < 4:
                continue
            df = df.applymap(lambda x: x.replace(
                "\n", "") if type(x) == str else x)

            plain_txt_list = []

            if df.shape[1] > 2:
                plain_txt_list = column_row_data(df)
            if df.shape[1] == 2:
                plain_txt_list = row_column_data(df)

            plain_txt_list = set(plain_txt_list)

            for txt in plain_txt_list:
                if "指是指" in txt:
                    continue
                if txt[-1] in ["是", "指"]:
                    continue
                if txt[0] in ["的"]:
                    continue
                if txt[0].isdigit() and (not txt[1].isdigit()):
                    continue
                if txt.count("%") >= 2:
                    continue
                if len(txt) < 2:
                    continue
                if "是" in txt:
                    s = txt.split('是')
                    if s[0] == s[1]:
                        continue
                    if s[0] in keyword:
                        continue
                    keyword.add(s[0])
                f.write(txt+'\n')


if __name__ == "__main__":
    file_names = glob.glob(PDF_DIRECTORY + '/*')

    parser = argparse.ArgumentParser()
    parser.add_argument("num1", type=int, help="开始序号")
    parser.add_argument("num2", type=int, help="结束序号")
    args = parser.parse_args()

    for i, file_name in enumerate(file_names):
        # 断点重连
        if i < args.num1 or i >= args.num2:
            continue
        tables = None
        try:
            tables = worker_for_table(file_name)
        except:
            print(f"Extract Fail No.{i} {os.path.basename(file_name)}")
            continue
        try:
            path = os.path.join(
                TAB_DIRECTORY, os.path.basename(file_name).split('.')[0]+".cal")
            ToTopic(path, tables)
        except:
            print(f"Transform Fail No.{i} {os.path.basename(file_name)}")
            continue

        print(f"Sucess No.{i} {os.path.basename(file_name)}")
