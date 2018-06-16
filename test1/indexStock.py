import tushare as ts
import operator
from test1.Item.indexItem import indexItem

class indexStock(object):
        header = ""

        def getIndex(self,excel):
            df = ts.get_index();
            indexIt = indexItem();
            headers = self.header.split(',')
            print(df);
            indexIt.shrate = df[operator.eq(df['name'],'上证指数')]['change'][0]
            indexIt.shamount = df[operator.eq(df['name'],'上证指数')]['amount'][0]

            indexIt.sh50rate = df[operator.eq(df['name'],'上证50')]['change'][8]
            indexIt.sh50amount = df[operator.eq(df['name'],'上证50')]['amount'][8]

            indexIt.szrate = df[operator.eq(df['name'], '深证成指')]['change'][12]
            indexIt.szamount = df[operator.eq(df['name'], '深证成指')]['amount'][12]

            indexIt.cyrate = df[operator.eq(df['name'], '创业板指')]['change'][17]
            indexIt.cyamount = df[operator.eq(df['code'], '399102')]['amount'][26]#新浪创业板成交额是399102的

            indexIt.zxrate = df[operator.eq(df['name'], '中小板指')]['change'][16]
            indexIt.zxamount = df[operator.eq(df['name'], '中小板指')]['amount'][16]

            excel.writeIndexData(indexIt);


