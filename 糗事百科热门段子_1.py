# -*- coding: cp936 -*-
import urllib
import urllib2
import re
import os
import xlwt

def open_url(page):
    head = {}
    head['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    url = "https://www.qiushibaike.com/hot/page/" + str(page) +'/'
    req = urllib2.Request(url, headers=head)
    respone = urllib2.urlopen(req)
    html = respone.read().decode("utf-8")
    return html
    

#<img src="//pic.qiushibaike.com/system/avtnew/2476/24768804/thumb/20171109213309.JPEG?imageView2/1/w/90/h/90" alt="一炮敏℡恩仇">
p_name = r'<img src="//([^"]+)" alt="([^"]+)">'
#<div class="articleGender womenIcon">23</div>
p_age = r'<div class="articleGender ([^"]+)">([^"]{1,3})</div>'
#<i class="number">994</i>
p_laugh = r'<i class="number">([^"]{1,5})</i>'

#file_object = open('thefile.txt', 'w')
#file_object.write(str(list_age))
#file_object.close( )


f = xlwt.Workbook() #创建工作簿
sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True) #创建sheet

for j in range(10):
    html = open_url(j+1)
    list_age = re.findall(p_age, html)
    list_name = re.findall(p_name,html)
    list_laugh = re.findall(p_laugh, html)
    for i in range(len(list_name)):
        sheet1.write(i+1+j*25,0,list_name[i][1])
    for i in range(len(list_age)):
        sheet1.write(i+1+j*25,1,list_age[i][1])
        sheet1.write(i+1+j*25,2,list_age[i][0])
    for i in range(len(list_laugh)/2):
        sheet1.write(i+1+j*25,3,list_laugh[2*(i+1)-1])
        sheet1.write(i+1+j*25,4,list_laugh[2*(i)])

sheet1.write(0,0,'name')
sheet1.write(0,1,'age')
sheet1.write(0,2,'gender')
sheet1.write(0,3,'comment num')
sheet1.write(0,4,'good num')
#sheet1.write(0,0,start_date,set_style('Times New Roman',220,True))
f.save('糗事百科.xls')#保存文件


'''
for each in list_name:
    for i in range(2):
        print('\s' % each[i])
for each in list_age:
    for i in range(2):
        print(each[i])
for each in list_laugh:
  print(each)
'''


        





