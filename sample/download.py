import requests, json, re, sys, os
from contextlib import closing

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class spider():
    def __init__(self, a, b=None):

        self.sess = requests.session()
        if b is None:
            self.find(a)
        else:
            self.singer=b
            self.pattern = re.compile(b)
            self.name = a


    def url_spider(self):
        num=1
        url_list = []
        for n, i in enumerate(api):
            req = self.sess.get(url=i.format(self.name+'%20'+self.singer,5))
            data = req.json()["data"]
            for j in data:
                match = self.pattern.search(j["singer"])
                if match:
                    print(num,'from:',api_name[n],j['name'],j['singer'])
                    url_list.append(j['url'])
                    num+=1
                    break
        if url_list ==[]:
            print('未搜索到相关歌曲')
        else:
            ch = input('请选择序号:')
            return url_list[int(ch)-1]

    def find(self,a):
        '''
        req = requests.get('http://baike.baidu.com/search/word', headers=dn_headers, params={'word': self.name})
        req.encoding = 'utf-8'
        m = re.findall(r'title="(.*?).{2}的?歌曲"', req.text)
        print('有如下歌手的歌曲版本：\n')
        for i in m:
            print(i, '\n')
        singer = input('请输入歌手：')
        self.pattern = re.compile(singer)
        self.singer=singer
        '''

        # 判断输入是歌手还是歌曲名
        req = self.sess.get(url=api[0].format(a, 1))
        data = req.json()["data"][0]
        match = re.search(a, data["singer"])

        if match:
            self.singer=a
            self.pattern = re.compile(a)
            for n, i in enumerate(api):
                req = self.sess.get(url=i.format(a, 5))
                data = req.json()["data"]
                print('from',api_name[n])
                for j in data:
                    if self.pattern.search(j["singer"]):
                        print(j['name'],j['singer'])
            self.name=input('请输入歌名：')
        else:
            self.name=a
            for n, i in enumerate(api):
                req = self.sess.get(url=i.format(a, 2))
                data = req.json()["data"]
                print('from', api_name[n])
                for j in data:
                    print(j['name'],j['singer'])
            self.singer=input('请输入歌手：')
            self.pattern = re.compile(self.singer)

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
                print('链接异常 错误代码：', response.status_code)


dn_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'}

api = ['https://api.bzqll.com/music/netease/search?key=579621905&s={}&type=song&limit={}&offset=0',
       'https://api.bzqll.com/music/tencent/search?key=579621905&s={}&limit={}&offset=0&type=song',
       'https://api.bzqll.com/music/kugou/search?key=579621905&s={}&limit={}&offset=0&type=song']
api_name = ['网易云音乐', 'QQ音乐', '酷狗音乐']

if __name__ == '__main__':
    a = sys.argv[1]
    if len(sys.argv) == 2:
        b = None
    elif len(sys.argv) == 3:
        b = sys.argv[2]

    ar = spider(a, b)
    url = ar.url_spider()
    if url is not None:
        print(url)
        ar.downloader(url)
