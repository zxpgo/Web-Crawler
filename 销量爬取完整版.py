import requests
import bs4
import re
import json
from openpyxl import Workbook
import time


def open(keywords, page):

      headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
               "referer":"https://www.taobao.com/"}

    
      payload = {'q':keywords, "initiative_id": "staobaoz_20181102","data-key":"s","data-value": str((page-1)*44),"sourceId": "tb.index","sort":"sale-desc"}
      url = "https://s.taobao.com/search"

      res = requests.get(url, params = payload,headers = headers)
      return res
      
      
def get_item(res):

      g_page_config = re.search(r'g_page_config = (.*?);\n', res.text)
      page_config_json = json.loads(g_page_config.group(1))
      page_item = page_config_json['mods']['itemlist']['data']['auctions']

      result = []#整理出我们关注的信息(ID,标题，链接，售价，销量和商家)
      for each in page_item:
            dict1 =dict.fromkeys(('id','title','link','price','sale','shoper'))
            dict1['id'] = each['nid']
            dict1['title'] = each['title']
            dict1['link'] = each['detail_url']
            dict1['price'] = each['view_price']
            dict1['sale'] = each['view_sales']
            dict1['shoper'] = each['nick']
            result.append(dict1)
            #print(dict1['shoper'],dict1['price'],dict1['title'])
      return result

          
def count_sales(items):
      count = 0
      for each in items:
            if ' ' in each['title']:#规定只取标题中包含小甲鱼
                  count += int(re.search(r'\d+',each['sale']).group())
                  
      return count

def main():

      keywords = input("请输入搜索关键词：")
      length = 10 #淘宝商品页数
      total = 0
      wb = Workbook()
      ws = wb.worksheets[0]
      t = time.strftime('%Y.%m.%d',time.localtime(time.time()))
      for each in range(length):
            res = open(keywords, each+1)
            items = get_item(res)
            for line in items:
                  count = int(re.search(r'\d+',line['sale']).group())
                  line1 = [line["price"],count,line['shoper'],line["title"],t]
                  ws.append(line1)
                  print(line1)
      wb.save("data.xlsx")
      total += count_sales(items)#销售总量
      print(total)


if __name__ == "__main__":
      main()
