from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from myproject.spiders.hm_spider import HMProductSpider
from scrapy import cmdline
cmdline.execute("scrapy crawl hm_product".split())

# if __name__ == '__main__':
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(HMProductSpider)
    # process.start()
