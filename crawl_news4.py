from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
import pandas as pd
import datetime
import time


# 返回主页所有新闻链接
def crawl_main():
    b = webdriver.Chrome()
    print('开始访问主页')
    b.get('http://www.thairath.co.th/home')  #访问主页
    time.sleep(20)   #设置强制等待
    wait = WebDriverWait(b, 40, 5)  # 最长等待40s，每5s判定查找元素是否存在
    e = wait.until(EC.presence_of_element_located((By.XPATH, '//img[@alt="thairath-logo"]'))).get_attribute('alt')
    print('找到页面元素：')
    print(e)
    link_list = []
    for i in b.find_elements_by_xpath('//h2//a'):
        link = i.get_attribute('href')
        if 'video' in link or 'clip' in link:
            continue
        if '/news/' in link:
            link_list.append(link)
    for i in b.find_elements_by_xpath('//h3//a'):
        link = i.get_attribute('href')
        if 'video' in link or 'clip' in link:
            continue
        if '/news' in link:
            link_list.append(link)
    b.close()   #关闭浏览器
    link_list = list(set(link_list))
    print('获取的主页新闻链接：'+str(link_list))
    return link_list


#返回某一属性所有新闻链接
def crawl_kind(kind):
    print('正在访问页面：'+'https://www.thairath.co.th/'+str(kind))
    b = webdriver.Chrome()
    b.get('https://www.thairath.co.th/'+str(kind))
    time.sleep(20)
    wait = WebDriverWait(b, 40, 5)
    e = wait.until(EC.presence_of_element_located((By.XPATH, '//img[@alt="thairath-logo"]'))).get_attribute('alt')
    print('找到页面元素：')
    print(e)
    link_list = []
    for i in b.find_elements_by_xpath('//h2//a'):
        link = i.get_attribute('href')
        if '/'+str(kind)+'/' in link:
            link_list.append(link)
    b.close()
    link_list = list(set(link_list))
    print('获取的新闻链接：'+str(link_list))
    return link_list


#获取单篇新闻链接下内容
def get_content(link_list, kind):
    wb = Workbook()
    ws = wb.active
    for link in link_list:
        print('正在访问链接：'+str(link))
        b = webdriver.Chrome()
        b.get(link)
        time.sleep(40)
        wait = WebDriverWait(b, 40, 3)
        e = wait.until(EC.presence_of_element_located((By.XPATH, '//img[@alt="thairath-logo"]'))).get_attribute('alt')
        print('找到页面元素：')
        print(e)
        title = str(b.find_element_by_xpath('//h1').text)
        day = str(b.find_element_by_xpath('//span[@class="css-1o5avae e1ui9xgn2"]').text)
        para_list = []
        for i in b.find_elements_by_xpath('//p'):
            para = str(i.text)
            para = para.replace('\n', '')
            para = para.replace('\r', '')
            para = para.strip()
            if len(para) > 0:
                para_list.append(str(para))
        content = [link, str(title), str(day), ''.join(para_list)]
        print('获取的单篇新闻内容为：'+str(content))
        b.close()  # 关闭网页
        ws.append(content)
        wb.save('C://cs//python//news4_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind))
        time.sleep(1.5)
        print('写入单条内容成功')
        print('-----------------------')
    print('该属性下所有链接访问完成')
    print('***************************')
    wb.close()

'''
#获取首页新闻链接和对应的单篇新闻内容
link_list = crawl_main()
time.sleep(1)
get_content(link_list, 'home')
'''
kind_list = ['news', 'sport', 'entertain']
for kind in kind_list:
    link_list = crawl_kind(kind)
    time.sleep(1)
    get_content(link_list, kind)
    time.sleep(1)

file = []
kind_list = ['home', 'news', 'sport', 'entertain']
for i in range(0, len(kind_list)):
    #无表头方式读取文件并设置表头
    file.append(pd.read_excel('C://cs//python//news4_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind_list[i]), header=None, Names=['A','B','C','D']))
writer = pd.ExcelWriter('C://cs//python//news4_{d}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d")))
result = pd.concat(file, axis=0).reset_index(drop=True)  #上下合并，并重设行索引即不按原来索引方式排列
result.to_excel(writer, 'Sheet', index=False, header=None)   #去掉表头
writer.save()
print('合并文件成功')
