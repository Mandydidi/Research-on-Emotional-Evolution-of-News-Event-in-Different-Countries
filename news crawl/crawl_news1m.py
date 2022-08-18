from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
import pandas as pd
import datetime
import time


#获取某一属性下的所有链接
def get_links(kind):
    #设置为无页面浏览模式
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    b = webdriver.Chrome(options=chrome_options)
    b.get('https://www.bharian.com.my/'+str(kind))
    time.sleep(10)    # 网站太慢设置了10s的等待
    # 因为网站加载太慢，设置显性等待，等待找到id为footer的元素，等待10s ，要是找不到就报错了
    wait = WebDriverWait(b, 40)
    e = wait.until(EC.presence_of_all_elements_located((By.ID, 'footer')))
    print('找到该页面的footer元素:')
    print(e)   # 这个是找到的footer元素
    link_list = []
    for i in b.find_elements_by_xpath('//span[@class="field-content"]//a'):  #第一部分链接
        link = str(i.get_attribute("href"))
        if kind in link:
            link_list.append(link)
    for i in b.find_elements_by_xpath('//div[@class="item-wrapper"]//a'):  #第二部分链接
        link = str(i.get_attribute("href"))
        if kind in link:
            link_list.append(link)
    link_list = list(set(link_list))
    print('当前页面获取到的新闻链接为：'+str(link_list))
    b.close()   #关闭当前浏览器
    wb = Workbook()  #创建新的工作簿工作表
    ws = wb.active
    for link in link_list:
        if 'https://www.bharian.com.my' not in link:  #获取单条新闻链接
            link = 'https://www.bharian.com.my'+str(link)
        print('访问单条链接：'+link)
        print('等待中...')
        b = webdriver.Chrome()
        b.get(link)
        time.sleep(10)  #网页慢设置等待
        wait = WebDriverWait(b, 30, 5)   #最长等待30s，每5s判定查找元素是否存在
        e = wait.until(EC.presence_of_all_elements_located((By.ID, 'footer')))
        print('获得所需元素：')
        print(str(e))
        title = str(b.find_element_by_xpath('//div//h1').text)
        day = str(b.find_element_by_xpath('//div[@class="node-meta"]').text)
        con = []
        for i in b.find_elements_by_xpath('//div[@class="field-items"]'):
            con.append(str(i.text))
        content = [link, clean1(title), clean1(day), clean1(con)]
        print('获取单篇新闻内容成功：'+str(content))
        b.close()
        ws.append(content)
        wb.save('D://cs//python//project//news1_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind))
        print('写入单篇新闻内容成功')
        print('------------------------')
        time.sleep(1.5)  #写入等待
    wb.close()


#数据预处理列表，返回字符串
def clean1(v_list):
    res = []
    for v in v_list:
        v = v.replace('\n', '')
        v = v.replace('\r', '')
        v = v.strip()
        if len(v) > 0:
            res.append(str(v))
    return ''.join(res)


#'berita', 'sukan', 'dunia',
kind_list = [ 'berita', 'sukan', 'dunia','hiburan']
#利用pandas整合四类新闻到一个excel文件中
def combine():
    file = []
    for i in range(0, len(kind_list)):
        #无表头方式读取文件并设置表头
        file.append(pd.read_excel('D://cs//python//project//news1_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind_list[i]), header=None, Names=['A','B','C','D']))
    writer = pd.ExcelWriter('D://cs//python//project//news1_{d}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d")))
    result = pd.concat(file, axis=0).reset_index(drop=True)  #上下合并，并重设行索引即不按原来索引方式排列
    result.to_excel(writer, 'Sheet', index=False, header=None)   #去掉表头
    writer.save()
    print('合并文件成功')

'''
for kind in kind_list:
    print('当前新闻类型为：'+str(kind))
    print('等待中...')
    get_links(kind)
    print(str(kind)+'类型新闻获取完毕')
    print('****************************')
    time.sleep(5)
'''
combine()  #整合四个文件到一个文件中