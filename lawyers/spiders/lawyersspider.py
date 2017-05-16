import scrapy
import re
from scrapy.utils.response import open_in_browser
from lawyers.items import LawyersItem
from scrapy_splash import SplashRequest

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

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args= {'wait' : 0.5})

    def parse(self, response):
        """Follows pagination links and iterate through floridabar listings."""
        results = response.xpath(
            '//div[@id= "searchresultsheader"]/p//text()'
        ).extract_first()
        totres = re.findall('[0-9,]+(?= results)',
            results
        )[0]
        totres = int(totres.replace(',',''))
        curres = re.findall('(?<=-)[0-9]+(?= of [0-9,]+ results)',
            results
        )[0]
        curres = int(curres)
        if curres < totres:
            # Extract page number and increment it by 1 for the next page
            curpagenum = re.findall('pageNumber=[0-9]+', response.url)[0]
            curpagenum = int(re.findall('[0-9]+', curpagenum)[0]) + 1
            newurl = re.sub('pageNumber=[0-9]+',
                            'pageNumber={}'.format(curpagenum),
                            response.url
                           )
            yield SplashRequest(newurl, callback= self.parse,
                args= {'wait' : 0.5}
            )
