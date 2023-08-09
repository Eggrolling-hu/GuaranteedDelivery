# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from opencc import OpenCC

import os

# 初始化转换器，s2t表示简体转繁体，t2s表示繁体转简体
cc = OpenCC('t2s')

WTHITE_LIST = [
    "销售费用", "流动比率", "三费比重", "现金及现金等价物", "利息收入", "综合收益总额", "财务费用率",
    "货币资金增长率", "营业利润率", "研发经费与营业收入比值", "公司网址", "总负债增长率", "证券代码", "所得税费用",
    "法定代表人", "应收款项融资", "管理费", "流动负债", "固定资产", "职工薪酬", "投资收益", "净利润", "营业成本",
    "营业税金及附加", "研发人员", "职工人数", "无形资产", "衍生金融资产", "博士及以上人数", "企业名称",
    "收回投资收到的现金", "净利润增长率", "研发费用", "研发经费", "办公地址", "速动比率", "公允价值变动收益",
    "技术人员", "利润总额", "无形资产增长率", "每股经营现金流量", "职工总数", "电子信箱", "环境信息", "外文名称",
    "社会责任", "核心竞争力", "重大关联交易", "硕士及以上人员", "利息支出", "毛利率", "证券简称", "净资产",
    "资产负债比率",
]


class WikiPipeline:
    def process_item(self, item, spider):
        data = dict(item)
        self.writeFile(data)
        return item

    def writeFile(self, data):
        # print('========',len(data),'=========')
        if not os.path.exists('./data'):
            os.mkdir('./data')

        cc_content_entity = cc.convert(str(data['content_entity']))
        cc_category = cc.convert(str(data['category']))
        cc_text = cc.convert(str(data['text']))
        cc_url = cc.convert(str(data['url']))

        is_relative = False
        for e in WTHITE_LIST:
            if e in cc_text:
                is_relative = True
        if not is_relative:
            return

        file_name = os.path.join(
            './data/', "{}.txt".format(cc_content_entity))

        with open(file_name, 'w', encoding='utf-8') as fw:
            fw.write('wiki 标题： {}\n'.format(cc_content_entity))
            fw.write('wiki 分类： {}\n'.format(cc_category))
            fw.write('wiki 网址： {}\n'.format(cc_url))
            fw.write('crawl时间： {}\n'.format(data['time']))

            formatted_text = str(cc_text).replace(' ', '')
            fw.write('text 内容： {}\n\n'.format(formatted_text))

            # HTML
            fw.write(data['content'])
