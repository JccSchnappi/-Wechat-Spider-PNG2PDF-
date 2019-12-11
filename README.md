# -微信公众号 爬虫-
实现公众号链接寻址，图片多进程下载，合成pdf

# 开发环境
Python 3.7\t\n
Requests
PyMuPDF(fitz)  python的一个第三方pdf库
Multiprocessing Pool

# 基本实现思路
该公众号分将ppt分割为图片，以图片格式分享内容，在文章末尾分享其干货ppt的连接。
爬虫思路如下
1.输入一个文章链接，建立访问，通过requests获得网页前端代码
2.寻址到底部超链接，建立urllist
3.对所有超链接按顺序进行访问，寻址找到图片的真实地址以及文章标题
4.通过多进程池批量下载图片
5.借助fitz模块，将图片合成为pdf



内容来源：博瑞智创汽车技术平台
https://mp.weixin.qq.com/s?__biz=MzI5Mjc4NjkyNQ==&mid=2247509474&idx=1&sn=f5b3c1b082e168f6dff54bcdd56dbd9a&chksm=ec7ee260db096b763fb23c03095fe8b354fa02ebcbdbfeaef14ac2ae990a8f792cb6ef164351&scene=21#wechat_redirect
