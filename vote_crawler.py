from bs4 import BeautifulSoup
from urllib import request
import prettytable as pt  # 格式化打印

# 文章汇总链接
url = 'https://developers.weixin.qq.com/community/develop/doc/000a0e617ec7d0b34bfa730b253400'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}

req = request.Request(url, headers=headers)

page = request.urlopen(req).read()
page = page.decode('utf-8')

soup = BeautifulSoup(page, 'html.parser')

# 获取所有的参赛作品链接
try:
    article_links = soup.find('div', attrs={'id': 'content'}).find_all('a')
    res = []
    for link in article_links:
        try:
            res.append({'href': link.get('href'), 'name': link.get_text(), 'like_num': 0})
        except:
            print('获取所有文章链接失败')
except:
    print('获取所有文章链接失败')

print('获取所有文章链接成功, 总共' + str(len(res)))
index = 1

# 遍历每个链接，查询点赞数量
for article in res:
    article_url = article['href']
    print('爬第' + str(index) + '篇文章:' + article_url)
    article_req = request.Request(article_url, headers=headers)
    article_page = request.urlopen(article_req).read().decode('utf-8');
    article_scrap_soup = BeautifulSoup(article_page, 'html.parser')
    try:
        like_num = article_scrap_soup.find('div', attrs={'class': 'post_opr_meta_btn_inner'}).find('span').get_text()
    except:
        like_num = 0
    article['like_num'] = int(like_num)
    index = index + 1

sorted_res = sorted(res, key=lambda i: i['like_num'], reverse=True)

tb = pt.PrettyTable()
tb.align = 'l'
tb.field_names = ['作品名称', '文章链接', '点赞数量']
for item in sorted_res:
    tb.add_row([item['name'], item['href'], item['like_num']])
    
print(tb)

