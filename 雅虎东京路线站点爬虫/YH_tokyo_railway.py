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
    tokyo_url =[
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%B1%B1%E6%89%8B%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%B7%8F%E6%AD%A6%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E9%9D%92%E6%A2%85%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%B8%AD%E5%A4%AE%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BA%AC%E6%B5%9C%E6%9D%B1%E5%8C%97%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%8D%97%E6%AD%A6%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%9F%BC%E4%BA%AC%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%B8%AD%E5%A4%AE%E6%9C%AC%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%B8%B8%E7%A3%90%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BA%94%E6%97%A5%E5%B8%82%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%B9%98%E5%8D%97%E6%96%B0%E5%AE%BF%E3%83%A9%E3%82%A4%E3%83%B3&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BA%AC%E8%91%89%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%85%AB%E9%AB%98%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%A8%AA%E6%B5%9C%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%AD%A6%E8%94%B5%E9%87%8E%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%B7%8F%E6%AD%A6%E6%9C%AC%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%A8%AA%E9%A0%88%E8%B3%80%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E5%8C%97%E6%9C%AC%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E6%B5%B7%E9%81%93%E6%9C%AC%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E9%AB%98%E5%B4%8E%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%B8%8A%E8%B6%8A%E6%96%B0%E5%B9%B9%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%B8%8A%E9%87%8E%E6%9D%B1%E4%BA%AC%E3%83%A9%E3%82%A4%E3%83%B3&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%8C%97%E9%99%B8%E6%96%B0%E5%B9%B9%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E5%8C%97%E6%96%B0%E5%B9%B9%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E6%B5%B7%E9%81%93%E6%96%B0%E5%B9%B9%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%9B%B8%E9%89%84%E7%9B%B4%E9%80%9A%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%B8%B8%E3%83%8E%E5%86%85%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9C%89%E6%A5%BD%E7%94%BA%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%97%A5%E6%AF%94%E8%B0%B7%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%8D%83%E4%BB%A3%E7%94%B0%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%8D%97%E5%8C%97%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E9%8A%80%E5%BA%A7%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E8%A5%BF%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%89%AF%E9%83%BD%E5%BF%83%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E5%9C%B0%E4%B8%8B%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%8D%8A%E8%94%B5%E9%96%80%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%96%B0%E5%AE%BF%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%B1%A0%E8%A2%8B%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%8B%9D%E5%B3%B6%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%9A%E6%91%A9%E6%B9%96%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%9A%E6%91%A9%E5%B7%9D%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%9B%BD%E5%88%86%E5%AF%BA%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E8%A5%BF%E6%AD%A6%E6%9C%89%E6%A5%BD%E7%94%BA%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E8%A5%BF%E6%AD%A6%E5%9C%92%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E8%B1%8A%E5%B3%B6%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E8%A5%BF%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%B1%B1%E5%8F%A3%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E7%8E%8B%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BA%AC%E7%8E%8B%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E7%8E%8B%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BA%95%E3%81%AE%E9%A0%AD%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E7%8E%8B%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%9B%B8%E6%A8%A1%E5%8E%9F%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E7%8E%8B%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E9%AB%98%E5%B0%BE%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E7%8E%8B%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BA%AC%E7%8E%8B%E6%96%B0%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E7%8E%8B%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%8B%95%E7%89%A9%E5%9C%92%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E7%8E%8B%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%AB%B6%E9%A6%AC%E5%A0%B4%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%A7%E4%BA%95%E7%94%BA%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%B1%A0%E4%B8%8A%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%B8%96%E7%94%B0%E8%B0%B7%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%94%B0%E5%9C%92%E9%83%BD%E5%B8%82%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E6%A8%AA%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%9B%AE%E9%BB%92%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%9A%E6%91%A9%E5%B7%9D%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%BA%A4%E9%80%9A%E5%B1%80&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%A7%E6%B1%9F%E6%88%B8%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%BA%A4%E9%80%9A%E5%B1%80&prefname=%E6%9D%B1%E4%BA%AC&line=%E8%8D%92%E5%B7%9D%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%BA%A4%E9%80%9A%E5%B1%80&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%B8%89%E7%94%B0%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%BA%A4%E9%80%9A%E5%B1%80&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%96%B0%E5%AE%BF%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%BA%A4%E9%80%9A%E5%B1%80&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%B5%85%E8%8D%89%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E9%83%BD%E4%BA%A4%E9%80%9A%E5%B1%80&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%97%A5%E6%9A%AE%E9%87%8C%E3%83%BB%E8%88%8E%E4%BA%BA%E3%83%A9%E3%82%A4%E3%83%8A%E3%83%BC&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BC%8A%E5%8B%A2%E5%B4%8E%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E4%B8%8A%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E4%BA%80%E6%88%B8%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E6%AD%A6%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%A7%E5%B8%AB%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E6%88%90%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9C%AC%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E6%88%90%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%8A%BC%E4%B8%8A%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E6%88%90%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E9%87%91%E7%94%BA%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E6%B5%9C%E6%80%A5%E8%A1%8C%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9C%AC%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E4%BA%AC%E6%B5%9C%E6%80%A5%E8%A1%8C%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E7%A9%BA%E6%B8%AF%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E5%B0%8F%E7%94%B0%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%B0%8F%E7%94%B0%E5%8E%9F%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E5%B0%8F%E7%94%B0%E6%80%A5%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%9A%E6%91%A9%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E8%87%A8%E6%B5%B7%E9%AB%98%E9%80%9F%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E3%82%8A%E3%82%93%E3%81%8B%E3%81%84%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E5%8C%97%E7%B7%8F%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%8C%97%E7%B7%8F%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E9%AB%98%E5%B0%BE%E7%99%BB%E5%B1%B1%E9%9B%BB%E9%89%84&prefname=%E6%9D%B1%E4%BA%AC&line=%E9%AB%98%E5%B0%BE%E7%99%BB%E5%B1%B1%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E5%A4%9A%E6%91%A9%E9%83%BD%E5%B8%82%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%A4%9A%E6%91%A9%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E9%A6%96%E9%83%BD%E5%9C%8F%E6%96%B0%E9%83%BD%E5%B8%82%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E3%81%A4%E3%81%8F%E3%81%B0%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%97%E3%83%AC%E3%82%B9&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E3%82%86%E3%82%8A%E3%81%8B%E3%82%82%E3%82%81&prefname=%E6%9D%B1%E4%BA%AC&line=%E8%87%A8%E6%B5%B7%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E5%BE%A1%E5%B2%B3%E7%99%BB%E5%B1%B1%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%BE%A1%E5%B2%B3%E5%B1%B1%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E5%9F%BC%E7%8E%89%E9%AB%98%E9%80%9F%E9%89%84%E9%81%93&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%9F%BC%E7%8E%89%E9%AB%98%E9%80%9F%E9%89%84%E9%81%93%E7%B7%9A&exdone=",
        "https://transit.yahoo.co.jp/stedit/station?pref=13&company=%E6%9D%B1%E4%BA%AC%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB&prefname=%E6%9D%B1%E4%BA%AC&line=%E6%9D%B1%E4%BA%AC%E3%83%A2%E3%83%8E%E3%83%AC%E3%83%BC%E3%83%AB%E7%BE%BD%E7%94%B0%E7%B7%9A&exdone="
    ]
    big_list = []
    url ='https://transit.yahoo.co.jp/stedit/station?pref=13&company=JR&prefname=%E6%9D%B1%E4%BA%AC&line=%E5%B1%B1%E6%89%8B%E7%B7%9A&exdone='
    html = call_page(url)
    parse_pages(html)

    # 上面完成第一次登陆，后面就不再登陆
    lpath = os.getcwd()
    for url in tokyo_url:
        driver.get(url)
        # 弄一个模拟登陆背
        time.sleep(1)
        html = driver.page_source
        parse_pages(html)


        print(big_list)


    text_save('{0}\\t.xlsx'.format(lpath),big_list)
    driver.quit()




