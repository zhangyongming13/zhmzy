import scrapy
import time
import random
from zhmzy.items import ZhmzyItem


url = ['url']


class Zhmzy_tupian(scrapy.Spider):
    name = 'zhmzy'
    allowed_url = ['url']
    start_urls = ['url']
    url_init = 'url'

    def parse(self,response):
        try:
            data = response.xpath("//a[@class='video-pic loading']")
            for each in data:  # 获取整个页面存在的帖子的名字对象的链接
                item = ZhmzyItem()
                item['tiezi_name'] = each.xpath("./span[@class='note text-bg-c']/text()").extract()[0]
                item['tiezi_link'] = self.url_init + each.xpath("./@href").extract()[0]
                # 获取每一个链接帖子的具体情况，相当于点进去然后获取每个图片的链接
                time.sleep(15 + random.randint(40, 160) / 10 )
                tupian_data = scrapy.Request(item['tiezi_link'], meta={'item': item}, callback=self.detail_parse)
                yield tupian_data
        except:
            print('该页爬取不成功！')
            recall_url = response._url
            time.sleep(15 + random.randint(10, 100) / 10)
            yield scrapy.Request(recall_url, callback=self.parse)

        try:  # 获取下一页链接地址
            try:
                next_page = response.xpath("//*[@id='long-page']/ul/li[10]/a/@href").extract()[0]
            except:
                next_page = response.xpath("//*[@id='long-page']/ul/li[11]/a/@href").extract()[0]
            url = self.url_init + next_page
            time.sleep(15 + random.randint(10, 100) / 10)
            yield scrapy.Request(url, callback=self.parse)
        except:
            print('爬取完毕！')

    def detail_parse(self, tupian_data):  # 获取每个帖子的图片的所有链接
        item = tupian_data.meta['item']
        link = []
        try:
            data = tupian_data.xpath("//div[@class='details-content text-justify']/p/img")
            for each in data:
                src = each.xpath("@src").extract()[0]
                link.append(src)
            item['tupian_link'] = link
            # for i in link:
            #     tupian = scrapy.Request(i, meta={'item': item}, callback=self.Get_tupian_data)
            #     yield tupian
        except:
            pass
        yield item

    # def Get_tupian_data(src, tupian):  # 获取图片链接对应的数据
    #     item = tupian.meta['item']
    #
    #     yield tupian.content
