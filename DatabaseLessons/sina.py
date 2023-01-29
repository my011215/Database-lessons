import requests
import logging
import os
import re
import bs4
import lxml
from bs4 import BeautifulSoup
import urllib
import chardet
import pymysql
from jieba import analyse


class SinaSpider:
    key_list = []
    author_list = []
    article_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'
    }

    # 新浪表
    @staticmethod
    def get_title(url_list):
        title1_list = []
        child_title_list = []
        title_link = ['https://sports.sina.com.cn/',
                      'https://auto.sina.com.cn/',
                      'https://ent.sina.com.cn/',
                      'https://finance.sina.com.cn/',
                      'https://mil.news.sina.com.cn/',
                      'https://book.sina.com.cn/',
                      'https://tech.sina.com.cn/',
                      'https://digi.sina.com.cn/',
                      'https://games.sina.com.cn/',
                      'https://edu.sina.com.cn/',
                      'https://baby.sina.com.cn/',
                      'https://fashion.sina.com.cn/',
                      'https://golf.sina.com.cn/',
                      'https://travel.sina.com.cn/',
                      'https://travel.sina.cn/search/',
                      'https://vr.sina.com.cn/',
                      'https://news.sina.com.cn/'
                      ]
        for i in range(0, len(url_list)):
            ex = r'<div class="order-menu clearfix SC_Order_Fix_Menu">(.*?)</div>'
            title1_list.extend(re.findall(ex, url_list[i], re.S))
        for i in range(0, len(title1_list)):
            ex = r'<.*?>'
            title2_list = re.findall(ex, title1_list[i], re.S)
            for j in range(0, len(title2_list)):
                title1_list[i] = (title1_list[i].replace(title2_list[j], ''))
        for i in range(0, len(title1_list)):
            title1_list[i] = title1_list[i].replace(' ', '')
            title1_list[i] = title1_list[i].replace('\n', '')
            title1_list[i] = title1_list[i].replace('\t', '')
        title1_list.remove('商讯')
        title1_list.remove('好物')
        title1_list.remove('女性情感')
        title1_list.remove('房产二手房家居')
        title1_list.remove('世相')
        for i in range(0, len(title1_list)):
            child_title_list.extend('无')
        for i in range(0, len(title1_list)):
            if title1_list[i] == '体育':
                child_title_list[i] = '无'
            elif title1_list[i] == '汽车购车找车':
                child_title_list[i] = r'购车/找车'
                title1_list[i] = '汽车'
            elif title1_list[i] == '娱乐娱乐视频':
                child_title_list[i] = r'娱乐/视频'
                title1_list[i] = '娱乐'
            elif title1_list[i] == '财经股票理财':
                child_title_list[i] = r'股票/理财'
                title1_list[i] = '财经'
            elif title1_list[i] == '军事':
                child_title_list[i] = '无'
            elif title1_list[i] == '读书小说':
                child_title_list[i] = '小说'
                title1_list[i] = '读书'
            elif title1_list[i] == '科技车研所':
                child_title_list[i] = '车研所'
                title1_list[i] = '科技'
            elif title1_list[i] == '数码众测':
                child_title_list[i] = '众测'
                title1_list[i] = '数码'
            elif title1_list[i] == '游戏电竞':
                child_title_list[i] = '电竞'
                title1_list[i] = '游戏'
            elif title1_list[i] == '教育':
                child_title_list[i] = '无'
                title1_list[i] = '教育'
            elif title1_list[i] == '育儿':
                child_title_list[i] = '无'
                title1_list[i] = '育儿'
            elif title1_list[i] == '时尚视觉':
                child_title_list[i] = '视觉'
                title1_list[i] = '时尚'
            elif title1_list[i] == '旅游热门':
                child_title_list[i] = '热门'
                title1_list[i] = '旅游'
            elif title1_list[i] == '高尔夫':
                child_title_list[i] = '无'
                title1_list[i] = '高尔夫'
            elif title1_list[i] == 'VR':
                child_title_list[i] = '无'
                title1_list[i] = 'VR'
            elif title1_list[i] == '热榜':
                child_title_list[i] = '无'
                title1_list[i] = '热榜'
        array = []
        for i in range(0, len(title1_list)):
            array.append([])
            array[i].append(title1_list[i])
            array[i].append(0)
            array[i].append(title_link[i])
            array[i].append(child_title_list[i])
        return title1_list, array

    # 板块文章对应链接和文章名字
    def get_link(self, title1_list, url_list):
        link1_list = []
        for i in range(0, len(url_list)):
            url_list[i] = url_list[i].replace('\t', '')
        for i in range(0, len(url_list)):
            ex = r'<a target="_blank" href="(.*?)".*?>(.*?)</a>'
            link1_list.extend('0')
            link1_list.extend(re.findall(ex, url_list[i], re.S))
        j = 0
        x = -1
        for i in range(0, len(link1_list)):
            j = j + 1
            if link1_list[i] == '0' and x < 16:
                x = x + 1
                # print(title1_list[x])
                j = 0
            # else:
            # print(j, link1_list[i])
        return link1_list

    # 关键字表
    def get_key(self, title1_list, link_list):
        key_list = []
        if title1_list == '汽车购车找车':
            title1_list = '汽车'
        elif title1_list == '娱乐娱乐视频':
            title1_list = '娱乐'
        elif title1_list == '财经股票理财':
            title1_list = '财经'
        elif title1_list == '读书小说':
            title1_list = '读书'
        elif title1_list == '科技车研所':
            title1_list = '科技'
        elif title1_list == '数码众测':
            title1_list = '数码'
        elif title1_list == '潮流世相':
            title1_list = '潮流'
        elif title1_list == '游戏电竞':
            title1_list = '游戏'
        elif title1_list == '女性情感':
            title1_list = '女性'
        elif title1_list == '教育':
            title1_list = '教育'
        elif title1_list == '育儿':
            title1_list = '育儿'
        elif title1_list == '时尚视觉':
            title1_list = '时尚'
        elif title1_list == '旅游热门':
            title1_list = '旅游'
        elif title1_list == '高尔夫':
            title1_list = '高尔夫'
        elif title1_list == 'VR':
            title1_list = 'VR'
        html = requests.get(url=link_list, headers=self.headers, verify=False)
        ex1 = '''channel: '(.*?)',
        		newsid: '(.*?)','''
        ex2 = '''"count":{"total":(.*?),"show":(.*?),'''
        if html.status_code == 200:
            if link_list == 'http://dj.sina.com.cn/article/mcwiwst1986029.shtml' or link_list == 'http://roll.collection.sina.com.cn/collection/yjjj/index.shtml' or link_list == 'http://roll.collection.sina.com.cn/collection/cjrw/index.shtml' or link_list == 'http://dj.sina.com.cn/article/mxzuhrv8941277.shtml':
                page_text = html.text
            else:
                page_text = html.text.encode('iso-8859-1').decode('utf-8')
            soup = BeautifulSoup(page_text, 'lxml')
            string = soup.find('div', class_='article')
            string1 = soup.find('div', class_='date-source')
            if link_list == 'http://roll.collection.sina.com.cn/collection/yjjj/index.shtml' or link_list == 'https://auto.sina.com.cn/newcar/x/2023-01-09/detail-imxzraex8624119.shtml':
                string = None
            if string != None and string1 != None:
                str1 = soup.find('div', class_='article').text
                str1 = str1.replace('  ', '')
                str1 = str1.replace('\n', '')
                str1 = str1.replace('\t', '')
                # 关键字keyword
                keywords = analyse.extract_tags(str1, topK=1, withWeight=False)
                # print(keywords[0])
                if keywords[0] != None:
                    key_list.append(keywords[0])
                    key_list.append(0)
                    key_list.append(0)
                return key_list
        # 板块对应文章链接和文章名字
        # 作者表

    def get_author(self, title1_list, link_list):
        author_list = []
        if title1_list == '汽车购车找车':
            title1_list = '汽车'
        elif title1_list == '娱乐娱乐视频':
            title1_list = '娱乐'
        elif title1_list == '财经股票理财':
            title1_list = '财经'
        elif title1_list == '读书小说':
            title1_list = '读书'
        elif title1_list == '科技车研所':
            title1_list = '科技'
        elif title1_list == '数码众测':
            title1_list = '数码'
        elif title1_list == '潮流世相':
            title1_list = '潮流'
        elif title1_list == '游戏电竞':
            title1_list = '游戏'
        elif title1_list == '女性情感':
            title1_list = '女性'
        elif title1_list == '教育':
            title1_list = '教育'
        elif title1_list == '育儿':
            title1_list = '育儿'
        elif title1_list == '时尚视觉':
            title1_list = '时尚'
        elif title1_list == '旅游热门':
            title1_list = '旅游'
        elif title1_list == '高尔夫':
            title1_list = '高尔夫'
        elif title1_list == 'VR':
            title1_list = 'VR'
        html = requests.get(url=link_list, headers=self.headers, verify=False)
        ex1 = '''channel: '(.*?)',
                newsid: '(.*?)','''
        ex2 = '''"count":{"total":(.*?),"show":(.*?),'''
        if html.status_code == 200:
            if link_list == 'http://dj.sina.com.cn/article/mcwiwst1986029.shtml' or link_list == 'http://roll.collection.sina.com.cn/collection/yjjj/index.shtml' or link_list == 'http://roll.collection.sina.com.cn/collection/cjrw/index.shtml' or link_list == 'http://dj.sina.com.cn/article/mxzuhrv8941277.shtml':
                page_text = html.text
            else:
                page_text = html.text.encode('iso-8859-1').decode('utf-8')
            soup = BeautifulSoup(page_text, 'lxml')
            string = soup.find('div', class_='article')
            string1 = soup.find('div', class_='date-source')
            if link_list == 'http://roll.collection.sina.com.cn/collection/yjjj/index.shtml' or link_list == 'https://auto.sina.com.cn/newcar/x/2023-01-09/detail-imxzraex8624119.shtml':
                string = None
            if string != None and string1 != None:
                # 作者s1_list[2]
                s_list = (soup.find('div', class_='date-source').text)
                s1_list = s_list.split('\n')
                print(s1_list[2])
                if s1_list[2] != None:
                    author_list.append(s1_list[2])
                    author_list.append('0')
                    author_list.append(' ')
                    author_list.append(' ')
                    author_list.append('0')
                    author_list.append('新浪')
                return author_list

    # 文章表

    def get_article(self, title1_list, link_list, page_name):
        article_list = []
        if title1_list == '汽车购车找车':
            title1_list = '汽车'
        elif title1_list == '娱乐娱乐视频':
            title1_list = '娱乐'
        elif title1_list == '财经股票理财':
            title1_list = '财经'
        elif title1_list == '读书小说':
            title1_list = '读书'
        elif title1_list == '科技车研所':
            title1_list = '科技'
        elif title1_list == '数码众测':
            title1_list = '数码'
        elif title1_list == '潮流世相':
            title1_list = '潮流'
        elif title1_list == '游戏电竞':
            title1_list = '游戏'
        elif title1_list == '女性情感':
            title1_list = '女性'
        elif title1_list == '教育':
            title1_list == '教育'
        elif title1_list == '育儿':
            title1_list = '育儿'
        elif title1_list == '时尚视觉':
            title1_list = '时尚'
        elif title1_list == '旅游热门':
            title1_list = '旅游'
        elif title1_list == '高尔夫':
            title1_list = '高尔夫'
        elif title1_list == 'VR':
            title1_list = 'VR'
        html = requests.get(url=link_list, headers=self.headers, verify=False)
        ex1 = '''channel: '(.*?)',
    		newsid: '(.*?)','''
        ex2 = '''"count":{"total":(.*?),"show":(.*?),'''
        if html.status_code == 200:
            # print(html.status_code)
            if link_list == 'http://dj.sina.com.cn/article/mcwiwst1986029.shtml' or link_list == 'http://roll.collection.sina.com.cn/collection/yjjj/index.shtml' or link_list == 'http://roll.collection.sina.com.cn/collection/cjrw/index.shtml' or link_list == 'http://dj.sina.com.cn/article/mxzuhrv8941277.shtml':
                page_text = html.text
            else:
                page_text = html.text.encode('iso-8859-1').decode('utf-8')
            # print(page_text)
            soup = BeautifulSoup(page_text, 'lxml')
            string = soup.find('div', class_='article')
            string1 = soup.find('div', class_='date-source')
            if link_list == 'http://roll.collection.sina.com.cn/collection/yjjj/index.shtml' or link_list == 'https://auto.sina.com.cn/newcar/x/2023-01-09/detail-imxzraex8624119.shtml':
                string = None
            # print(string)
            if string != None and string1 != None:
                # print(soup.find('div', class_='article').text)
                str1 = soup.find('div', class_='article').text
                str1 = str1.replace('  ', '')
                str1 = str1.replace('\n', '')
                str1 = str1.replace('\t', '')
                # 板块名字
                print(title1_list)
                # 排序，文章链接
                # 文章内容
                # print(str1)
                # 文章时间s3和作者s1_list[2]
                s_list = soup.find('div', class_='date-source').text
                s1_list = s_list.split('\n')
                s2 = str(s1_list[1])
                s2 = s2.split(' ')
                s3 = s2[0]
                s3 = s3.replace('年', '-')
                s3 = s3.replace('月', '-')
                s3 = s3.replace('日', '')
                # 关键字keyword和关键字出现次数amount
                keywords = analyse.extract_tags(str1, topK=1, withWeight=False)
                print(keywords[0])
                keyword = keywords[0]
                print(type(keyword))
                print("关键词：", keyword)
                amount = str1.count(keyword)  # 关键字出现次数
                print("关键词次数：", amount)
                # #文章总字数
                all_count = len(str1)
                print('文章总字数：', all_count)

                # 评论数
                print(link_list)
                html1 = requests.get(url=link_list, headers=self.headers, verify=False)
                page_text1 = html1.text.encode('iso-8859-1').decode('utf-8')
                url1 = re.findall(ex1, page_text1, re.S)
                print(url1)
                if url1 != []:
                    u1 = url1[0][0]
                    u2 = url1[0][1]
                    link1 = 'https://comment5.news.sina.com.cn/page/info?format=json&channel=' + u1 + '&newsid=' + u2
                    print(link1)
                    html2 = requests.get(url=link1, headers=self.headers, verify=False)
                    page_text2 = html2.text
                    print(page_text2)
                    comments = re.findall(ex2, page_text2, re.S)
                    comments_num = comments[0][1]
                    if page_name == None:
                        page_name = 'None'
                    elif s1_list[2] == None:
                        s1_list[2] = 'None'
                    elif all_count == None:
                        all_count = 'None'
                    elif title1_list == None:
                        title1_list = 'None'
                    elif comments_num == None:
                        comments_num = 'None'
                    elif s3 == None:
                        s3 = 'None'
                    elif keyword == None:
                        keyword = 'None'
                    elif amount == None:
                        amount = 'None'
                    elif link_list == None:
                        link_list = 'None'
                    if keyword != None and s1_list[2] != None:
                        article_list.append(page_name)
                        article_list.append(s1_list[2])
                        article_list.append('新浪')
                        article_list.append(all_count)
                        article_list.append(title1_list)
                        article_list.append(comments_num)
                        article_list.append(s3)
                        article_list.append(keyword)
                        article_list.append(amount)
                        article_list.append(' ')
                        article_list.append(link_list)
                else:
                    comments = 0
                    if page_name is None:
                        page_name = 'None'
                    elif s1_list[2] is None:
                        s1_list[2] = 'None'
                    elif all_count is None:
                        all_count = 'None'
                    elif title1_list is None:
                        title1_list = 'None'
                    elif comments is None:
                        comments = 'None'
                    elif s3 is None:
                        s3 = 'None'
                    elif keyword is None:
                        keyword = 'None'
                    elif amount is None:
                        amount = 'None'
                    elif link_list is None:
                        link_list = 'None'
                    if keyword is not None and s1_list[2] is not None:
                        article_list.append(page_name)
                        article_list.append(s1_list[2])
                        article_list.append('新浪')
                        article_list.append(all_count)
                        article_list.append(title1_list)
                        article_list.append(comments)
                        article_list.append(s3)
                        article_list.append(keyword)
                        article_list.append(amount)
                        article_list.append(' ')
                        article_list.append(link_list)
        return article_list

    def run(self):
        # 爬取搜狐引擎搜索界面内容（get,UA绕过，代理绕过）
        # 当开了代理时候加上这句话
        os.environ['NO_PROXY'] = 'sina.com'
        logging.captureWarnings(True)
        url = 'https://www.sina.com.cn/'
        html = requests.get(url=url, headers=self.headers, verify=False)
        page_text = html.text.encode('iso-8859-1').decode('utf-8')
        ex = '<div class="SC_Order_Fix">(.*?)<!-- mod'
        url_list = re.findall(ex, page_text, re.S)
        # 板块主标题
        title1_list, sina_list = self.get_title(url_list)
        link1_list = self.get_link(title1_list, url_list)
        print(link1_list)
        # 链接对应文章内容
        html = requests.get(url='https://lottery.sina.com.cn/football/?from=ls', headers=self.headers, verify=False)
        s = -1
        for i in range(0, len(link1_list)):
            if link1_list[i] == '0' and s < 16:
                i = i + 1
                s = s + 1
            if '.shtml' in link1_list[i][0]:
                key0 = self.get_key(title1_list[s], link1_list[i][0])
                if key0:
                    self.key_list.append(key0)
                author0 = self.get_author(title1_list[s], link1_list[i][0])
                if author0:
                    self.author_list.append(author0)
                article0 = self.get_article(title1_list[s], link1_list[i][0], link1_list[i][1])
                if article0:
                    self.article_list.append(article0)
        return sina_list, self.key_list, self.author_list, self.article_list


if __name__ == '__main__':
    s = SinaSpider()
    a, b, c, d = s.run()
    print(a)
    print(b)
    print(c)
    print(d)