#     lpath = '/root/YD_mp3Cards/日语mp3单词库'
#     # lpath =  os.getcwd()
#     excelFile = '{0}/mp_jans.xlsx'.format(lpath)
#     full_items = read_xlrd(excelFile=excelFile)
#     for single_name in full_items:
#         print(single_name)
#         url = 'https://www.youdao.com/w/jap/{0}/#keyfrom=dict2.top'.format(single_name[0])
#         html = call_page(url)
#
#         patt = re.compile('<a href="#" title="发音" class="sp dictvoice voice-js log-js" data-rel="(.*?)" data-4log="dict.basic.jc.voice"></a>',re.S)
#         mp3_c = re.findall(patt, html)
#         try:
#             big_list = []
#             if len(mp3_c) != 0:
#                 for item in mp3_c:
#                     f_url = "".join(item.split("amp;"))
#                     big_list.append('https://dict.youdao.com/dictvoice?audio={0}'.format(f_url))
#
#             for mp3_url in big_list:
#                 res = requests.get(mp3_url)
#
#                 music = res.content
#
#                 with open(r'{0}/{1}.mp3'.format(lpath,single_name[1]), 'ab') as file:  # 保存到本地的文件名
#                     file.write(res.content)
#                     file.flush()
#                     time.sleep(0.3)
#
#         except:
#
#             pass


