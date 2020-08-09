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

def call_page(url):

    driver.get(url)
    # 弄一个模拟登陆背
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="username"]').clear()
    driver.find_element_by_xpath('//*[@id="username"]').send_keys("")#用户名
    driver.find_element_by_xpath('//*[@id="btnNext"]').click()
    time.sleep(3)

    driver.find_element_by_xpath('//*[@id="passwd"]').clear()
    driver.find_element_by_xpath('//*[@id="passwd"]').send_keys("")# 密码
    driver.find_element_by_xpath('//*[@id="btnSubmit"]/span').click()


    html = driver.page_source


    return html


def parse_pages(html):

    selector = etree.HTML(html)
    station_Name = selector.xpath('//*[@id="station"]/ul/li/a/text()')
    city_name = selector.xpath('//*[@id="cat-pass"]/p/a[4]/text()')
    railwayName = selector.xpath('//*[@id="title"]/h2/text()')
    f_city = len(station_Name)*city_name
    f_railwayName= len(station_Name)*railwayName
    for i1,i2,i3 in zip(station_Name,f_railwayName,f_city):
        big_list.append((i1+"--"+i2+"--"+i3))








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



if __name__ == '__main__':

    driver = webdriver.Chrome()
    osaka_url = ["https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E5%A4%A7%E9%98%AA%E7%92%B0%E7%8A%B6%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E7%89%87%E7%94%BA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E3%81%8A%E3%81%8A%E3%81%95%E3%81%8B%E6%9D%B1%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E9%96%A2%E8%A5%BF%E6%9C%AC%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E6%9D%B1%E6%B5%B7%E9%81%93%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E6%9D%B1%E8%A5%BF%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E6%9D%B1%E6%B5%B7%E9%81%93%E6%9C%AC%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E6%A1%9C%E5%B3%B6%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E9%96%A2%E8%A5%BF%E7%A9%BA%E6%B8%AF%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E5%B1%B1%E9%99%BD%E6%96%B0%E5%B9%B9%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E6%9D%B1%E6%B5%B7%E9%81%93%E6%96%B0%E5%B9%B9%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E7%A6%8F%E7%9F%A5%E5%B1%B1%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E8%B0%B7%E7%94%BA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%BE%A1%E5%A0%82%E7%AD%8B%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%95%B7%E5%A0%80%E9%B6%B4%E8%A6%8B%E7%B7%91%E5%9C%B0%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E4%B8%AD%E5%A4%AE%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%8D%83%E6%97%A5%E5%89%8D%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E4%BB%8A%E9%87%8C%E7%AD%8B%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%9B%9B%E3%81%A4%E6%A9%8B%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%8D%97%E6%B8%AF%E3%83%9D%E3%83%BC%E3%83%88%E3%82%BF%E3%82%A6%E3%83%B3%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E5%B8%82%E9%AB%98%E9%80%9F%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%A0%BA%E7%AD%8B%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%8D%97%E5%A4%A7%E9%98%AA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%A4%A7%E9%98%AA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%A5%88%E8%89%AF%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%95%B7%E9%87%8E%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E3%81%91%E3%81%84%E3%81%AF%E3%82%93%E3%81%AA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E4%BF%A1%E8%B2%B4%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%81%93%E6%98%8E%E5%AF%BA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%9B%A3%E6%B3%A2%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%BF%91%E7%95%BF%E6%97%A5%E6%9C%AC%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E8%A5%BF%E4%BF%A1%E8%B2%B4%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E5%A4%A7%E9%98%AA&line=%E4%BA%AC%E9%83%BD%E6%9C%AC%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E5%A4%A7%E9%98%AA&line=%E5%AE%9D%E5%A1%9A%E6%9C%AC%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E5%A4%A7%E9%98%AA&line=%E5%8D%83%E9%87%8C%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E5%A4%A7%E9%98%AA&line=%E7%A5%9E%E6%88%B8%E6%9C%AC%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E5%A4%A7%E9%98%AA&line=%E7%AE%95%E9%9D%A2%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%8D%97%E6%B5%B7%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%8D%97%E6%B5%B7%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%8D%97%E6%B5%B7%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%AB%98%E9%87%8E%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%8D%97%E6%B5%B7%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E5%A4%9A%E5%A5%88%E5%B7%9D%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%8D%97%E6%B5%B7%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E7%A9%BA%E6%B8%AF%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%8D%97%E6%B5%B7%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%AB%98%E5%B8%AB%E6%B5%9C%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E4%BA%AC%E9%98%AA%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E4%BA%AC%E9%98%AA%E6%9C%AC%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E4%BA%AC%E9%98%AA%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E4%BA%A4%E9%87%8E%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E4%BA%AC%E9%98%AA%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E4%B8%AD%E4%B9%8B%E5%B3%B6%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E5%A0%BA%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%98%AA%E5%A0%BA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E5%A0%BA%E9%9B%BB%E6%B0%97%E8%BB%8C%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E4%B8%8A%E7%94%BA%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB&prefname=%E5%A4%A7%E9%98%AA&line=%E5%A4%A7%E9%98%AA%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%A4%A7%E9%98%AA%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB&prefname=%E5%A4%A7%E9%98%AA&line=%E5%9B%BD%E9%9A%9B%E6%96%87%E5%8C%96%E5%85%AC%E5%9C%92%E9%83%BD%E5%B8%82%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E7%A5%9E%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E3%81%AA%E3%82%93%E3%81%B0%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E9%98%AA%E7%A5%9E%E9%9B%BB%E6%B0%97%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E9%98%AA%E7%A5%9E%E6%9C%AC%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E6%B0%B4%E9%96%93%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E6%B0%B4%E9%96%93%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E6%B3%89%E5%8C%97%E9%AB%98%E9%80%9F%E9%89%84%E9%81%93&prefname=%E5%A4%A7%E9%98%AA&line=%E6%B3%89%E5%8C%97%E9%AB%98%E9%80%9F%E9%89%84%E9%81%93%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E8%83%BD%E5%8B%A2%E9%9B%BB%E9%89%84&prefname=%E5%A4%A7%E9%98%AA&line=%E5%A6%99%E8%A6%8B%E7%B7%9A&exdone=","https://transit.yahoo.co.jp/stedit/station?pref=27&company=%E5%8C%97%E5%A4%A7%E9%98%AA%E6%80%A5%E8%A1%8C%E9%9B%BB%E9%89%84&prefname=%E5%A4%A7%E9%98%AA&line=%E5%8D%97%E5%8C%97%E7%B7%9A&exdone="]

    url ="https://transit.yahoo.co.jp/stedit/station?pref=27&company=JR&prefname=%E5%A4%A7%E9%98%AA&line=%E9%98%AA%E5%92%8C%E7%B7%9A&exdone="
    html = call_page(url)
    parse_pages(html)

    # 上面完成第一次登陆，后面就不再登陆
    lpath = os.getcwd()
    for url in osaka_url:
        big_list = []
        driver.get(url)
        # 弄一个模拟登陆背
        time.sleep(1)
        html = driver.page_source
        parse_pages(html)



        print(big_list)


    # text_save('{0}\\s.xlsx'.format(lpath),big_list)



#
# create table tokyo_railway
# (id int not null primary key auto_increment,
# hanzi text,
# jiaming text,
# railway text,
# location text) engine=InnoDB  charset=utf8;
