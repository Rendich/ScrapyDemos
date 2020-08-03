import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['http://quotes.toscrape.com']
    start_urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/'
    ]
    def start_request(self):
	    for url in urls:
	        yield scrapy.Request(url=url, callback = self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.txt' % page

        for quote in response.css('div.quote'):
            quote_text = quote.css('span.text::text').get()
            quote_author = quote.xpath('span/small/text()').get()
            s = quote.css('div.tags a.tag::text').getall()
            quote_tags = ' '.join(map(str, s))

            with open(filename, 'a') as f:
            	f.write( quote_text+ ", DE "+ quote_author + " - " + quote_tags + "\n\n" )
            yield {
                'text': quote_text,
                'author': quote_author,
                'tags': quote_tags,
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        self.log('Saved file %s' % filename)
