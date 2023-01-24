from qq import QQSpider
from sina import SinaSpider
from sql import SQL
from souhu import SouhuSpider
from wy import WySpider
s = SQL(user='root', host="127.0.0.1", password='', db='sjk',)


def website(web, i, li):
    sql = f'''INSERT INTO `sjk`.`{web}_information`(`id`, `type`, `article_number`, `link`, `child_plate`)
            VALUES ({i}, '{li[0]}', '{li[1]}', '{li[2]}', '{li[3]}')'''
    print(sql)
    db = s.conn()
    cursor = db.cursor()
    cursor.execute(sql)
    s.close(db)


def websites(sina_list, qq_list, souhu_list, wy_list):
    i = 0
    while i < len(sina_list):
        website('sina', str(i+1), sina_list[i])
        i += 1
    i = 0
    while i < len(qq_list):
        website('qq', str(i+1), qq_list[i])
        i += 1
    i = 0
    while i < len(souhu_list):
        website('souhu', str(i+1), souhu_list[i])
        i += 1
    i = 0
    while i < len(wy_list):
        website('wy', str(i + 1), wy_list[i])
        i += 1


def keywords_distinct(sina_keywords, qq_keywords, souhu_keywords, wy_keywords):
    keywords_list = []
    for i in range(len(sina_keywords)):
        if sina_keywords[i] not in keywords_list:
            keywords_list.append(sina_keywords[i])
    for i in range(len(qq_keywords)):
        if qq_keywords[i] not in keywords_list:
            keywords_list.append(qq_keywords[i])
    for i in range(len(souhu_keywords)):
        if souhu_keywords[i] not in keywords_list:
            keywords_list.append(souhu_keywords[i])
    for i in range(len(wy_keywords)):
        if wy_keywords[i] not in keywords_list:
            keywords_list.append(wy_keywords[i])
    return keywords_list


def keywords(keyword):
    db = s.conn()
    for i in range(len(keyword)):
        sql = f'''INSERT INTO `sjk`.`key_information`(`id`, `keyword`, `keycount`, `source_article_count`)
                    VALUES ({str(i+1)}, '{keyword[i][0]}', {keyword[i][1]}, {keyword[i][2]})'''
        print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
    s.close(db)


def authors(author):
    db = s.conn()
    j = 1
    print(author)
    for i in range(len(author)):
        author[i][3].replace('"', "”")
        sql = f'''INSERT INTO `sjk`.`author_information`(`id`, `name`, `article_count`, `ip_address`, `introduction`, `fans_number`, `source`)
                                            VALUES ({str(j)}, '{author[i][0]}', {author[i][1]}, '{author[i][2]}',"{author[i][3]}", {author[i][4]}, '{author[i][5]}')'''

        try:
            cursor = db.cursor()
            cursor.execute(sql)
            j += 1
        except Exception as e:
            # print(e, e.__class__.__name__)
            sql = f'''UPDATE `sjk`.`author_information`
            SET `name`='{author[i][0]}', `article_count`={author[i][1]},
             `ip_address` ='{author[i][2]}', `introduction`='{author[i][3]}', `fans_number`={author[i][4]},
              `source`='{author[i][5]}' WHERE `name`='{author[i][0]}' AND `source`='{author[i][5]}' '''
            cursor = db.cursor()
            cursor.execute(sql)
        finally:
            print(sql)
    s.close(db)


def articles(essay):
    db = s.conn()
    j = 1
    for i in range(len(essay)):
        sql = f'''INSERT INTO `sjk`.`essay_information`(`id`, `title`, `author`, `source`, `word_count`, `type`, `comment_count`, `publish_time`, `keyword`, `keyword_count`, `publish_address`, `article_link`)
                  VALUES ({str(j)}, '{essay[i][0]}', '{essay[i][1]}', '{essay[i][2]}',{essay[i][3]}, '{essay[i][4]}', {essay[i][5]}, '{essay[i][6]}', '{essay[i][7]}',{essay[i][8]}, '{essay[i][9]}', '{essay[i][10]}')'''
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            j += 1
        except Exception as e:
            print(e, e.__class__.__name__)
        finally:
            print(sql)
    s.close(db)


def type_info():
    db = s.conn()
    j = 1
    sql = '''SELECT type FROM `wy_information` 
UNION SELECT type from `qq_information`
UNION SELECT type from `sina_information`
UNION SELECT type from `souhu_information`'''
    cursor = db.cursor()
    cursor.execute(sql)
    types = cursor.fetchall()
    # print(types)
    for i in range(len(types)):
        try:
            sql = f'''INSERT INTO `sjk`.`type_information`
                  VALUES ({str(j)}, '{types[i][0]}', 0)'''

            cursor = db.cursor()
            cursor.execute(sql)
            j += 1
        except Exception as e:
            print(e, e.__class__.__name__)
        finally:
            print(sql)
    s.close(db)


