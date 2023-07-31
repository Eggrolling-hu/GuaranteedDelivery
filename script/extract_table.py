from multiprocessing import Pool
import pandas as pd
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
    path = os.path.join(TAB_DIRECTORY, os.path.basename(
        file_names[0]).split('.')[0])
    if not os.path.exists(path):
        os.makedirs(path)
    tables = camelot.read_pdf(file_name, pages='1-30', parallel=True)
    for i, t in enumerate(tables):
        with open(os.path.join(path, f"{i}.json"), "w") as f:
            json.dump(t.parsing_report, f)
        t.df.to_csv(os.path.join(path, f"{i}.csv"), index=False, sep='\x01')


if __name__ == "__main__":
    file_names = glob.glob(PDF_DIRECTORY + '/*')

    for i, file_name in enumerate(file_names):
        if i < 45:
            continue
        try:
            worker_for_table(file_names[0])
        except:
            print(f"error: {file_name}")
        print(f"Sucess No.{i}")

    # pool = Pool(10)

    # for file_name in file_names[:3]:
    #     pool.apply_async(worker_for_table, args=(file_name,),)

    # # 关闭进程池
    # pool.close()
    # pool.join()
