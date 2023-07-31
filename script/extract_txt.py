from transformers import AutoTokenizer
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


def read_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\'', '\"')
            line = line.replace('<', '\"')
            line = line.replace('>', '\"')
            # 用正则表达式找到所有双引号包围的数组
            # matches = re.findall(r'"\[.*?\]"', line)
            matches = re.findall(r'"\[.*\]"', line)
            for match in matches:
                # 将数组中的双引号去掉，并替换原字符串中的部分
                corrected = match.replace('\"', '')
                corrected = match[1:-1]
                line = line.replace(match, corrected)
            try:
                row_dict = json.loads(line)
            except:
                splited_line = line.split("\"inside\": ")
                s1, s2 = splited_line[0], splited_line[1]
                s2 = s2.replace("\"", "\'")
                s2 = s2.replace("\\'", "\"")
                s2 = s2 if s2[0] != "\'" else "\"" + s2[1:-2] + "\"}"
                # s2 = s2[:-2] + "}" if s2[0] == "[" and s2[-3:] == "\'}\n" else s2
                s2 = s2.replace("]\'}\n", "]}")

                formatted = s1+"\"inside\": "+s2

                try:
                    row_dict = json.loads(formatted)
                except:
                    # print(s2[-3:], s2)
                    # print(f"解析错误: {line}")
                    s2 = s2.replace("\\", "")
                    s2 = s2.replace("\"", "\'")
                    s2 = s2.replace("\n", "")
                    s2 = s2.replace("}", "")
                    s2 = "\"" + s2 + "\"}"
                    formatted = s1+"\"inside\": "+s2
                    try:
                        row_dict = json.loads(formatted)
                    except:
                        print(f"解析错误: {line}")
                        print(formatted)
                    # break
            data.append(row_dict)
    return data


def is_title(e):
    n = len(e['inside'])
    if e['type'] != 'text':
        return False
    if n > 2 and e['inside'][0] in ("第", "（", "("):
        return True
    if n > 1 and e['inside'][0] in "一二三四五六七八九十":
        return True
    if n > 1 and e['inside'][:2] in [f"{i}{l}" for i in range(10) for l in ['.', '、']]:
        return True
    if n > 3 and e['inside'][:3] in [f"{i}{l}" for i in range(10, 50) for l in ['.', '、']]:
        return True
    if n > 2 and e['inside'][:2] in [f"{i}{l}" for i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for l in ['.', '、']]:
        return True
    return False


def ToTopic(path, data, level_set, tokenizer):
    with open(path, "w", encoding="utf-8") as f:
        topic_dict = {"level": "", "n": "", "content": ""}
        for d in data:
            if d['type'] != 'text':
                continue
            if d['inside'] in level_set:
                topic_dict["content"] = topic_dict["content"].replace('\n', '')
                new_text = ''
                n = 0
                for text in topic_dict["content"]:
                    new_text += text
                    if text[-1] in ['.', '!', '?', '。', '！', '？', '…', ';', '；', ':', '：', '”', '’', '）', '】', '》', '」',
                                    '』', '〕', '〉', '》', '〗', '〞', '〟', '»', '"', "'", ')', ']', '}']:
                        input_tokens = tokenizer(new_text)
                        new_text = new_text.replace(' ', '')
                        if len(input_tokens['input_ids']) > 256:
                            # print("too long")
                            f.write(new_text[:200])
                            f.write('\n')
                            f.write(new_text[200:])
                            f.write('\n')
                            new_text = ''
                        elif len(input_tokens['input_ids']) > 150:
                            f.write(new_text)
                            f.write('\n')
                            new_text = ''

                topic_dict = {"level": "", "content": ""}
                topic_dict['level'] = d['inside']
            else:
                topic_dict["content"] += " " + d['inside']


if __name__ == "__main__":
    base_tokenizer_model = 'D:\\code\\llm\\embeding\\text2vec-base-chinese-paraphrase'
    tokenizer = AutoTokenizer.from_pretrained(base_tokenizer_model)

    file_names = glob.glob(TXT_DIRECTORY + '/*')
    file_names = [name for name in file_names if "txt.txt" not in name]

    n, error_list = 0, []
    for i, file_name in enumerate(file_names):
        try:
            data = read_data(file_name)
            level = [e for e in data if is_title(e)]
            level_set = set([e['inside'] for e in level])
            path = os.path.join(VEC_DIRECTORY, os.path.basename(file_name))
            ToTopic(path, data, level_set, tokenizer)
        except:
            n += 1
            error_list.append(file_name)
            print("No.{:7d} {} cannot be read".format(
                i, os.path.basename(file_name)))
