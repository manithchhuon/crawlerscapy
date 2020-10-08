import scrapy
import os

class CneSpider(scrapy.Spider):
    name = 'cne'
    start_urls = ['https://cne.wtf/2020/10/08/cintri-worker-strike-continues-despite-negotiations/']
    current_url = ""
    url_eng_file_path = "/home/mono/Documents/RND/crawler/data/eng/eng_url.txt"
    url_eng_no_source_file_path = "/home/mono/Documents/RND/crawler/data/eng/no_source.txt"
    url_khm_file_path = "/home/mono/Documents/RND/crawler/data/khm/khm_url.txt"
    url_eng_content="/home/mono/Documents/RND/crawler/data/eng/"
    url_eng_content_no_source="/home/mono/Documents/RND/crawler/data/eng/nosource/"
    eng_lines=[]
    
    
    def parse(self, response):
        self.eng_lines = self.storeInList(self.url_eng_file_path)
        self.eng_last_num = self.getLastNum(self.url_eng_file_path)
        contenteng = "";
        for category in response.css('.above-entry-meta'):
            contenteng = str(self.listToString(category.css('a::text').extract(),',')) + ";"
        #     yield {'category':category.css('a::text').extract()}
        for content in response.css('.entry-content'):
            contenteng = contenteng+str(self.listToString(content.css('p ::text').extract(),"------"))+"\n"
        #     yield {'content': content.css('p ::text').extract()}
            # yield {'next': content.css('p>a::attr(href)').get()}

        km_source = response.css('.entry-content>p>a::attr(href)').get()

        if ((self.eng_last_num==0) or (not self.checkInList(response.url,self.eng_lines))):
            
            self.eng_last_num = self.eng_last_num + 1
            if km_source:
                furleng = open(self.url_eng_file_path,"a+")
                furleng.write(str(self.eng_last_num)+';'+response.url+';none\n')
            
                furlkhm = open(self.url_khm_file_path,"a+")
                furlkhm.write(str(self.eng_last_num)+';'+km_source+';none\n')

                fcontenteng = open(self.url_eng_content+"eng_"+str(self.eng_last_num)+".csv","w+")
                fcontenteng.write(contenteng)
            else:
                furleng = open(self.url_eng_no_source_file_path,"a+")
                furleng.write(str(self.eng_last_num)+';'+response.url+';none\n')

                fcontenteng = open(self.url_eng_content_no_source+"eng_"+str(self.eng_last_num)+".csv","w+")
                fcontenteng.write(contenteng)

        for next_page in response.css('li.previous>a'):
            yield response.follow(next_page, self.parse)

    def parse_item(self, response):
        # parse item here
        self.state['items_count'] = self.state.get('items_count', 0) + 1

    def listToString(self,s,c):
        str1 = c
        return (str1.join(s))

    def checkEmptyFile(self,file_name):
        return os.stat(file_name).st_size==0
    
    def checkInList(self,str,clists):
        return (str in clists)
    
    def storeInList(self,file_name):
        url_lists=[]
        if not (self.checkEmptyFile(file_name)):
            with open(file_name) as engfile:
                for line in engfile:
                    url_lists.append(line.split(';')[1])
        return url_lists
    
    def getLastNum(self,file_name):
        eng_last_num=0
        if not self.checkEmptyFile(file_name):
            with open(file_name, 'r') as f_read:
                eng_last_line = f_read.readlines()[-1]
                eng_last_num= eng_last_line.split(';')[0]
        return int(eng_last_num)