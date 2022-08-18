from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
import pandas as pd
import datetime
import time


#根据新闻属性获取某一页面上所有新闻链接
def get_links(kind):
    # 设置为无页面浏览模式
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    b = webdriver.Chrome(options=chrome_options)
    print('正在访问'+str(kind)+'属性新闻页面')
    b.get('https://www.malaysiakini.com/my/latest/' + str(kind))
    time.sleep(10)  # 设置10s的等待
    link_list = []
    for i in b.find_elements_by_xpath('//div[@class="jsx-2459159877 news"]//a'):
        link = str(i.get_attribute("href"))
        if '/'+str(kind)+'/' in link:
            link_list.append(link)
    print('该属性下新闻编号为：'+str(link_list))
    b.close()   #关闭浏览器
    wb = Workbook()  #保存一个属性下新闻内容
    ws = wb.active
    #访问单篇新闻网页
    for link in link_list:
        # 设置为无页面浏览模式
        '''
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        b = webdriver.Chrome(options=chrome_options)
        '''
        b = webdriver.Chrome()
        print('正在访问单篇新闻链接：'+str(link))
        b.get(link)
        time.sleep(10)  #设置10s等待
        # 因为网站加载慢，设置显性等待，等待找到指定元素，等待20s ，每5秒钟检查一次，要是找不到就报错了
        wait = WebDriverWait(b, 20, 5)
        e = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="jsx-1905622071"]'))).text
        print('找到该页面的指定元素:')
        print(e)  # 这个是找到的元素
        title = str(b.find_element_by_xpath('//h1').text)
        day = str(b.find_element_by_xpath('//time').text)
        para_list = []
        for para in b.find_elements_by_xpath('//div[@class="jsx-4064603974 content"]//p'):
            para = str(para.text)
            para = para.replace('\n', '')
            para = para.replace('\r', '')
            para = para.strip()
            if len(para) > 0:
                para_list.append(str(para))
        content = [str(link), str(title), str(day), ''.join(para_list)]
        print('获取单页新闻内容为：'+str(content))
        b.close()   #关闭网页
        ws.append(content)
        wb.save('D://cs//python//project//news2_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind))
        time.sleep(2)
        print('写入单条内容成功')
        print('-----------------------')
        time.sleep(1)
    wb.close()



#'news', 'columns', 'letters', 'hiburan', 'sukan'
kind_list = [  'news', 'columns', 'letters', 'hiburan', 'sukan']
#整合文件
def combine():
    file = []
    for i in range(0, len(kind_list)):
        #无表头方式读取文件并设置表头
        file.append(pd.read_excel('D://cs//python//project//news2_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind_list[i]), header=None, Names=['A','B','C','D']))
    writer = pd.ExcelWriter('D://cs//python//project//news2_{d}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d")))
    result = pd.concat(file, axis=0).reset_index(drop=True)  #上下合并，并重设行索引即不按原来索引方式排列
    result.to_excel(writer, 'Sheet', index=False, header=None)   #去掉表头
    writer.save()
    print('合并文件成功')



for kind in kind_list:
    print('当前新闻类型为：'+str(kind))
    get_links(kind)
    print('获取' + str(kind) + '新闻完成')
    print('*****************************')
    time.sleep(1.5)

combine()

