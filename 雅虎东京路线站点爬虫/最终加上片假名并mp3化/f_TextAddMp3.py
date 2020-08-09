#! -*- coding:utf-8 -*-


import datetime
import re
import os
import time
from selenium import webdriver

import xlrd
from xlrd import xldate_as_tuple
import datetime
import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException
import xlrd



#app选择好(完成)
# 单个下载脚本测试好（完成）
# 需要读取本地excel文件的程序（完成）
# 整理专门的excel文件（完成（完成））
# 在服务器上进行适配# 整理专门的excel文件（完成（完成））
# 放到服务器上去跑




def read_xlrd(excelFile):
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    dataFile = []
    for rowNum in range(table.nrows):
        dataFile.append(table.row_values(rowNum))

       # # if 去掉表头
       # if rowNum > 0:


    return dataFile


def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")


def login_():

    url = 'https://dict.hjenglish.com/jp/jc/%E3%81%8A%E3%81%BE%E3%81%A4%E3%82%8A'
    driver.get(url)
    # 弄一个模拟登陆背
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[1]/header/nav[1]/div/ul[2]/li[1]/a').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="hp-pass-box"]/div/div[1]/div[3]/button').click()
    time.sleep(3)

    driver.find_element_by_xpath('//*[@id="nameInput"]').clear()
    driver.find_element_by_xpath('//*[@id="nameInput"]').send_keys("")  # 用户名
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="passInput"]').clear()
    driver.find_element_by_xpath('//*[@id="passInput"]').send_keys("")  # 密码
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="hp-pass-box"]/div/div[2]/button').click()
    time.sleep(3)

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='fr_pre',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:

        f_4 = "%s," *4
        cursor.executemany('insert into tokyo_railway (hanzi,jiaming,railway,location) values ({0})'.format(f_4[:-1]), content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass
#不强求了，存数据吧！

if __name__ == '__main__':

    driver = webdriver.Chrome()

    lpath = 'C:\\Users\\Administrator\\Desktop\\FR_pre\\雅虎东京路线站点爬虫\\最终加上片假名并mp3化'



    # 剔除所有假名的正则

    excelFile = '{0}\\t.xlsx'.format(lpath)
    full_items = read_xlrd(excelFile=excelFile)
    # login_()
    # 单独弄一个登陆模块
    for single_name in full_items:

        get_url = 'https://dict.hjenglish.com/notfound/jp/jc/{0}'.format(single_name[0])
        driver.get(get_url)
        # 弄一个模拟登陆背
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/form/div[2]/div[2]/button[1]').click()


        time.sleep(2)
        html = driver.page_source

        selector = etree.HTML(html)
        pian_name = selector.xpath('/html/body/div[1]/div/main/div/section/div/section/div/header/div[1]/div[2]/span[1]/text()')
        f_pianName =[]
        if len(pian_name) ==1:
            f_pianName = pian_name
        elif len(pian_name)>1:
            f_pianName = [pian_name[0]]
        elif len(pian_name)==0:
            f_pianName = ["0"]
        else:
            pass
        try:
            f_list = []
            re_fpianName = re.sub(r"[\[\]]","",f_pianName[0])
            patt = re.compile('<span class="word-audio audio audio-light" data-src="(.*?)"></span>',re.S)
            mp3_url = re.findall(patt,html)
            f_saveText = (single_name[0], re_fpianName,single_name[1],single_name[2])
            f_list.append(f_saveText)
            print(f_saveText)
            print(datetime.datetime.now())
            insertDB(f_list)
            try:

                res = requests.get(mp3_url[0])
                music = res.content
                with open(r'{0}\{1}.mp3'.format(lpath, f_saveText), 'ab') as file:  # 保存到本地的文件名
                    file.write(res.content)
                    file.flush()
                    time.sleep(3)
            except:
                pass
        except:
            pass
    # 背禁止访问？
    # text_save('{0}\\f_tokyo.xlsx'.format(lpath), f_list)



# create table tokyo_railway
# (id int not null primary key auto_increment,
# hanzi text,
# jiaming text,
# railway text,
# location text) engine=InnoDB  charset=utf8;


# drop table tokyo_railway;

