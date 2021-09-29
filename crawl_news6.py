from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
import pandas as pd
import datetime
import time

#获取某一属性下的所有链接和单篇新闻内容
def get_content(kind):
    #访问首页获得最大页码
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    b = webdriver.Chrome()
    b.get('https://www.matichon.co.th/'+str(kind)+'/page/1')
    time.sleep(10)  # 网页慢设置等待
    wait = WebDriverWait(b, 20, 5)  # 最长等待30s，每5s判定查找元素是否存在
    e = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="last"]')))[0].text  #最后一页页码
    print('获得所需元素：' + str(e))
    b.close()
    last_page = int(e)
    last_page = min(last_page, 1000)
    wb = Workbook()  # 创建新的工作簿工作表
    ws = wb.active
    for page in range(1, last_page+1):   #可随时修改页面，重新爬取
        print('当前属性为：'+str(kind)+'页码为：'+str(page))
        link_list = list(set(get_page_links(kind, page)))  #获取某页面下所有单篇新闻链接
        for link in link_list:
            print('访问单条链接：'+link)
            print('等待中...')
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            b = webdriver.Chrome()
            b.get(link)
            time.sleep(10)  #网页慢设置等待
            wait = WebDriverWait(b, 20, 5)   #最长等待30s，每5s判定查找元素是否存在
            e = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="block-title"]//span')))[0].text
            print('获得所需元素：'+str(e))
            title = str(b.find_element_by_xpath('//h1[@class="entry-title"]').text)
            day = str(b.find_element_by_xpath('//header//span//time').text)
            para = []
            for i in b.find_elements_by_xpath('//div[@class="td-ss-main-content"]//p'):
                para.append(str(i.text))
            content = [link, clean1(title), clean1(day), clean1(para)]
            print('获取单篇新闻内容成功：'+str(content))
            b.close()
            ws.append(content)
            wb.save('C://Users//zyb//project//news6_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind))
            print('写入单篇新闻内容成功')
            print('------------------------')
            time.sleep(1.5)  #写入等待
        print('********************************')
    wb.close()



#某一页码下所有单篇新闻链接
def get_page_links(kind, page):
    link_list = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    b = webdriver.Chrome(options=chrome_options)
    b.get('https://www.matichon.co.th/'+str(kind)+'/page/'+str(page))
    time.sleep(10)  # 网站太慢设置了10s的等待
    # 因为网站加载太慢，设置显性等待，等待找到id为footer的元素，等待20s ，要是找不到就报错了
    wait = WebDriverWait(b, 20)
    e = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="last"]')))[0].text  #最后一页页码
    print('找到该页面的页码元素:')
    print(e)  # 这个是找到的元素
    for i in b.find_elements_by_xpath('//h3//a'):
        link = str(i.get_attribute("href"))
        if 'news' in link:
            link_list.append(link)
    b.close()
    print('属性：'+str(kind)+'页码'+str(page)+'单篇新闻链接获取完成')
    print('*************************************')
    print(str(link_list))
    return link_list


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


#'court-news', 'covid19', 'politics', 'economy', 'local', 'region', 'foreign', 'education', 'lifestyle', 'sport', 'entertainment', 'international', 'prachachuen'
kind_list = ['court-news', 'covid19', 'politics', 'economy', 'local', 'region', 'foreign', 'education', 'lifestyle', 'sport', 'entertainment', 'international', 'prachachuen']
#利用pandas整合四类新闻到一个excel文件中
def combine():
    file = []
    for i in range(0, len(kind_list)):
        #无表头方式读取文件并设置表头
        file.append(pd.read_excel('C://Users//zyb//project//news6_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d"), kind=kind_list[i]), header=None, Names=['A','B','C','D']))
    writer = pd.ExcelWriter('C://Users//zyb//project//news6_{d}_{kind}.xlsx'.format(d=datetime.datetime.now().strftime("%m-%d")))
    result = pd.concat(file, axis=0).reset_index(drop=True)  #上下合并，并重设行索引即不按原来索引方式排列
    result.to_excel(writer, 'Sheet', index=False, header=None)   #去掉表头
    writer.save()
    print('合并文件成功')


for kind in kind_list:
    print('当前新闻类型为：'+str(kind))
    print('等待中...')
    get_content(kind)
    print(str(kind)+'类型新闻获取完毕')
    print('****************************')
    time.sleep(5)

kind_list = [ 'court-news', 'covid19', 'politics', 'economy', 'local', 'region', 'foreign', 'education', 'lifestyle', 'sport', 'entertainment', 'international', 'prachachuen']
combine()  #整合四个文件到一个文件中