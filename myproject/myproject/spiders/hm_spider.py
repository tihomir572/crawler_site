import scrapy
import json


class HMProductSpider(scrapy.Spider):
    name = "hm_product"
    allowed_domains = ["www2.hm.com"]
    start_urls = ["https://www2.hm.com/bg_bg/productpage.1274171085.html"]

    def parse(self, response):
        name = response.css('h1::text').get()
        price = response.css('span.b44193.e396ea.d9ca8b::text').get()[:-3].replace(",", '.')
        color = response.css('[property="og:title"]::attr(content)').get().split(' - ')[1]
        json_ld = response.css('script[id="__NEXT_DATA__"]::text').get()

        data = json.loads(json_ld)

        availableColors_list = []
        for value in data['props']['pageProps']['productPageProps']['aemData']['productArticleDetails'][
            'variations'].values():
            if value['selection']:
                availableColors_list.append(value['swatchDetails']['colorName'])

        yield scrapy.Request(url='https://www2.hm.com/bg_bg/reviews/rrs/ugcsummary?sku=1274171085004',
                             headers={
                                 "sec-ch-ua-platform": "\"Windows\"",
                                 "Referer": "https://www2.hm.com/bg_bg/productpage.1274171085.html",
                                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                                 "Accept": "application/json",
                                 "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
                                 "Content-Type": "application/json",
                                 "sec-ch-ua-mobile": "?0"
                             },
                             callback=self.reviews_callback,
                             meta={
                                 "name": name,
                                 "price": price,
                                 "color": color,
                                 "availableColors": availableColors_list
                             })

    def reviews_callback(self, response):
        response_json = response.json()[0]
        rating = response_json['ratings']
        avg_rating = response_json['averageRating']
        yield {
            "name": response.meta['name'],
            "price": response.meta['price'],
            "color": response.meta['color'],
            "availableColors": response.meta['availableColors'],
            "reviews_count": rating,
            "reviews_score": avg_rating,
            # **response.meta
        }
