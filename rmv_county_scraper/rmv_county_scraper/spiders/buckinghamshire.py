import scrapy
import re
import json
from scrapy.crawler import CrawlerProcess
import mysql.connector

class BuckinghamshireSpider(scrapy.Spider):
    name = 'buckinghamshire'
    allowed_domains = ['rightmove.co.uk']
    start_urls = ['https://www.rightmove.co.uk/estate-agents/Buckinghamshire.html?branchType=SALES&page=1']

    def __init__(self):
        """ Connects to local MySQL server """

        self.mydb = mysql.connector.connect(host='localhost', user='hall_m', password='***', database='rightmove')
        self.mycursor = self.mydb.cursor(buffered=True)

        self.mycursor.execute("SHOW TABLES")
        self.mycursor.execute("TRUNCATE TABLE `buckinghamshire`")


    def parse(self, response):
        """ Loops through the number of pages of estate agents """

        pages = response.xpath('//select[@name="currentPage"]/option/text()').extract()[-1]
        for page_num in range(1, int(pages)+1):
            ea_results_url = "https://www.rightmove.co.uk/estate-agents/Buckinghamshire.html?branchType=SALES&page=" + str(page_num)
            yield scrapy.Request(ea_results_url, callback=self.all_ea_all_pages)


    def all_ea_all_pages(self,response):
        """ Single results page, collects urls of all estate agents on page from branch id"""

        partial_url = "https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E"
        all_urls = response.xpath('//a[@class="ksc_link default"]/@href').extract()
        for url in set(all_urls):
            if url.startswith("/estate-agents/agent") and (url.endswith(".html") or url.endswith("#ram") or url.endswith("#lam")):
                ea_id = re.findall(r'(?<=\-)[0-9]+(?=\.html)', url)[0]
                full_url = partial_url + str(ea_id)
                yield scrapy.Request(full_url, callback=self.one_ea_all_pages, meta={"ea_id":ea_id})


    def one_ea_all_pages(self, response):
        """ Single estate agent, with all their pages containing all their properties """

        ea_id = response.meta["ea_id"]
        num_properties = response.xpath('//span[@class="searchHeader-resultCount"]/text()').extract()
        if num_properties[0] != '0':
            page_idxs = [24*i for i in range(20) if 24*i<int(num_properties[0])]
            for page_idx in page_idxs:
                full_url = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=BRANCH%5E"+str(ea_id) + "&index=" + str(page_idx) + "&includeSSTC=true" + "&sortType=6"
                yield scrapy.Request(full_url, self.one_ea_one_page)


    def one_ea_one_page(self, response):
        """ A single page from a single estate agent """

        property_urls = response.xpath('//div[@class="propertyCard-description"]//a[@class="propertyCard-link"]/@href').extract()
        for property_url in property_urls:
            if property_url != '':
                yield response.follow(property_url, self.one_house)

    def one_house(self, response):
        """ A single house, all data collected here and passed through to MySQL server """

        script_all = response.xpath('//script').extract()
        #script_all = [i for i in script_all if "window.PAGE_MODEL" in i[0:30]]

        analytics_house = re.findall(r'(?<="analyticsProperty":).*?(?=}}})', str(script_all))
        analytics_house = json.loads(analytics_house[0] + "}")
   
        propertyId = analytics_house.get("propertyId", None)
        propertySubType = analytics_house.get("propertySubType", None)
        propertyType = analytics_house.get("propertyType", None)
        retirement = analytics_house.get("retirement", None)
        soldSTC = analytics_house.get("soldSTC", None)
        preOwned = analytics_house.get("preOwned", None)
        latitude = analytics_house.get("latitude", None)
        longitude = analytics_house.get("longitude", None)
        beds = analytics_house.get("beds", None)
        added = analytics_house.get("added", None)
        price = analytics_house.get("price", None)

        analytics_ea = re.findall(r'(?<="analyticsBranch":).*?(?=,"analyticsProperty")', str(script_all))
        analytics_ea = json.loads(analytics_ea[0])

        branchId = analytics_ea.get("branchId", None)
        brandName= analytics_ea.get("brandName", None)
        branchName = analytics_ea.get("branchName", None)
        companyName = analytics_ea.get("companyName", None)
        companyTradingName = analytics_ea.get("companyTradingName", None)
        pageType = analytics_ea.get("pageType", None)

        analytics_station = re.findall(r'(?<="nearestStations":\[).*?(?=],"showSchoolInfo")', str(script_all))
        analytics_station = re.findall(r'(?<="distance":)[.0-9]+(?=\,)', analytics_station[0])
        if analytics_station:
            closest_train = float(analytics_station[0])
        else:
            closest_train = None

        key_features = re.findall(r'(?<="keyFeatures":\[).*?(?=])', str(script_all))
        key_features = (" ").join(key_features).lower()
        garage = garden = parking = pool = 0
        if "garage" in key_features:
            garage = 1
        if "garden" in key_features:
            garden = 1
        if "parking" in key_features:
            parking = 1
        if "pool" in key_features:
            pool = 1

        bathrooms = re.findall(r'(?<="bathrooms":).*?(?=,)', str(script_all))
        try: 
            bathrooms = int(bathrooms[0])
        except:
            bathrooms = 0

        sql = "INSERT INTO `rightmove`.`buckinghamshire` \
             (propertyId, propertySubType, propertyType, retirement, soldSTC, \
                preOwned, latitude, longitude, beds, bathrooms, added, price, \
                branchId, brandName, branchName, companyName, companyTradingName, \
                pageType, closest_train, garage, garden, parking, pool) VALUES \
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        val = (propertyId, propertySubType, propertyType, retirement, soldSTC, preOwned,
               float(latitude), float(longitude), int(beds), int(bathrooms), int(added), 
               price, int(branchId), brandName, branchName, companyName, companyTradingName, 
               pageType, float(closest_train), int(garage), int(garden), int(parking), int(pool))
                
        self.mycursor.execute(sql, val)
        self.mydb.commit()

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BuckinghamshireSpider)
    process.start()
















        
        

