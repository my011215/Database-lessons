# -*- coding = utf-8 -*-
# Author:Lucinda
# @Software: PyCharm
# @Email: txdforever58@163.com

import re
import time

from jieba import analyse
from selenium.webdriver.common.by import By


# 本来只是处理keycount部分 现在得处理所有部分
class Article:
    _content = ''
    _count = 0
    _flag = 0
    _key = '空'
    _html = ''
    _key_times = 0

    # url在init_article_web

    # 初始化
    def __init__(self, driver):
        self._driver = driver

    # 文章网页初始化
    def init_article_web(self):

        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        self.get_html()

    # 正则预处理
    def get_html(self):
        # 正则预处理
        el = self._driver.find_element(By.XPATH, '/html')
        self._html = el.get_attribute("outerHTML")

    @staticmethod
    def find_content(pa, words):
        pattern = re.compile(pa)
        return pattern.findall(words)

    def get_key_count(self):
        return self._count

    def get_key(self):
        return self._key

    def get_author(self):
        el = self._driver.find_elements(By.XPATH, '//a[@class="author"]')
        if el:
            for e in el:
                return e.get_attribute("innerText").replace("企鹅号", '')
        else:
            return "无"

    def get_time(self):
        li = self.find_content(r'"pubtime": "\d{4}-\d{1,2}-\d{1,2}', self._html)
        if li:
            pubtime = li[0].replace('"pubtime": "', '')
            return pubtime
        else:
            return "2023-01-20"

    def get_sp(self):
        el = self._driver.find_elements(By.XPATH, '//div[@class="IPInfo"]/div[2]')
        if el:
            for e in el:
                return e.get_attribute("innerText")
        else:
            return "无"

    @staticmethod
    def get_article_content(wd):

        content = ''
        eles = wd.find_elements(By.XPATH, '//p[@class="one-p"]')
        for el in eles:
            text = ''
            text = el.get_attribute("innerText")
            content = content + text

        return content

    def cut_and_count(self):
        if self._count:
            keywords = analyse.extract_tags(self._content, topK=1)
            if keywords:
                return keywords[0], self._content.count(keywords[0])
            else:
                return '无', 0
        else:
            return '无', 0

    def get_three(self):

        self._content = self.get_article_content(self._driver)

        self._count = len(self._content)

        # 分词统计
        self._key, self._key_times = self.cut_and_count()
        return self._count, self._key, self._key_times

    def get_comment_count(self):

        # 配一下所有的iframe
        iframe = self._driver.find_elements(By.XPATH, '//iframe[@class="commentIframe"]')
        # 有病s就行没s就不行
        for i in iframe:
            # print(i.get_attribute("outerHTML"))
            self._driver.switch_to.frame(i)
            el = self._driver.find_elements(By.XPATH, '//*[@id="J_CommentTotal"]')
            for e in el:
                num = e.get_attribute("innerText")
                if num:
                    if num == '--':
                        return 0
                    else:
                        return int(num)
                else:
                    return 0
            return 0
        return 0

    def get_authork(self):
        li = self.find_content(r'"media_id": "[0-9]+', self._html)
        if li:
            author = li[0].replace('"media_id": "', 'https://new.qq.com/omn/author/')
            print(author)
            return author
        else:
            return []