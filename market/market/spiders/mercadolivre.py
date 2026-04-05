import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/monitor#D[A:monitor]"]
    page_count = 1
    max_page = 10

    def parse(self, response):

        products = response.css('div.ui-search-result__wrapper')

        for product in products:

            prices = product.css('span.andes-money-amount__fraction::text').getall()

            yield {
                'title': product.css('a.poly-component__title::text').get(),
                'review': product.css('span.poly-phrase-label::text').get(),
                'new_price': prices[1] if len(prices) > 1 else None,
                'old_price': prices[0] if len(prices) > 0 else None,
                'percent_off': product.css('span.poly-price__disc_label::text').get(),
                'installment_count' : product.css('span.poly-price__installments::text').get(),
                'installment_amount': prices[2] if len(prices) > 2 else None
            }

            if self.page_count <= self.max_page:

                next_page = response.css('li.andes-pagination__button andes-pagination__button--next a::attr(href)').get()

                if next_page:
                    self.page_count += 1

                    yield scrapy.Request(url=next_page, callback=self.parse)

        pass

        
