from jieba import analyse
import requests
import re
import json
import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from hashlib import md5
import pymysql


class WySpider:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'
    }
    date = '2023-1-20'

    def __init__(self):
        self.wy_list = []  # 网易信息表
        self.author_list = []  # 作者信息表
        self.essay_list = []  # 文章信息表
        self.key_list = []

    @staticmethod
    def get_essay(text1):
        # print(html1.text)#//*[@id="content"]/div[2]
        patten = re.compile(
            '<div class="post_body">.*?<!-- 相关 -->|<div class="post_body">.*?</div>|<div class="article-details">.*?</div>',
            re.S | re.M)
        results = re.findall(patten, text1)
        # patten4 = re.compile('<.*?>', re.S | re.M)
        patten4 = re.compile(r'''<script.*?>.*?</script>|<style>.*?</style>|<.*?>''', re.S | re.M)
        if len(results) > 0:
            results0 = re.findall(patten4, results[0])
            str1 = results[0]
            str1 = str1.replace('  ', '')
            for j in range(0, len(results0)):
                str1 = str1.replace(results0[j], '')
            str1 = str1.replace('\n', '')
            str1 = str1.replace('\t', '')
            str1 = str1.replace('\r', '')
            # str1 = str1.replace('\n\n', '')
            return str1
        else:
            return " "

    def get_author_ip(self, url0):
        # print(url0)
        html1 = requests.get(url0, headers=self.headers)
        soup = BeautifulSoup(html1.text, 'lxml')
        string = soup.find('div', class_='icon_line iplocation')
        if string is not None:
            return string.text
        else:
            return ''

    def get_author(self, text1):
        # print("author")
        author = ['无', '作者未知', 0, '', "", 0]
        soup = BeautifulSoup(text1, 'lxml')
        string = soup.find('a', class_='post_side_logo_name')
        if string is None:
            string = soup.find('span', class_='text')
            if string is None:
                string = soup.find('div', class_='post_wemedia_title')
                if string is None:
                    if author not in self.author_list:
                        author1 = author[1:]
                        author1.append('网易')
                        self.author_list.append(author1)
                    return author
                author[-2] = string.a.text
                string1 = soup.find('span', class_='post_wemedia_info1')
                author[2] = string1.a.text
                string2 = soup.find('span', class_='post_wemedia_info2')
                author[-1] = string2.a.text
                string = soup.find('div', class_='post_wemedia_name')
                author[0] = string.a.attrs['href']
                author[1] = string.a.text
                author[-3] = self.get_author_ip(author[0])
            else:
                author[1] = string.text
        else:
            author[0] = string.attrs['href']
            author[1] = string.text
        if author not in self.author_list:
            author1 = author[1:]
            author1.append('网易')
            self.author_list.append(author1)
        return author

    def get_comment_count(self, text1):
        count = 0
        url = 'https://comment.tie.163.com/'
        patten = re.compile(''' *var config = {
 *"productKey": ".*?",
 *"docId": "(.*?)",''')
        results = re.findall(patten, text1)
        # print(results)
        url = url + results[0] + '.html'
        # print(url)
        html1 = requests.get(url, headers=self.headers).text
        patten1 = re.compile('''"cmtCount":(.*?),''')
        results = re.findall(patten1, html1)
        if len(results) != 0:
            # print(results)
            count = int(results[0])
        # print(count)
        return count

    def get_info(self, text1):
        info = [0, self.date, 'ip未知']
        soup = BeautifulSoup(text1, 'lxml')
        string = soup.find('div', class_='post_info')
        if string is not None:
            # print(string)
            string = string.text
            string = string.replace('	', '')
            string = string.replace('举报', '')
            patten1 = re.compile(
                '(2.*?) ')
            patten2 = re.compile(
                '''\n([\u4E00-\u9FA5]+)''')
            results = re.findall(patten1, string)
            results += re.findall(patten2, string)
            # print(results)
            if results is not None:
                info[1] = results[0]
                info[2] = results[-1]
        # url = soup.find('a', class_='post_top_tie_count js-tielink js-tiejoincount')
        # print('url:', url)
        info[0] = self.get_comment_count(text1)
        return info

# title author source word_count type comment_count publish_time keyword keyword_count publish_address article_link
    def into_page(self, url0, title):
        html1 = requests.get(url0, headers=self.headers)
        if html1.status_code == 200:
            text1 = html1.text.replace('  ', '')
            str1 = self.get_essay(text1)
            # print('字数', len(str1))
            keywords = analyse.extract_tags(str1, topK=1, withWeight=False)
            if len(keywords) != 0:
                keyword = keywords[0]  # 关键字
                amount = str1.count(keyword)  # 关键字出现次数
            else:
                keywords = analyse.extract_tags(title, topK=1, withWeight=False)
                keyword = keywords[0]  # 关键字
                amount = title.count(keyword)  # 关键字出现次数
            author = self.get_author(text1)
            if author[0] != '无':
                info = self.get_info(text1)
            else:
                info = [0, self.date, 'ip未知']
        l0 = [title, author[1], '网易', len(str1), self.wy_list[-1][0], info[0], info[1], keyword, amount, info[2], url0]
        self.essay_list.append(l0)

    def keys(self):
        for i in range(len(self.essay_list)):
            key0 = [self.essay_list[i][7], 0, 0]
            self.key_list.append(key0)

    # |<ul class="cm_ul_round">.*?</ul>
    def run(self):
        url = 'https://www.163.com/'
        html = requests.get(url, headers=self.headers)
        text = html.text.replace('  ', '')
        # print(text)
        patten1 = re.compile(
            r'''<ul class="tab_nav[ tab_nav3]* clearfix">\n<li ne-role="tab-nav" class="tagname icon.*?</ul>|
<ul class="cm_ul_round ul_page1">.*?</ul>''',
            re.S | re.M)
        results1 = re.findall(patten1, text)
        # print(results)
        results2 = []
        patten2 = re.compile(
            r'''href="(.*?)">(.*?)<''',
            re.S | re.M)
        for result in results1:
            # print(result)
            results2 += (re.findall(patten2, result))
        i = 0
        while i < len(results2):
            if ' ' in results2[i][0] or (
                    ('clickfrom' not in results2[i][0]) and (len(results2[i][0]) > 30)) or 'special' in results2[i][0]:
                del results2[i]
                i = i - 1
            i += 1
        # print(len(results2))
        flag = True
        for i in range(0, len(results2)):
            if len(results2[i][1]) > 4:
                flag = True
                if self.wy_list[-1][3] == '':
                    self.wy_list[-1][3] = '无'
                self.into_page(results2[i][0], results2[i][1])
            else:
                if flag:
                    self.wy_list.append([results2[i][1], 0, results2[i][0], ''])
                    flag = False
                else:
                    if self.wy_list[-1][3] != '':
                        self.wy_list[-1][3] += '/'
                    self.wy_list[-1][3] += results2[i][1]
        # time.sleep(1)
        self.keys()
        return self.wy_list, self.key_list, self.author_list, self.essay_list


if __name__ == '__main__':
    w = WySpider()
    a, b, c, d = w.run()
    print(a)
    print(b)
    print(c)
    print(d)
