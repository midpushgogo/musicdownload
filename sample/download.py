import requests, json, re, sys, os
from contextlib import closing
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class spider():
    def __init__(self, name, singer=None):
        self.name = name
        self.sess = requests.session()
        if singer is None:
            self.find()
        else:
            self.pattern = re.compile(singer)

    def url_spider(self):
        api = ['https://api.bzqll.com/music/netease/search?key=579621905&s={}&type=song&limit=5&offset=0',
               'https://api.bzqll.com/music/tencent/search?key=579621905&s={}&limit=5&offset=0&type=song',
               'https://api.bzqll.com/music/kugou/search?key=579621905&s={}&limit=5&offset=0&type=song']
        for i in api:
            req = self.sess.get(url=i.format(self.name))
            data = req.json()["data"]
            for i in data:
                match = self.pattern.search(i["singer"])
                if match:
                    return i["url"]
        print('未搜索到相关歌曲')


    def find(self):
        req = requests.get('http://baike.baidu.com/search/word', headers=dn_headers, params={'word': self.name})
        # date=str(req.content,'utf-8')
        req.encoding = 'utf-8'
        m = re.findall(r'title="(.*?).{2}的?歌曲"', req.text)
        print('有如下歌手的歌曲版本：\n')
        for i in m:
            print(i,'\n')
        singer=input('请输入歌手：')
        self.pattern = re.compile(singer)





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
    name = sys.argv[1]
    if len(sys.argv)==2:
        singer=None
    elif len(sys.argv)==3:
        singer = sys.argv[2]

    a = spider(name, singer)
    url = a.url_spider()
    if url is not None:
        print(url)
        a.downloader(url)





