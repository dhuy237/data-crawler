# import scrapy
# from scrapy.selector import Selector
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
# from scrapy.http import FormRequest

# # class UAESpider(scrapy.Spider):
# #     name = 'uae_free'

# #     allowed_domains = ['https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=A']

# #     start_urls = [
# #         'https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=A'
# #     ]

# #     # def __init__(self):
# #     #     chrome_options = Options()
# #     #     chrome_options.add_argument("--headless")

# #     #     chrome_path = 'D:\\work\\crawl data\\selenium_project\\chromedriver.exe'

# #     #     driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
# #     #     driver.get("https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=A")

# #     def parse(self, response):
# #         pages = response.xpath('//table[@class="GridViewStyle"]//tr[12]//a/@href').getall()
# #         for page in pages[0:11]:
# #             rows = page.xpath('//table[@class="GridViewStyle"]//tr')
# #             for row in rows[1:11]:
# #                 yield {
# #                     'company_name': row.xpath('.//td[2]//text()').get(),
# #                     'company_name_link': row.xpath('.//td[2]//a/@href').get(),
# #                     'zone': row.xpath('.//td[4]//text()').get(),
# #                     'category': row.xpath('.//td[6]//text()').get(),
# #                     'category_link': row.xpath('.//td[6]//a/@href').get()
# #                 }

# #         # next_section = response.xpath('//table[@class="GridViewStyle"]//tr[12]//td[11]//a/@href').get()

# #         # if next_section:
# #         #     yield scrapy.Request(url=next_section, callback=self.parse)

# HEADERS = {
#     'X-MicrosoftAjax': 'Delta=true',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
# }

# URL = 'https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=A'

# class UAESpider(scrapy.Spider):
#     name = 'uae_free'

#     allowed_domains = ['https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=A']

#     start_urls = [
#         'https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=A'
#     ]

#     def parse(self, response):
#         self.data = {}
        
#         for form_input in response.css('form#aspnetForm input'):
#             name = form_input.xpath('@name').extract()[0]
#             try:
#                 value = form_input.xpath('@value').extract()[0]
#             except IndexError:
#                 value = ""
#             self.data[name] = value

#         # self.data['ctl00_ContentPlaceHolder2_panelGrid'] = 'ctl00$ContentPlaceHolder2$grdDirectory'
#         self.data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder2$grdDirectory'
#         self.data['__EVENTARGUMENT'] = 'Page$1'

#         yield FormRequest(url=URL,
#                             method='POST',
#                             callback=self.parse_page,
#                             formdata=self.data,
#                             meta={'page':1},
#                             dont_filter=True,
#                             headers=HEADERS)

#     def parse_page(self, response):
#         current_page = response.meta['page'] + 1
#         rows = response.xpath('//table[@class="GridViewStyle"]//tr')
#         for row in rows[1:11]:
#             yield {
#                 'company_name': row.xpath('.//td[2]//text()').get(),
#                 'company_name_link': row.xpath('.//td[2]//a/@href').get(),
#                 'zone': row.xpath('.//td[4]//text()').get(),
#                 'category': row.xpath('.//td[6]//text()').get(),
#                 'category_link': row.xpath('.//td[6]//a/@href').get()
#             }

#         # EVENTVALIDATION = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()
#         VIEWSTATE = response.css('input#__VIEWSTATE::attr(value)').extract_first()

#         data = {
#             '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$grdDirectory',
#             '__EVENTARGUMENT': 'Page$%d' % current_page,
#             '__VIEWSTATE': VIEWSTATE
#             # '__EVENTVALIDATION': EVENTVALIDATION
#             }

#         return FormRequest(url=URL,
#                             method='POST',
#                             formdata=data,
#                             callback=self.parse_page,
#                             meta={'page': current_page},
#                             dont_filter=True,
#                             headers=HEADERS)

# import scrapy
# from scrapy.http import FormRequest


class UAESpider(scrapy.Spider):
    name = 'uae_free'
    headers = {
        'X-MicrosoftAjax': 'Delta=true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
    }

    allowed_domains = ['www.uaeonlinedirectory.com']
    # TODO: Include the urls for all other items (e.g. A-Z)
    start_urls = ['https://www.uaeonlinedirectory.com/UFZOnlineDirectory.aspx?item=Z']
    current_page = 0

    def parse(self, response):
        # request the next page
        self.current_page = self.current_page + 1

        if self.current_page == 1:
            # submit a form (first page)
            data = {}
            for form_input in response.css('form#aspnetForm input'):
                name = form_input.xpath('@name').extract()[0]
                try:
                    value = form_input.xpath('@value').extract()[0]
                except IndexError:
                    value = ""
                data[name] = value
            data['__EVENTTARGET'] = 'ctl00$MainContent$List'
            data['__EVENTARGUMENT'] = 'Page$1'
        else:
            # Extract the form fields and arguments using XPATH
            event_validation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()
            view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract()
            view_state_generator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()
            view_state_encrypted = response.xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()

            data = {
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$grdDirectory',
                '__EVENTARGUMENT': 'Page$%d' % self.current_page,
                '__EVENTVALIDATION': event_validation,
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': view_state_generator,
                '__VIEWSTATEENCRYPTED': view_state_encrypted,
                '__ASYNCPOST': 'true',
                '': ''
            }

        # Yield the companies
        # TODO: move this to a different function
        rows = response.xpath('//table[@class="GridViewStyle"]//tr')
        for row in rows[1:11]:
            result = {
                'company_name': row.xpath('.//td[2]//text()').get(),
                'company_name_link': row.xpath('.//td[2]//a/@href').get(),
                'zone': row.xpath('.//td[4]//text()').get(),
                'category': row.xpath('.//td[6]//text()').get(),
                'category_link': row.xpath('.//td[6]//a/@href').get()
            }
            yield result

        # TODO: check if there is a next page, and only yield if there is one
        yield FormRequest(url=self.start_urls[0],  # TODO: change this so that index is not hardcoded
                          method='POST',
                          formdata=data,
                          callback=self.parse,
                          meta={'page': self.current_page},
                          dont_filter=True,
                          headers=self.headers)