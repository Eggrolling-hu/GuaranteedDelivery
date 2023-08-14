from langchain import PromptTemplate

PROMPT = """
你需要扮演一位金融专家助手。回答下列问题。

要求：
1. 答案应简练、清晰、准确。
2. 仅使用与问题直接相关的额外信息进行回答。
3. 避免引入与问题无关的信息。

示例一：
问题：什么是价值投资？
价值投资是投资策略的一种，由班杰明·葛拉汉和大卫·多德（英语：DavidDodd）所提出。和价值投资法所对应的是成长投资法。其重点是透过基本面分析中的概念，例如高股息收益率、低市盈率（P/E，股价/每股净利润）和低市净率（P/B，股价/每股净资产），去寻找并投资于一些股价被低估的股票。

示例二：
问题：什么是营业利润？
营业利润（英语：OperatingIncome、OperatingProfit）或译营业利益是营业收入减除营业成本及营业费用后之余额。其为正数，表示本期营业盈余之数；其为负数，表示本期营业亏损之数。当一间公司没有营业外收入与营业外支出，有时营业利润与息税前利润被当作同义词。


现在开始：
问题：{query}
"""


def answer_open_question_raw_prompt():
    return PromptTemplate(template=PROMPT, input_variables=["query"])


def answer_open_question_prompt(query: str):
    P = PromptTemplate(template=PROMPT, input_variables=["query"])
    return P.format(query=query)


if __name__ == "__main__":
    print(answer_open_question_prompt("你们的装箱算法能不能用在家居业呀？主要用于是沙发的装箱。"))
