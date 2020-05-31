import scrapy 

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
            'http://quotes.toscrape.com/page/1/'
            # 'http://quotes.toscrape.com/page/2/',
        ]

    def parse(self,response):
        """
        stores dictionary from scraping quotes.toscrape.com
        input:
            response: TextResponse instance that has methods with it.

        """
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("span.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall()
            }
    
        next_page = response.css("li.next a::attr(href)")
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
    # def parse(self, response):
    # """ 
    # Save entire files rather than store data
    # """
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)

class AuthorSpider(scrapy.Spider):
    """ 
    Extract information from authors
    """
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }