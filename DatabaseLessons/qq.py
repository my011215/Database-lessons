# -*- coding = utf-8 -*-
# Author:Lucinda
# @Software: PyCharm
# @Email: txdforever58@163.com
import threading
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import os
import time
import re
import qq_article
import datetime


'''
1.相对路径问题
2.谷歌浏览器驱动版本对应问题
3.管理员权限问题
4.path添加问题

5.清洗数据的核验问题
6.默认时间的应该返回什么值
7.其他都是默认值为无吗

优化：
1.访问次数减少
2.直接无图模式不可以 
3.尝试拼接作者id创造链接并且用无图模式访问
4.多开网站预先加载，切换句柄进行读取

# js两种语句无法解决 模拟键盘无法解决 正则表达式匹配
'''

# lock = threading.Lock()

class QQSpider:
    _data = []
    _article_link = []
    _key_list = []
    _author_link = []

    _article_tmp = []
    _author_link_tmp = []
    _key_list_tmp = []

    _article = []
    _author = []
    _author_list = []


    def __init__(self):
        self._nowaupg = None
        self._nowartpg = None
        self._driver = self.load_chrome_driver()
        self._driver.implicitly_wait(3)

    @staticmethod
    def if_el_exist(wd, xpath):
        flag = True
        try:
            wd.find_element(By.XPATH, xpath)
            return flag
        finally:
            flag = False
            return flag

    # 所有作者
    def deal_author(self):
        remain = len(self._author_link)
        i = 0
        while remain - 40 > 0:
            remain -= 40
            self.author_change_read(i, 40, remain)
            i = i + 40
        if remain:
            self.author_change_read(i, remain, remain)

    # 切换作者
    def author_change_read(self, num, step, remain):
        self._driver = self.load_chrome_driver()
        self._nowaupg = qq_article.Article(self._driver)

        c = datetime.datetime.now()
        print(c.hour, c.minute, c.second)

        # 放入第一个作者链接
        print(self._author_link[num])
        self._driver.get(self._author_link[num])

        if remain > 1:
            # 剩下的作者链接
            for ii in range(num + 1, num + step):
                self._driver.execute_script("window.open('" + self._author_link[ii] + "')")
            time.sleep(10)

            # 切换句柄执行
            handles = self._driver.window_handles
            for ii in range(0, step):
                self._driver.switch_to.window(handles[ii])
                self.deal_one_author()

            self._driver.close()
            time.sleep(0.2)
        else:
            self.deal_one_author()
            self._driver.close()

    # 单页作者
    def deal_one_author(self):
        name = '无'
        intro = '无'
        ip = '无'

        # 定位名字
        n = self._driver.find_elements(By.XPATH, '//div[@class="author-name"]')
        if n:
            for nn in n:
                name = nn.get_attribute("innerText")

        if name == '无':
            pass

        else:
            # 定位介绍
            i = self._driver.find_elements(By.XPATH, '//div[@class="author-intro"]')
            if i:
                for ii in i:
                    intro = ii.get_attribute("innerText")

            # 定位ip
            p = self._driver.find_elements(By.XPATH, '//div[@class="IPInfo"]')
            if p:
                for pp in p:
                    ip = pp.get_attribute("innerText")
                    ip = ip.replace("IP属地：", '')

            self._author_list.append([name, 0, ip, intro, 0, '腾讯'])
            # print([name, 0, ip, intro, 0, '腾讯'])

    # 所有文章/多进程/数据共享
    # 1.内部函数的变量需要独立
    # 2.都需要有返回值放到最终的函数里面，再放到爬虫本身的东西里面
    def deal_article(self, start, end, index):
        remain = end - start
        print(threading.currentThread().ident, "剩下:", str(remain))
        i = start
        while remain - 40 > 0:
            remain -= 40
            self.page_change_read(i, 40, remain, index)
            i = i + 40

        self.page_change_read(i, remain, remain, index)
        # 返回在内部根据索引完成

    # 切换文章页
    def page_change_read(self, num, step, remain, d):

        driver = self.load_chrome_driver()
        nowartpg = qq_article.Article(driver)

        c = datetime.datetime.now()
        print(c.hour, c.minute, c.second)

        driver.get(self._article_link[num][3])
        hand = []
        hand.append(driver.window_handles[0])

        if remain > 1:

            for ii in range(num + 1, num + step):
                driver.execute_script("window.open('" + self._article_link[ii][3] + "')")
                handle = driver.window_handles
                # 这里怎样获得最新的选项卡
                hand.append(handle[-1])

            time.sleep(5)
            # 打印当前句柄标题
            for i in hand:
                print(i)

            # 切换句柄执行
            # handles = driver.window_handles
            # print(len(handles))
            for ii in range(0, step):
                driver.switch_to.window(hand[ii])

                # # print("第几个", ii)
                # # print("句柄", self._hand[ii])
                # print("当前句柄url:", driver.current_url)
                # print("句柄标题", driver.title)

                # print(self._article_link[num+ii])

                # 这里需要一个返回值
                self._article_tmp[d].append(self.deal_one_article(self._article_link[num + ii], nowartpg, d))

            driver.quit()
            time.sleep(0.2)
        else:
            # 这里需要一个返回值

            self._article_tmp[d].append(self.deal_one_article(self._article_link[num], nowartpg, d))
            driver.quit()

    # 单页文章
    def deal_one_article(self, ar, nowartpg, d):

        # 标题 作者 来源 字数* 子版块 评论数* 时间* 关键字* 关键字出现次数* 发布地址* 文章链接
        nowartpg.init_article_web()

        # 作者
        author = nowartpg.get_author()
        ar.insert(1, author)

        # 时间
        pubtime = nowartpg.get_time()

        # 发布地址(不一定有)
        space = nowartpg.get_sp()

        # 文章字数 文章关键字 文章关键词出现次数
        count, key, key_times = nowartpg.get_three()

        # 评论数
        comment_count = nowartpg.get_comment_count()

        # 作者链接
        ak = nowartpg.get_authork()
        if ak:
            self._author_link_tmp[d].append(ak)


        ar.insert(3, count)
        ar.insert(-1, comment_count)
        ar.insert(-1, pubtime)
        ar.insert(-1, key)
        ar.insert(-1, key_times)
        ar.insert(-1, space)

        # key 列表处理
        if key == '无':
            pass
        else:
            tmp = []
            tmp.append(key)
            tmp.append(0)
            tmp.append(0)
            self._key_list_tmp[d].append(tmp)

        print(ar)
        return ar

    # 洗文章链接
    def wash_article_link(self, arti):

        # 去除不符合规范网站
        temp = []

        for ar in arti:
            length = self.find_content(r"^https://new.qq.com/", ar[3])
            if length:
                temp.append(ar)

        return temp

    # 测试
    @staticmethod
    def print_result(d):
        for i in d:
            print(i, end='\n')
        print("******************************************")

    # 采用这种方法就不用重新补http的数据了
    @staticmethod
    def get_a(el):

        text1 = el.get_attribute("text")
        text1 = text1.replace(' ', '').replace('\n', '')
        text2 = el.get_attribute("href")
        tmp = []
        if text1 != '':
            tmp.append(text1)
            tmp.append(text2)
        return tmp

    # 匹配
    @staticmethod
    def find_content(pa, words):

        pattern = re.compile(pa)
        return pattern.findall(words)

    # 特殊小板块处理
    def deal_spe_box(self, elements, data, artk):

        # 获取特殊板块
        tt = elements.find_elements(By.XPATH, ".//div[@class='bd']")
        smallel = elements.find_elements(By.XPATH, ".//h2")

        a = 0
        # 获取特殊板块标题和链接
        for e in smallel:
            a += 1
            tmp = []
            if a == 5:
                tmp.append('从何说起')
            elif e.text == '':
                continue
            else:
                # 特殊板块小标题获取
                tmp.append(e.text)

            # 设置板块初始数，利用sql统计就好
            tmp.append(0)

            # 链接的获取
            links = e.find_elements(By.XPATH, ".//a")
            for link in links:
                li = link.get_attribute("href")
                res = self.find_content('^http', str(li))
                if len(res) > 0:
                    tmp.append(li)
                else:
                    tmp.append("无")

            data.append(tmp)

        # 对每个bd进行处理
        a = 0
        for t in tt:
            datatmp = data[a]
            cc = t.find_elements(By.XPATH, ".//a")
            # print(len(cc))

            # 子标题 文章标题 文章连接处理
            # 获取内部html用正则表达式进行匹配
            sub = ''
            for c in cc:
                # 筛选不显示部分
                # 动态更新玩我是吧
                # if c.is_displayed():

                html = c.get_attribute("outerHTML")

                # 获取a链接
                text1 = self.find_content(r"<a .*?>(.*?)</a>", str(html))

                # 筛子标题
                if len(text1) > 0:
                    text = self.find_content(r".cate.", str(html))

                    # 子标题处理
                    if len(text) > 0:
                        stradd = lambda x, y, z: x + y + z
                        for tex in text1:
                            sub = stradd(sub, tex, '/')

                    else:
                        # 链接
                        text2 = self.find_content(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(html))
                        artitmp = []

                        # 列表转字符串
                        artitmp.append(text1[0])
                        artitmp.append(text2[0])

                        # 加上该板块的名字
                        artitmp.insert(1, datatmp[0])
                        artk.append(artitmp)

            if len(sub) > 0:
                data[a].append(sub)
            else:
                data[a].append('无')
            a += 1

        # print(data[0][0])

        return data, artk

    # 一般小板块处理
    def deal_normal_box(self, element, data, artk):

        # 存在需要动态拉动的问题,否则无法显示对应内容
        a_list = element.find_elements(By.XPATH, ".//a")

        now_name = ''
        # 把每个a元素扔进去处理了
        for a in a_list:
            name = a.get_attribute("class")
            # 标题处理

            tmp = self.get_a(a)
            if len(tmp) == 0:
                continue
            # 分离标题和文章链接
            elif name == "txt active":
                data.append(tmp)
                data[-1].insert(1, 0)
                now_name = tmp[0]
                data[-1].append('无')
            # 文章处理
            else:
                tmp.insert(1, now_name)  # 来源板块
                artk.append(tmp)

        return data, artk

    # 子版块处理
    def deal_box(self, elements, data, article_k):

        data = []
        article_k = []
        for el in elements:
            classname = el.get_attribute('class')

            # 特殊小板块的处理
            if classname == 'layout qq-main cf':
                data, article_k = self.deal_spe_box(el, data, article_k)
            # 一般小板块处理
            elif 'channel' in classname:
                data, article_k = self.deal_normal_box(el, data, article_k)

        for b in article_k:
            b.insert(1, '腾讯')

        # 清洗文章数据只爬文章
        article_k = self.wash_article_link(article_k)

        return data, article_k

    # 主网页初始化
    @staticmethod
    def init_web(driver, url, js):

        driver.maximize_window()

        driver.get(url)

        time.sleep(2)

        driver.execute_script(js)

        time.sleep(2)

    # 驱动加载
    @staticmethod
    def load_chrome_driver():

        if 'nt' == os.name:
            # 驱动相对路径设置
            relapath = os.path.join(os.path.abspath('.'), 'driver', 'chromedriver.exe')
            # print(relapath)
            os.environ['webdriver.chrome.driver'] = relapath

            options = webdriver.ChromeOptions()
            '''options.add_argument("start-maximized")
            options.add_argument("--auto-open-devtools-for-tabs")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)'''
            options.add_experimental_option('excludeSwitches', ['enable-logging'])

            # options.add_argument('--headless')

            options.add_argument('--disable-gpu')  # 禁用GPU加速

            options.page_load_strategy = "none"
            prefs = {"profile.managed_default_content_settings.images": 2}  # 设置无图模式
            options.add_experimental_option("prefs", prefs)  # 加载无图模式设置

            # 启动Chrome浏览器
            # 怎么会突然启动失败
            return webdriver.Chrome(service=Service(relapath), options=options)
            # return webdriver.Chrome(service=Service(r'E:\code python\crawler\driver\chromedriver.exe'),
            #                           options=options)
            # return webdriver.Chrome(options=options)

    # 获取所需的子版块列表
    def get_qq_title(self):

        # 网页初始化的操作
        self.init_web(self._driver, 'https://www.qq.com/',
                      "window.scrollTo(0, document.body.scrollHeight)")
        # "window.onload=function(){var q=document.documentElement.scrollTop=30000}"

        # 子版块元素行获取
        elements = self._driver.find_elements(By.XPATH, "/html/body/div[1]/div")

        # 处理子版块
        self._data, self._article_link = self.deal_box(elements, self._data, self._article_link)

        self._driver.quit()

        return self._data

    # 获取文章信息列表/多线程/数据共享
    def get_article_info(self):

        # 每个进程处理100个文章
        thead_list = []

        left = len(self._article_link)
        print("left", left)
        i = 0
        d = 0

        while left - 100 > 0:
            p = Thread(target=self.deal_article, args=(i, i + 100, d))
            p.start()
            thead_list.append(p)
            self._article_tmp.append([])
            self._author_link_tmp.append([])
            self._key_list_tmp.append([])
            i = i + 100
            left = left - 100
            d = d + 1

        if  left > 0 :
            p = Thread(target=self.deal_article, args=(i, i + left, d))
            p.start()
            thead_list.append(p)
            self._article_tmp.append([])
            self._author_link_tmp.append([])
            self._key_list_tmp.append([])

        print("thread_list", len(thead_list))
        for p in thead_list:
            p.join()
            time.sleep(3)

        for s in self._article_tmp:
            for ss in s:
                self._article.append(ss)
        return self._article

    # 获取关键字列表
    def get_key_list(self):
        for s in self._key_list_tmp:
            for ss in s:
                self._key_list.append(ss)
        return self._key_list

    # 获取作者信息列表
    def get_author_info(self):
        for s in self._author_link_tmp:
            for ss in s:
                self._author_link.append(ss)
        self.deal_author()
        return self._author_list

    def run(self):
        qq_list = self.get_qq_title()
        article_list = self.get_article_info()
        key_list = self.get_key_list()
        author_list = self.get_author_info()
        key_list.append(['无', 0, 0])
        author_list.append(['无', 0, ' ', ' ', 0, '腾讯'])
        for i in range(len(article_list)):
            flag = False
            for j in range(len(author_list)):
                if article_list[i][1] == author_list[j][0]:
                    flag = True
                    break
            if not flag:
                author_list.append([f'{article_list[i][1]}', 0, ' ', ' ', 0, '腾讯'])
        return qq_list, key_list, author_list, article_list


if __name__ == '__main__':
    a = QQSpider()
    a.get_qq_title()
    a.get_article_info()
    a.get_key_list()
    a.get_author_info()
