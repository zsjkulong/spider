import scrapy
import operator
from test1.Item.uptopItem import uptopItem
from test1.excelUtil import excelUtil
class EastmoneySpider(scrapy.spiders.Spider):
    name="eastmoney";
    allow_domains = ["eastmoney.com"];
    excelUtil = excelUtil();
    yesterdayCode = [];
    beforeYesterdayCode = [];
    #i = 0;
    def start_requests(self):
        self.yesterdayCode = excelUtil.readYesterday(excelUtil,0)
        self.beforeYesterdayCode = excelUtil.readBeforeYesterday(excelUtil,0)
        urls = [
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKGN&type=ct&st=(ChangePercent)&sr=-1&p=1&ps=500&js=var%20zGVqneVk={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=50939525',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse);


    def parse(self, response):
        str = response.body_as_unicode();
        strindex = str.index('"')
        str = str[strindex+1:len(str)];
        print(str);
        i = 0
        for box in str.split('","')[0:3]:
            item = uptopItem()
            print('box:'+box);
            #print('sdfs'+ box.split(',')[1]);
            item['code'] = box.split(',')[1];
            item['title']= box.split(',')[2];
            item['upRate'] = box.split(',')[3];
            item['amount'] = box.split(',')[4];


            for bx in str.split('","'):
                vars = bx.split(',');
                if(len(self.yesterdayCode)==0):
                    item['ycode'] = 'NA'
                    item['ytitle'] = 'NA';
                    item['yupRate'] = '';
                    item['yamount'] = '';
                    break;
                if(operator.eq(vars[1],self.yesterdayCode[i])):
                    item['ycode'] = vars[1]
                    item['ytitle'] = vars[2];
                    item['yupRate'] = vars[3];
                    item['yamount'] = vars[4];
                    break;

            for bx in str.split('","'):
                vars = bx.split(',');
                if (len(self.beforeYesterdayCode) == 0):
                    item['bycode'] = 'NA';
                    item['bytitle'] = 'NA';
                    item['byupRate'] = '';
                    item['byamount'] = '';
                    break;
                if(operator.eq(vars[1],self.beforeYesterdayCode[i])):
                    item['bycode'] = vars[1];
                    item['bytitle'] = vars[2];
                    item['byupRate'] = vars[3];
                    item['byamount'] = vars[4];
                    break;


            i+=1;
            yield item;
