#-*- Coding UTF-8 -*-

from PIL import Image
import requests
import fitz
import glob
import os 
from re import findall
from multiprocessing import Pool


#   网页图片为webp格式时需要转换png一次
def webp2png():
    for img in glob.glob(r'*.webp'):
        im=Image.open(img)
        im.save('%s.png'%img.split('.')[0],'png')

def png2pdf(pdf_name):
    #   打开一个空文档
    doc = fitz.open()
    for png in sorted(glob.glob(r"*.png")): 
    #sorted 按照顺序重新排序对象。 glob命令可以读取该文件夹下所有图片
        imdoc = fitz.open(png)                  # open image
        pdfbytes = imdoc.convertToPDF()         # make one page PDF
        imgpdf = fitz.open('pdf',pdfbytes)
        doc.insertPDF(imgpdf)                   # add diese Seite 
    #if os.path.exists('%s.pdf'%pdf_name):
        #os.remove('%s.pdf'%pdf_name)
    doc.save('%s.pdf'%pdf_name)      # save pdf
    doc.close()
    os.system('del *.png')
    print('%s.pdf  ok....'%pdf_name)


def img_dl(index,img_url):
    response = requests.get(img_url[index])
    f=open('%03d.png'%index,'wb')
    print('%03d.png  ok...'%index)
    f.write(response.content)
    f.close()

def web2png(url):
    pool=Pool()
    response = requests.get(url).text
    content=response
    #   找到所有图片的真实地址
    img_url=findall('data-src="(.+?)"',content)
    #   排查其他文章是否存在，如果被删除会无法爬取
    if content.find('该内容已被发布者删除' )==-1:
        pdf_name=findall('"og:title" content="(.+?)"',content)[0]
    else:
        pdf_name='培训班'
    print(pdf_name)
    #   剔除所有标题包含培训班的文章，其没有爬取价值
    if pdf_name.find('培训班')==-1:
        #   判断该文章是否已经爬取，如果已存在，跳过
        if not os.access('%s.pdf'%pdf_name,os.F_OK):
            for index in range(len(img_url)):
                #   多进程保存图片，加速爬取速度
                pool.apply_async(img_dl,(index,img_url))
            pool.close()
            pool.join()
            a=1
            #   判断所有图片是否都已下载，如果没有进行至多5次重复下载
            while len(glob.glob(r'*.png'))<len(img_url):
                a += 1
                if a==5:
                    break
                for index in range(len(img_url)):
                    if not os.access('%03d.png'%index,os.F_OK):
                        img_dl(index,img_url)
            png2pdf(pdf_name)
        #with open('%s.txt'%pdf_name,'w',encoding='utf-8') as f:
        #f.write(''.join(img_url))
        #f.write(content)
        #f.close()

if __name__ == '__main__':
    #   目标网址，包含所有ppt的超链接
    url='https://mp.weixin.qq.com/s?__biz=MzI5Mjc4NjkyNQ==&mid=2247493522&idx=1&sn=28a0ba30972a5eb24b380de6661211b4&chksm=ec7ea010db092906b2b59682aed6928e3587650987842e85fa6c1dbcbb2af3c1824e0622a31a&scene=21#wechat_redirect'
    #   需要设置非加密通讯，hhtps多次建立加密通信会报错（未解决）
    response = requests.get(url,verify=False).text
    content=str(response)
    #   正则表达式找到底部所有其他文章链接，（）内为返回list内容
    url=findall('<a href="(http.+?)"',content)

    for index in url:
        web2png(index)


    #   微信公众号不做浏览器头验证，这个头可以不用
    headers={
    'Origin' : 'https://mp.weixin.qq.com',
    'Referer':'https://mp.weixin.qq.com/s?__biz=MjM5MzM5MDY1MQ==&mid=2658246483&idx=1&sn=63c4ef72e6c0da64e18692d04f93c2ce&chksm=bd12f6078a657f1172e2a5344dcdda2f39e97b7a423b47780e2e07963c7d16d68592654eb947&scene=0&xtrack=1',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36'
}