def webs_info():
    db = s.conn()
    cursor = db.cursor()
    sql = '''INSERT INTO `sjk`.`website_information`
VALUES ("新浪网","http://www.sina.com.cn",0,30,"北京","北京新浪互联信息服务有限公司","1998","一切由你开始");'''
    cursor.execute(sql)
    sql = '''INSERT INTO `sjk`.`website_information`
VALUES ("网易网","http://www.163.com",0,27,"杭州","网易网络有限公司","1997","网聚人的力量");'''
    cursor.execute(sql)
    sql = '''INSERT INTO `sjk`.`website_information`
VALUES ("搜狐网","https://www.sohu.com/",0,21,"北京","北京搜狐互联网信息服务有限公司","1998","上搜狐, 知天下");'''
    cursor.execute(sql)
    sql = '''INSERT INTO `sjk`.`website_information`
VALUES ("腾讯网","https://www.qq.com/",0,24,"深圳","深圳市腾讯计算机系统有限公司","1998","一切以用户价值为依归");'''
    cursor.execute(sql)
    s.close(db)


def key_counts():
    db = s.conn()
    cursor = db.cursor()
    sql = '''SELECT keyword from key_information;'''
    cursor.execute(sql)
    keys = cursor.fetchall()
    for i in range(len(keys)):
        sql = f'''select keyword_count from `essay_information` where keyword='{keys[i][0]}' '''
        # print(keys)
        articles = cursor.execute(sql)
        counts = cursor.fetchall()
        count = 0
        for j in range(len(counts)):
            count += counts[j][0]
        # print(count, articles)
        sql = f'''update `key_information` set keycount={count},source_article_count={articles} where keyword='{keys[i][0]}' '''
        cursor.execute(sql)
    s.close(db)


def author_article():
    db = s.conn()
    cursor = db.cursor()
    sql = '''SELECT name from author_information;'''
    cursor.execute(sql)
    auths = cursor.fetchall()
    for i in range(len(auths)):
        sql = f'''select * from `essay_information` where author='{auths[i][0]}' '''
        # print(keys)
        article_count = cursor.execute(sql)
        # print(count, articles)
        sql = f'''update `author_information` set article_count={article_count} where name='{auths[i][0]}' '''
        cursor.execute(sql)
    s.close(db)


def web_article_count(web, web_name=''):
    db = s.conn()
    cursor = db.cursor()
    if web != 'website':
        sql = f'''SELECT type from `{web}_information` '''
        print(sql)
        cursor.execute(sql)
        type_name = cursor.fetchall()
        for i in range(len(type_name)):
            if web_name != '':
                sql = f'''select * from `essay_information` where type='{type_name[i][0]}' and source='{web_name}' '''
            else:
                sql = f'''select * from `essay_information` where type='{type_name[i][0]}' '''
            print(sql)
            counts = cursor.execute(sql)
            sql = f'''update `{web}_information` set article_number={counts} where type='{type_name[i][0]}' '''
            cursor.execute(sql)
    else:
        sql = f'''SELECT * from `essay_information` where source='{web_name}' '''
        counts = cursor.execute(sql)
        sql = f'''update `website_information` set article_count={counts} where webname='{web_name}网' '''
        cursor.execute(sql)

    s.close(db)


def webs_article_count():
    web_article_count('sina', '新浪')
    web_article_count('qq', '腾讯')
    web_article_count('souhu', '搜狐')
    web_article_count('wy', '网易')
    web_article_count('type')
    web_article_count('website', '新浪')
    web_article_count('website', '腾讯')
    web_article_count('website', '搜狐')
    web_article_count('website', '网易')


def run():
    # sina_list, sina_keywords, sina_author, sina_article = sina.run()
    # # sina_list, sina_keywords, sina_author, sina_article = [], [], [], []
    # qq_list, qq_keywords, qq_author, qq_article = qq.run()
    # # qq_list, qq_keywords, qq_author, qq_article = [], [], [], []
    # souhu_list, souhu_keywords, souhu_author, souhu_article = souhu.run()
    # # souhu_list, souhu_keywords, souhu_author, souhu_article = [], [], [], []
    # wy_list, wy_keywords, wy_author, wy_article = wy.run()
    # # wy_list, wy_keywords, wy_author, wy_article = [], [], [], []
    # websites(sina_list, qq_list, souhu_list, wy_list)
    # keywords_list = keywords_distinct(sina_keywords, qq_keywords, souhu_keywords, wy_keywords)
    # keywords(keywords_list)
    # authors(sina_author + qq_author + souhu_author + wy_author)
    # type_info()
    # articles(sina_article + qq_article + souhu_article + wy_article)
    # webs_info()
    # key_counts()
    author_article()
    webs_article_count()



if __name__ == '__main__':
    sina = SinaSpider()
    qq = QQSpider()
    souhu = SouhuSpider()
    wy = WySpider()
    run()
