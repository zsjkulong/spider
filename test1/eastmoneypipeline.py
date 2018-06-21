import os
from test1.excelUtil import excelUtil
from test1.indexStock import indexStock
import configparser
import operator
class eastmoneypipeline(object):
    excel = excelUtil();
    index = indexStock();
    def __init__(self):
        self.readConfig(self.excel, self.index)
        if(os.path.exists(self.excel.path)==False):
            self.excel.makeSheetAndHeader()
        self.index.getIndex(self.excel);



    def process_item(self, item, spider):
        #path = 'data/2003.xls';
        #print(item)
        startRow=0;
        if(operator.eq(item['isConcept'],'true')):
            startRow = self.excel.readExcelRows(1)
        else:
            startRow = self.excel.readExcelRows(2)
        #print(self.startRows)
        self.excel.topN(item,startRow);
        return item

    def close_spider(self, spider):
        self.excel.writerDate(); #写入日期
        self.excel.setCellColor(); #修改隔一行的颜色，方便阅读
        self.excel.makeItRed();#把今日涨幅前3的板块与昨日前日匹配，如果在昨日前日中都出现就把字体显示为红色，如果只是在前日昨日中出现一次就显示紫色



    def readConfig(self,excel,index):
        cf = configparser.ConfigParser()
        cf.read('config.ini',encoding="utf-8-sig")
        excel.numberOfGet = cf.getint('config', 'numberOfGet')
        excel.path = cf.get('config', 'path')
        index.header = cf.get('config', 'indexname')