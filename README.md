# Database-lessons  
抓取四大门户的内容，然后进行数据清理和分析，最后将信息存储在数据库中进行可视化。  
## 成员    
啊英：表的设计，搜狐网站数据爬取，数据展示图表的选择。     
啊悦：表的设计，新浪网站数据爬取，搭建superset平台进行大数据展示。  
小唐：表的设计，网易网站数据爬取，代码合并，将数据导入数据库。  
啊媛：表的设计，腾讯网站数据爬取，数据展示图表的选择。  
## 表的设计    
1. 根据四大门户网站的数据特性和共性，运用数据库相关知识设计出十张基本表和对应数据类型。  
2. 根据后期爬取数据塞入过程进行数据类型和设计的迭代。  
3. 每人写2-3个表的建表sql语句，将空表在数据库中创建出来。  
## 爬虫    
1. 新浪、搜狐、网易分别由三位小伙伴采取正则表达式和一些常见的库进行爬取，最终将需要爬取的对应表的数据封装在对应函数中。  
2. 腾讯由一位小伙伴采用谷歌驱动进行爬取对应内容，并且采取多线程，通过空间换时间的策略方法提高爬取速度。    
驱动链接：https://chromedriver.storage.googleapis.com/index.html    
## 数据清洗    
1. 一起约定具体数据格式要求，将数据清洗封装到每个独立的函数中。    
2. 进行合并，使用sql语句将具体数据插入更新到具体表中。   
## 数据聚合展示   
1. 搭建大数据展示平台superset。     
2. 选取合适的图表和聚合数据进行大数据展示。   
