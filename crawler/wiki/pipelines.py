# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
from opencc import OpenCC

# 初始化转换器，s2t表示简体转繁体，t2s表示繁体转简体
cc = OpenCC('t2s')


class WikiPipeline:
    def process_item(self, item, spider):
        data = dict(item)
        self.writeFile(data)
        return item

    def writeFile(self, data):
        # print('========',len(data),'=========')
        if not os.path.exists('./data'):
            os.mkdir('./data')

        file_name = os.path.join(
            './data/', "{}.txt".format(data['content_entity']))
        with open(file_name, 'w', encoding='utf-8') as fw:
            fw.write('wiki标题： {}\n'.format(
                cc.convert(str(data['content_entity']))))
            fw.write('wiki分类： {}\n'.format(cc.convert(str(data['category']))))
            fw.write('原文地址： {}\n'.format(cc.convert(str(data['url']))))
            fw.write('爬取时间： {}\n'.format(data['time']))

            cc_text = cc.convert(str(data['text']))
            formatted_text = str(cc_text).replace(' ', '')
            fw.write('文字内容： {}\n\n'.format(formatted_text))
            # HTML
            fw.write(data['content'])
