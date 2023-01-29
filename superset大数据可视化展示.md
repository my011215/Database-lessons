---
title: superset大数据可视化展示  
date: 2023-1-29 17:12:30
categories:
    - 学习分享  
---
<!-- toc -->  
<!-- more -->  

## 搭建（superset）  
参考：https://juejin.cn/post/6991730150203195400  
个人建议：本人搭建superset颇为费力，在此提以下建议：  
1. python版本建议3.6.7  
2. 各种操作按照最新文档操作  
3. 大数据可视化图片大部分需要时间，所以数据很多要求有时间。自行考虑搭建需求。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/316.png?raw=true)  

## 课设展示  
* 介绍  
对四大门户网站信息进行爬取，和队友自行设计10张表。进行数据清洗后用sql语句写入数据库，最后对数据进行聚合展示。  

### 文章发布时间（git）展示  
在2022年1月-2023年1月，统计每个时间段发布文章数目，参考github样式进行总体展示。  
可以清晰简单的看到每个时间段发布的文章数目  
![](https://github.com/my011215/my011215.github.io/blob/main/image/317.png?raw=true)  

### 网站信息展示  
#### 网站文章数目饼图  
根据四大门户网站，显示每个网站爬取的文章数目。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/318.png?raw=true)  

#### 网站地区文章数目图  
根据四大门户网站总部公司的地址，在中国地图上显示具体位置和对应爬取文章数目总数。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/319.png?raw=true)  

### 四大门户网站信息展示
#### 腾讯网各板块文章数展示  
对腾讯网爬取板块的文章数用柱状图展示文章数目爬取多少情况。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/320.png?raw=true)  

#### 新浪网各板块文章数展示  
对新浪网爬取板块的文章数用柱状图展示文章数目爬取多少情况。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/321.png?raw=true)  

#### 搜狐网各板块文章数展示  
对搜狐网爬取板块的文章数用柱状图展示文章数目爬取多少情况。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/322.png?raw=true)  

#### 网易网各板块文章数展示  
对网易网爬取板块的文章数用柱状图展示文章数目爬取多少情况。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/323.png?raw=true)  

### 作者来源数量展示  
根据作者信息表，对四个门户网站的作者数量使用矩形分布图进行展示。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/324.png?raw=true)  

### 种类信息展示  
根据种类信息表，对每个板块的文章数量使用旭日图进行展示。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/325.png?raw=true)  

### 作者文章top50展示  
根据作者信息表，展示文章总量前50的作者名字。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/326.png?raw=true)  

### 热度top20排名展示  
根据热度信息表，对评论数进行热度排名，选取前20个火爆的文章。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/327.png?raw=true)  

### 关键字信息展示  
根据关键字信息表，对在文章中出现次数排名前20的关键字使用旭日图进行展示。  
![](https://github.com/my011215/my011215.github.io/blob/main/image/328.png?raw=true)  