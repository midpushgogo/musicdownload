import requests, json, re, sys, os
from contextlib import closing
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class spider():
    def __init__(self, name, singer=None):
        if singer is None:
            self.find()
        else:
            self.singer = singer
        self.name = name
        self.sess = requests.session()

    def url_spider(self):
        api = ['https://api.bzqll.com/music/netease/search?key=579621905&s={}&type=song&limit=5&offset=0',
               'https://api.bzqll.com/music/tencent/search?key=579621905&s={}&limit=5&offset=0&type=song',
               'https://api.bzqll.com/music/kugou/search?key=579621905&s={}&limit=5&offset=0&type=song']
        for i in api:
            req = self.sess.get(url=i.format(self.name))
            data = req.json()["data"]
            for i in data:
                if i['singer'] == self.singer:
                    return i["url"]

    def downloader(self, url):
        size = 0
        # 单线程下载
        with closing(self.sess.get(url, headers=dn_headers, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
                with open(self.name + '.mp3', 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
                        sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                        # sys.stdout.flush()
                        if size / content_size == 1:
                            print('\n')
            else:
                print('链接异常 错误代码：',response.status_code)



dn_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'}

if __name__ == '__main__':
    if len(sys.argv)==2:
        name = sys.argv[1]
        singer=None
    elif len(sys.argv)==3:
        name = sys.argv[1]
        singer = sys.argv[2]

    a = spider(name, singer)
    url = a.url_spider()
    if url is not None:
        print(url)
        a.downloader(url)





