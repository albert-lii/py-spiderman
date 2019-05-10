# -*- coding: utf-8 -*-

"""
一个简单的爬虫示例，爬虫大致流程如下：
1. 向目标 url 发送请求
2. 获取请求的响应内容
3. 解析响应内容
4. 保存解析后的数据
"""

import os
import requests
from datetime import datetime
from lxml import etree


class SimpleSpider:
    """封装爬虫方法的类"""

    def __get_target_response(self, target):
        """
        发送请求，获取响应内容

        :param target(str): 目标网页链接
        """
        # 向目标 url 发送一个 get 请求，返回一个 response 对象
        res = requests.get(target)
        # 返回目标 url 的网页 html 文本
        return res.text

    def __parse_html(self, res):
        """
        解析响应内容，使用 XPath 解析 html 文本，并保存

        :param res(str): 目标网页的 html 文本
        """
        # 初始化生成一个 XPath 解析对象，获取 html 内容元素
        dom = etree.HTML(res)
        # 获取 h1 标签中的文字内容，其中 dom.xpath('//h1/text()')返回的是数组，提取一个元素
        title = dom.xpath('//h1/text()')[0]
        # 获取 class="theDate" 的 li 标签中的文字内容
        date = dom.xpath('//li[@class="theDate"]/text()')[0]
        # 获取 rel="author" 的 a 标签中的文字内容
        author = dom.xpath('//a[@rel="author"]/strong/text()')[0]
        # 获取 rel="author" 的 a 标签中的 href 属性内容
        author_link = 'https://www.archdaily.cn/' + dom.xpath('//a[@rel="author"]/@href')[0]
        # 获取 article 标签下的所有不含属性的 p 标签元素
        p_arr = dom.xpath('//article/p[not(@*)]')
        # 创建一个数组用于存储文章中的段落文本
        paragraphs = []
        # 遍历 p 标签数组
        for p in p_arr:
            # 提取 p 标签下的所有文本内容
            p_txt = p.xpath('string(.)')
            if p_txt.strip() != '':
                paragraphs.append(p_txt)
        paragraphs = paragraphs
        # 将数据保存到 beginner 下的 txt 文件中，如果文件不存在会自动创建
        with open('{}/first{}.txt'.format(os.getcwd(), datetime.now().strftime('%Y%m%d%H%M%S')), 'w') as ft:
            ft.write('标题：{}\n'.format(title))
            ft.write('时间：{}\n'.format(date))
            ft.write('作者：{}（{}）\n\n'.format(author, author_link))
            ft.write('正文：\n')
            for txt in paragraphs:
                ft.write(txt + '\n\n')

    def crawl_web_content(self, target):
        """
        爬虫执行方法

        :param target(str): 目标网页链接
        """
        res = self.__get_target_response(target)
        self.__parse_html(res)


##########################################################
# 执行爬虫
##########################################################
if __name__ == '__main__':
    url = 'https://www.archdaily.cn/cn/915495/luo-shan-ji-guo-ji-ji-chang-xin-lu-ke-jie-yun-xi-tong-yi-dong-gong'
    spider = SimpleSpider()
    # spider.crawl_web_content(url)
    help(spider)

