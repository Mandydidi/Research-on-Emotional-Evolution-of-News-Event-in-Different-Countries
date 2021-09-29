from fake_useragent import UserAgent
import requests
from lxml import etree
import time
import datetime


ua = UserAgent()
#根据feature获取页面中所有新闻链接
def get_links(feature):
    headers = {
        'User-Agent': ua.random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://www.bharian.com.my/',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }
    cookies = {
        '__cfduid': 'd66a528e13a74a910f8da5eb74cb6aea01578465175',
        '_cb': 'D50XDM0bQ_4eZg65',
        '_cb_ls': '1',
        '_cb_svref': 'null',
        '_chartbeat2': '.1578465200516.1578465928889.1.D9UtsDD4MchDC7SbZjDGpZtKBBK_Il.5',
        '_ga': 'GA1.3.302027057.1578465201',
        '_dc_gtm_UA-98696-4': '1',
        '_gid': 'GA1.3.1805810982.1578465201',
        'enableAds': 'no',
        'has_js': '1',
        'loginStatus': 'not logged in',
        'gig_bootstrap_3__S7kGj3PeZ_qvs-Nl-Ypf9POGuDsrGvzxVLNvhcE16cZU0nyve7oP4AtZJrLHkx8': 'ver2',
        'pageType': 'article',
        'reloaded': 'false',
        'UID': 'n/a',
    }
    url = 'https://www.bharian.com.my/'+str(feature)
    response = requests.get(url=url, headers=headers, cookies=cookies, timeout=10)
    response.encoding = 'utf-8'#指定编码
    if response.status_code != 200:
        print('访问网站出错，检查cookies,错误码：'+str(response.status_code))
    else:
        time.sleep(1)
        print('访问新闻网站成功')
        response = response.text
        print(response)
        html = etree.HTML(response)
        link_list = html.xpath('//span/a/@href')
        print(str(feature)+'原始链接')
        print(link_list)
        for i in range(0, len(link_list)):
            link_list[i] = 'https://www.bharian.com.my'+link_list[i]
        print(str(feature)+'新闻链接：')
        print(link_list)
        return link_list

#将获得的两个feature新闻链接写入文本文档
def write_links():
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    file_path = 'E://cs//links1_'+str(month)+'_'+str(day)+'.txt'
    f = open(file_path, 'w+')
    link_list = get_links('berita')+get_links('dunia')
    for each in link_list():
        f.write(each+'\n')
    print('文件写入完成')
    f.close()

write_links()