from requests_html import HTMLSession
import time
import re


class fofa_spider:
    '''fofa 爬虫'''

    def __init__(self, qbase64, cookies):
        self.s = HTMLSession()
        self.cookies = {'_fofapro_ars_session': cookies}
        self.url = 'https://fofa.so/result?qbase64=' + qbase64
        self.link_list = self.link()

    def _page(self):
        '''取出最大页数和链接地址'''

        r = self.s.get(self.url, cookies=self.cookies)
        page_max = r.html.xpath('//*[@id="will_page"]/a')[-2].attrs["href"]
        page_max = int(re.search(r'/result\?page=(\d*).*', page_max)[1])
        # 我的会员只能看一千页，所以大于一千也的不看
        if page_max > 1000:
            page_max = 1000
        for page in range(1, page_max+1):
            yield self.url + '&page=' + str(page)

    def _link(self, url):
        '''取出每个结果的，url或IP+prot'''
        r = self.s.get(url, cookies=self.cookies)
        linkall = r.html.xpath('//*[@id="ajax_content"]/div')
        list1 = []
        for link in linkall[:-1]:
            try:
                # 取url如果报错就是ip
                try:
                    link = link.xpath('//div[1]/div[1]', first=True)
                    link = list(link.xpath('//div[1]/div[1]/a[2]', first=True).links)[0]
                except AttributeError:
                    link = list(link.xpath('//div[1]/div[1]/a', first=True).links)[0]
            except AttributeError:
                # 取出 ip+prot
                link = link.xpath('//div[1]/div[1]', first=True).text
                
            list1.append(link)
        return list1

    def link(self):
        for page in self._page():
            yield self._link(page)


if __name__ == "__main__":
    qbase64 = 'InNoaXJvIiAmJiBjb3VudHJ5PSJrciI%3D'
    cookies = 'a056c8c8238185208122fff65d806a4b'
    a = fofa_spider(qbase64, cookies)
    for i in a.link_list:
        print(i)
        time.sleep(3)