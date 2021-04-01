import json
import os
import re
import requests
import time
import random
import pandas as pd


class Spider:
    '''京东随机选取100部图书商品每书10条评论爬虫'''

    def __init__(self):
        self.url = None
        self.cookie = 'shshshfpa=1dec07d1-31c1-d395-b409-c19ab27d8de0-1531147936;' \
                      ' shshshfpb=2a0eeb4d693334d7e85fb1f8d3f3f4a605b43769f7c217e0621b61bd57;' \
                      ' __jdu=1553345717454455955504; mt_xid=V2_52007VwMWVl9aV14ZSR9ZAWIGFlZVXF' \
                      'ZeHkwpVAdnBUBVXwtODRlMH0AAZAAWTg1dAF0DTkoIDWcDQFNbWwJSL0oYXA17AhpOXV5DWhhCHFsOZ' \
                      'QciUG1YYlMfTx1ZAGQHEmJeX1s%3D; areaId=7; ipLoc-djd=7-420-45534-0; PCSYCityID=CN_410' \
                      '000_410200_410202; user-key=851d3dca-aaa0-47a5-a3d1-b4cba8ea7744; cn=0; unpl=V2_ZzNtb' \
                      'UEAFhF8DRRdfxhaB2JTFFURUREQd18TVitMCw1kCxoJclRCFX0UR1xnGloUZAEZX0dcQxVFCEdkeBBVAW' \
                      'MDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsdW' \
                      'AdlBhZbQlFGEXANQlBzHVgBZgYibUVncyV8D0VXfhlsBFcCIh8WC0ASdwFOUzYZWAFlARdZRFdFEHENQ1B%2' \
                      'fEVgBYwIXbUNnQA%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f' \
                      '3d30c8dba7459bb52f2eb5eba8ac7d_0_2fd584c850734a79b7c43fd3adf9299e|1569598452338; s' \
                      'hshshfp=e4692fc09e869eb8a131f9313f907646; __jda=122270672.1553345717454455955504.' \
                      '1553345717.1568709832.1569595855.6; __jdc=122270672; 3AB9D23F7A4B3C9B=6442ZN2AYT' \
                      'QNOA3LG2FNGXFN2RC4IKKFPMBAILZO4XTZ5WF2FIXMLCOGE7W6FUTZKDAQCQTIDOJPYVHFMWGGNPOAAE' \
                      '; shshshsID=acb4d916af2f63ae802589a494d0ac43_58_1569599865122; __jdb=122270672.' \
                      '63.1553345717454455955504|6.1569595855'
        self.data = []
        self.COUNT = 0
        # 个人定义的代理
        self.proxys = ['47.95.178.212:3128', '13.212.241.236:80', '13.250.48.44:80',
                       '127.0.0.1:7890']
        # 测试IP可用性的url
        self.check_url = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98" \
                         "&productId=100008771754&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"
        # IP池应用的端口
        self.proxys_url = "http://127.0.0.1:5010/"
        self.headers = {
            'cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'upgrade-insecure-requests': '1',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
        }
        self.get_available_ip()  # 筛选可用ip

    def get_proxy(self):
        """从IP池应用获取IP"""
        proxy = requests.get(f"{self.proxys_url}get_all/").json()
        res = []
        for p in proxy:
            res.append(p['proxy'])
        return res

    def get_available_ip(self):
        """筛选可用IP"""
        check_url = self.check_url

        self.proxys += self.get_proxy()
        self.proxys = list(set(self.proxys))
        available = []
        for ip_address in self.proxys:
            proxy = {
                'https': ip_address,
                'http': ip_address
            }
            try:
                r = requests.get(check_url, headers=self.headers, proxies=proxy, timeout=3)
            except Exception as ex:
                # print(ex)
                print('fail-%s' % ip_address)
            else:
                print('success-%s' % ip_address)
                available.append(ip_address)
        print(f"可用的IP数量为：{len(available)}")
        self.proxys = available

    def request(self, url):
        print(len(self.proxys))
        proxy = random.choice(self.proxys)
        proxies = {
            'http': proxy,
            'https': proxy
        }
        try:
            resp = requests.get(url, headers=self.headers, proxies=proxies, timeout=3)
        except:
            self.proxys.remove(proxy)
            print(f"{proxy}不可用")
            return self.request(url)
        print("请求完毕")
        # resp.encoding = 'gbk'
        return resp.text

    @staticmethod
    def clean_comment(comment: str):
        """清除冗余词汇"""
        comment = comment.replace('使用心得：', '').replace('\xa0', '')
        return comment

    def parse(self, text):
        data0 = re.sub(u'^fetchJSON_comment98\(', '', text)
        reg1 = re.compile('\);')
        data1 = reg1.sub('', data0)
        comment = json.loads(data1)
        for i in comment['comments']:
            self.COUNT += 1
            productName = i['referenceName']
            commentTime = i['creationTime']
            content = ','.join('。'.join(i['content'].split('\n')).split(' ')).replace("&amp", '')
            info = {
                # "商品名" : productName,
                # "评论时间": commentTime,
                "评论内容": content
            }
            print(info)
            self.data.append(info)

    def main(self):
        # 商品IP
        ids = [100008771754, 4217490, 100016285268]
        # 评论类型
        sc0 = {0: "全部",
               1: "差评",
               2: "中评",
               3: "好评"
               }
        for id in ids:
            for score in range(4):
                # 评论大多是好评，差评和中评可能低于1000条
                # 对于全部评论取一半来进行较为完整的评论爬取
                page = 100
                # 失策了，京东只展示100页（0-99，1页10条评论）
                # if score == 0:
                #     page = 700000
                for i in range(page):
                    try:
                        print(f'-----正在爬取第{i + 1}页：{id}的数据-----')
                        # 分别手动改变score参数 score=3 score=2 score=1  爬取好评 中评 差评数据
                        url = f"https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_" \
                              f"comment98&productId={id}&score={score}&sortType=5&page={i}&pageSize=10"
                        text = self.request(url)
                        print("requests执行完毕")
                        self.parse(text)
                        print("prase执行完毕")
                        print('**************************************')
                        print(f'***  当前爬取到的评论总数为：{self.COUNT}  ***')
                        print('**************************************')
                        if self.COUNT >= 200 and self.COUNT % 200 == 0:
                            # 每提交10次请求（爬取100条评论）更新IP池
                            self.get_available_ip()
                            print("IP池更新完毕！")
                        if self.COUNT >= 1000:
                            print('爬取的商品评论数超过1000条！')  # 当抓取到商品评论的数量为1k时停止
                            break

                        time.sleep(random.randint(2, 5))
                    except Exception as ex:
                        print(ex)
                df = pd.DataFrame(self.data)
                self.COUNT = 0  # 重置新文件评论数
                self.data = []
                path = f'./comment/{id}'
                # 创建目录
                if not os.path.exists(path):
                    os.makedirs(path)
                df.to_csv(f'{path}/{sc0[score]}.csv', index_label=None, index=None, encoding='gbk')
                print(f"完成一个文件{path}/{sc0[score]}.csv")


if __name__ == '__main__':
    spi = Spider()
    spi.main()
