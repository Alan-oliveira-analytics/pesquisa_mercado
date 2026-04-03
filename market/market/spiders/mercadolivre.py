import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/monitor#D[A:monitor]"]

    def parse(self, response):

        products = response.css('div.ui-search-result__wrapper')

        for product in products:

            yield {
                'title': product.css('a.poly-component__title::text').get(),
                'review': product.css('span.poly-phrase-label::text').get(),
                'price': product.css('span.andes-money-amount__fraction::text').getall(),
                'percent_off': product.css('span.poly-price__disc_label::text').get(),
                'installment_count' : product.css('span.poly-price__installments::text').get(),
                'installment_amount': product.css('span.andes-money-amount__fraction::text').getall()
            }

        pass

        
