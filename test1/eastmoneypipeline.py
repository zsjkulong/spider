import os
from test1.excelUtil import excelUtil
class eastmoneypipeline(object):
    excel = excelUtil();
    def __init__(self):
        if(os.path.exists(self.excel.path)==False):
            self.excel.makeSheetAndHeader()


    def process_item(self, item, spider):
        #path = 'data/2003.xls';
        print(item)
        startRow = self.excel.readExcelRows()
        #print(self.startRows)
        self.excel.top3GaiNianBanKuai(item,startRow);
        return item

    def close_spider(self, spider):
        self.excel.writerDate(); #写入日期
        self.excel.setCellColor(); #修改隔一行的颜色，方便阅读
        self.excel.makeItRed();#把今日涨幅前3的板块与昨日前日匹配，如果在昨日前日中都出现就把字体显示为红色，如果只是在前日昨日中出现一次就显示紫色


