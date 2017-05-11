import scrapy
import re
from scrapy.utils.response import open_in_browser

class LawyersSpider(scrapy.Spider):
    """Crawls lawyers' listings in floridabar website."""
    
    name = 'lawyers'
    start_urls = [
        'https://www.floridabar.org/'
        + 'directories/find-mbr/'
        + '?barNum=&lName=&lNameSdx=N&fName=&fNameSdx=N&eligible=N&deceased=N'
        + '&firm=&locValue=&locType=C&pracAreas=&lawSchool=&services='
        + '&langs=&certValue=&pageNumber=1&pageSize=50'
    ]

    def parse(self, response):
        """Follows pagination links and iterate through floridabar listings."""
        # Extract page number and increment it by 1 for the next page
        curpagenum = re.findall('pageNumber=[0-9]+', response.url)[0]
        curpagenum = int(re.findall('[0-9]+', curpagenum)[0]) + 1
        newurl = re.sub('pageNumber=[0-9]+',
                        'pageNumber={}'.format(curpagenum),
                        response.url
                       )
        yield scrapy.Request(newurl, callback= self.parse)
