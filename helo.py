import requests
from bs4 import BeautifulSoup
import os
import urllib
from urllib import request
import threading
import threadpool


class mzitu():
    num = 0
    picNum = 0

    def all_url(self, url):
        self.cv = threading.Condition()
        html = self.request(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')

        task_pool = threadpool.ThreadPool(50)
        requests = threadpool.makeRequests(self.nice, all_a)
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()

        # for a in all_a:
        #     if self.num >= 50:
        #         self.cv.acquire()
        #         self.cv.wait()
        #         self.cv.release()
        #     self.num = self.num + 1
        #     t = threading.Thread(target=self.nice, args=(
        #         a,))  # cloudquery是指每个线程干的活，
        #     t.start()  # 启动线程

    def nice(self, a):
        title = a.get_text()
        path = str(title).replace("?", '_')  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
        if self.mkdir(path):  ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            os.chdir("e:\\pic\\" + path)  ##切换到目录
            href = a['href']
            self.html(href, "e:\\pic\\" + path)  ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！
            # self.num = self.num - 1
            # self.cv.acquire()
            # self.cv.notify()
            # self.cv.release()

    def html(self, href, path):  ##这个函数是处理套图地址获得图片的页面地址
        html = self.request(href)
        helo = BeautifulSoup(html.text, 'lxml').find_all('span')
        if len(helo) < 10:
            return
        max_span = helo[10].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url, path)  ##调用img函数

    def img(self, page_url, path):  ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        helo = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image')
        if helo is not None:
            helo1 = helo.find('img')
            if helo1 is not None:
                # do some thing you need
                img_url = helo1['src']
                self.helo(img_url, path)

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        if path.__contains__("妲己"):
            return False
        isExists = os.path.exists(os.path.join("e:\\pic\\", path))
        if not isExists:
            os.makedirs(os.path.join("e:\\pic\\", path))
            return True
        else:
            return False

    def request(self, url):  ##这个函数获取网页的response 然后返回
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)

        return content

    def helo(self, url, path):
        getHeaders = {
            'Host': 'i.meizitu.net',
            'Connection': 'Keep-Alive',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer': 'http://www.mzitu.com/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        response = requests.get(url, headers=getHeaders)
        if (response.status_code == 404):  # 若404错误，递归get，尝试非重定向方式获取
            response = requests.get(url, headers=getHeaders, allow_redirects=False)
            if (response.status_code == 302):  # 302表示访问对象已被移动到新位置，但仍按照原地址进行访问（造成404错误）。
                name = url[-9:-4]
                redirectUrl = response.headers['location']  # 因此需在响应头文件中获取重定向后地址
                response = requests.get(redirectUrl)
                fp = open(name + ".jpg", 'ab')
                fp.write(response.content)
                fp.close()
        else:
            os.chdir(path)
            name = url[-9:-4]
            fp = open(name + ".jpg", 'ab')
            fp.write(response.content)
            fp.close()
            self.picNum = self.picNum + 1
            print(self.picNum)


Mzitu = mzitu()  ##实例化
Mzitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
