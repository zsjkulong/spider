import tushare as ts
import operator
from test1.Item.indexItem import indexItem
from test1.LineUtil import *
import test1.LineUtil
import datetime
class indexStock(object):
        header = ""
        indexIt = indexItem();
        def getIndex(self,excel):
            df = ts.get_index();

            headers = self.header.split(',')
            print(df);
            self.indexIt.shrate = df[operator.eq(df['name'],'上证指数')]['change'][0]
            self.indexIt.shamount = df[operator.eq(df['name'],'上证指数')]['amount'][0]

            self.indexIt.sh50rate = df[operator.eq(df['name'],'上证50')]['change'][8]
            self.indexIt.sh50amount = df[operator.eq(df['name'],'上证50')]['amount'][8]

            self.indexIt.szrate = df[operator.eq(df['name'], '深证成指')]['change'][12]
            self.indexIt.szamount = df[operator.eq(df['name'], '深证成指')]['amount'][12]

            self.indexIt.cyrate = df[operator.eq(df['name'], '创业板指')]['change'][17]
            self.indexIt.cyamount = df[operator.eq(df['code'], '399102')]['amount'][26]#新浪创业板成交额是399102的

            self.indexIt.zxrate = df[operator.eq(df['name'], '中小板指')]['change'][16]
            self.indexIt.zxamount = df[operator.eq(df['code'], '399101')]['amount'][20]

            excel.writeIndexData(self.indexIt);


class AnalysisIndexData(object):
    indexIt = indexItem();

    df = ts.get_index();

    # tup1 = ('弱势', '强势', '平衡势')
    tup2 = ('多头', '空头','多平衡','空平衡','平衡')
    tup3 = ('成交量弱势|green','成交量中','成交量强势|red')


    shlowVal = 1800;shpowerVal = 2500;
    sh50lowVal = 350;sh50powerVal = 450;
    szlowVal = 2300 ;szpowerVal = 3000
    zxlowVal = 900 ;zxpowerVal = 1100
    cylowVal = 800 ;cypowerVal = 1100

    indexDirection = '';#指数方向

    array = [];
    shhisMa5 = []; szhisMa5 = [];sh50hisMa5=[]; zxhisMa5 = [];cyhisMa5 = [];
    shhisMa10 = [];szhisMa10 = []; sh50hisMa10=[]; zxhisMa10 = []; cyhisMa10 = [];
    shhisMa20 = [];szhisMa20 = []; sh50hisMa20=[]; zxhisMa20 = []; cyhisMa20 = [];
    shDire,szDire,sh50Dire,zxDire,cyDire = '','','','',''
    shValStatus,szValStatus,sh50ValStatus,zxValStatus,cyValStatus = '', '', '', '', ''
    shStatusHit, szStatusHit, sh50StatusHit, zxStatusHit, cyStatusHit = '', '', '', '', ''
    shMACDHit,szMACDHit,sh50MACDHit,zxMACDHit,cyMACDHit  = '', '', '', '', ''
    shMACDDayHit, szMACDDayHit, sh50MACDDayHit, zxMACDDayHit, cyMACDDayHit = '', '', '', '', ''
    todayshClose,todayszClose,todaysh50Close,todaycyClose,todayzxClose = '', '', '', '', ''
    def getMa5_10_20Data(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=60)
        fromDate = (now - delta).strftime('%Y-%m-%d');
        nowDate = now.strftime('%Y-%m-%d');

        indexnow = ts.get_index()
        nowindex = 0;
        df = ts.get_k_data('sh', start=fromDate, end=nowDate);#获取历史收盘价 上证

        if(operator.eq(df.iloc[-1,0],nowDate)):#判断最新数据是否为今天
            nowindex = 0;
        else:
            nowindex = indexnow[operator.eq(indexnow['name'], '上证指数')]['close'][0];


        self.getHisData(self.array, self.shhisMa5, df['close'], 5,
                        nowindex);#获取ma5
        #print(self.shhisMa5);
        self.getHisData(self.array, self.shhisMa10, df['close'], 10,
                        nowindex);#获取ma10
        #print(self.shhisMa10);
        self.getHisData(self.array, self.shhisMa20, df['close'], 20,
                        nowindex);#获取ma20
        print(self.shhisMa20);

        df = ts.get_k_data('sz50', start=fromDate, end=nowDate);
        #print(df);
        if (operator.eq(df.iloc[-1, 0], nowDate)):
            nowindex = 0;
        else:
            nowindex = indexnow[operator.eq(indexnow['name'], '上证50')]['close'][8]

        self.getHisData(self.array, self.sh50hisMa5, df['close'], 5,
                        nowindex);
        #print(self.sh50hisMa5);
        self.getHisData(self.array, self.sh50hisMa10, df['close'], 10,
                        nowindex);
        #print(self.sh50hisMa10);
        self.getHisData(self.array, self.sh50hisMa20, df['close'], 20,
                        nowindex);
        #print(self.sh50hisMa20);

        df = ts.get_k_data('cyb', start=fromDate, end=nowDate);
        if (operator.eq(df.iloc[-1, 0], nowDate)):
            nowindex = 0;
        else:
            nowindex = indexnow[operator.eq(indexnow['name'], '创业板指')]['close'][17]

        self.getHisData(self.array, self.cyhisMa5, df['close'], 5,
                        nowindex);
        #print(self.cyhisMa5);
        self.getHisData(self.array, self.cyhisMa10, df['close'], 10,
                        nowindex);
        #print(self.cyhisMa10);
        self.getHisData(self.array, self.cyhisMa20, df['close'], 20,
                        nowindex);
        #print(self.cyhisMa20);

        df = ts.get_k_data('zxb', start=fromDate, end=nowDate);

        if (operator.eq(df.iloc[-1, 0], nowDate)):
            nowindex = 0;
        else:
            nowindex = indexnow[operator.eq(indexnow['name'], '中小板指')]['close'][16]

        self.getHisData(self.array, self.zxhisMa5, df['close'], 5,
                        nowindex);
        #print(self.zxhisMa5);
        self.getHisData(self.array, self.zxhisMa10, df['close'], 10,
                        nowindex);
        #print(self.zxhisMa10);
        self.getHisData(self.array, self.zxhisMa20, df['close'], 20,
                        nowindex);
        #print(self.zxhisMa20);


        df = ts.get_k_data('sz', start=fromDate, end=nowDate);
        if (operator.eq(df.iloc[-1, 0], nowDate)):
            nowindex = 0;
        else:
            nowindex = indexnow[operator.eq(indexnow['name'], '深证成指')]['close'][12]

        self.getHisData(self.array, self.szhisMa5, df['close'], 5,
                        nowindex);
        #print(self.szhisMa5);
        self.getHisData(self.array, self.szhisMa10, df['close'], 10,
                        nowindex);
        #print(self.szhisMa10);
        self.getHisData(self.array,self.szhisMa20, df['close'],20,
                        nowindex);
        #print(self.szhisMa20);

    def analysisIndexData(self):
        self.getMa5_10_20Data();
        self.shDire = self.getIndexDire(self.shhisMa20);
        self.szDire = self.getIndexDire(self.szhisMa20);
        self.cyDire = self.getIndexDire(self.cyhisMa20);
        self.zxDire = self.getIndexDire(self.zxhisMa20);
        self.sh50Dire = self.getIndexDire(self.sh50hisMa20);

        self.analysisTodayValAndDire();

        self.analysisTodayMACD();



        print(self.shDire+','+self.szDire +','+self.cyDire+','+self.zxDire+','+self.sh50Dire)
        print(self.shValStatus+','+self.szValStatus +','+self.sh50ValStatus+','+self.cyValStatus+','+self.zxValStatus)
        print(
            self.shStatusHit + ',' + self.szStatusHit + ',' + self.sh50StatusHit + ',' + self.cyStatusHit + ',' + self.zxStatusHit)
        print(self.shMACDHit+','+self.szMACDHit+','+self.sh50MACDHit+','+self.cyMACDHit+','+self.zxMACDHit)
        print(
            self.shMACDDayHit+','+self.szMACDDayHit+','+self.sh50MACDDayHit+','+self.zxMACDDayHit+','+self.cyMACDDayHit)

    def analysisTodayMACD(self):
        #print(self.df);
        self.todayshClose = self.df[operator.eq(self.df['name'], '上证指数')]['close'][0];
        self.todayszClose = self.df[operator.eq(self.df['name'], '深证成指')]['close'][12];
        self.todaysh50Close = self.df[operator.eq(self.df['name'], '上证50')]['close'][8];
        self.todaycyClose = self.df[operator.eq(self.df['name'], '创业板指')]['close'][17];
        self.todayzxClose = self.df[operator.eq(self.df['name'], '中小板指')]['close'][16];

        todayshhigh = self.df[operator.eq(self.df['name'], '上证指数')]['high'][0];
        todayszhigh = self.df[operator.eq(self.df['name'], '深证成指')]['high'][12];
        todaysh50high = self.df[operator.eq(self.df['name'], '上证50')]['high'][8];
        todaycyhigh = self.df[operator.eq(self.df['name'], '创业板指')]['high'][17];
        todayzxhigh = self.df[operator.eq(self.df['name'], '中小板指')]['high'][16];

        todayshlow = self.df[operator.eq(self.df['name'], '上证指数')]['low'][0];
        todayszlow  = self.df[operator.eq(self.df['name'], '深证成指')]['low'][12];
        todaysh50low  = self.df[operator.eq(self.df['name'], '上证50')]['low'][8];
        todaycylow  = self.df[operator.eq(self.df['name'], '创业板指')]['low'][17];
        todayzxlow  = self.df[operator.eq(self.df['name'], '中小板指')]['low'][16];

        self.shMACDHit = self.getMACDHit(self.shhisMa5,self.shhisMa20);
        self.szMACDHit = self.getMACDHit(self.szhisMa5, self.szhisMa20);
        self.sh50MACDHit = self.getMACDHit(self.sh50hisMa5, self.sh50hisMa20);
        self.zxMACDHit = self.getMACDHit(self.zxhisMa5, self.zxhisMa20);
        self.cyMACDHit = self.getMACDHit(self.cyhisMa5, self.cyhisMa20);

        # 当日价触碰20日均线。
        if(operator.eq(self.shDire,'多头') or operator.eq(self.shDire,'多平衡')):
            self.shMACDDayHit = self.getMACDHitDay(todayshlow,self.shhisMa20,self.shDire,self.shhisMa5)
        elif(operator.eq(self.shDire,'空头') or operator.eq(self.shDire,'空平衡')):
            self.shMACDDayHit = self.getMACDHitDay(todayshhigh, self.shhisMa20, self.shDire,self.shhisMa5)

        if (operator.eq(self.szDire, '多头') or operator.eq(self.szDire, '多平衡')):
            self.szMACDDayHit = self.getMACDHitDay(todayszlow, self.shhisMa20, self.szDire,self.szhisMa5)
        elif (operator.eq(self.szDire, '空头') or operator.eq(self.szDire, '空平衡')):
            self.szMACDDayHit = self.getMACDHitDay(todayszhigh, self.szhisMa20, self.szDire,self.szhisMa5)

        if (operator.eq(self.sh50Dire, '多头') or operator.eq(self.sh50Dire, '多平衡')):
            self.sh50MACDDayHit = self.getMACDHitDay(todaysh50low, self.sh50hisMa20, self.sh50Dire,self.sh50hisMa5)
        elif (operator.eq(self.sh50Dire, '空头') or operator.eq(self.sh50Dire, '空平衡')):
            self.sh50MACDDayHit = self.getMACDHitDay(todaysh50high, self.sh50hisMa20, self.sh50Dire,self.sh50hisMa5)

        if (operator.eq(self.zxDire, '多头') or operator.eq(self.zxDire, '多平衡')):
            self.zxMACDDayHit = self.getMACDHitDay(todayzxlow, self.zxhisMa20, self.zxDire,self.zxhisMa5)
        elif (operator.eq(self.zxDire, '空头') or operator.eq(self.zxDire, '空平衡')):
            self.zxMACDDayHit = self.getMACDHitDay(todayzxhigh, self.zxhisMa20, self.zxDire,self.zxhisMa5)

        if (operator.eq(self.cyDire, '多头') or operator.eq(self.cyDire, '多平衡')):
            self.cyMACDDayHit = self.getMACDHitDay(todaycylow, self.cyhisMa20, self.cyDire,self.cyhisMa5)
        elif (operator.eq(self.zxDire, '空头') or operator.eq(self.zxDire, '空平衡')):
            self.cyMACDDayHit = self.getMACDHitDay(todaycyhigh, self.cyhisMa20, self.cyDire,self.cyhisMa5)



    def analysisTodayValAndDire(self):

        # df = ts.get_index();

        shamount = self.df[operator.eq(self.df['name'], '上证指数')]['amount'][0]
        sh50amount = self.df[operator.eq(self.df['name'], '上证50')]['amount'][8]
        szamount = self.df[operator.eq(self.df['name'], '深证成指')]['amount'][12]
        cyamount = self.df[operator.eq(self.df['code'], '399102')]['amount'][26]  # 新浪创业板成交额是399102的
        zxamount = self.df[operator.eq(self.df['name'], '中小板指')]['amount'][16]

        shrate = self.df[operator.eq(self.df['name'], '上证指数')]['change'][0]
        sh50rate = self.df[operator.eq(self.df['name'], '上证50')]['change'][8]
        szrate = self.df[operator.eq(self.df['name'], '深证成指')]['change'][12]
        cyrate = self.df[operator.eq(self.df['name'], '创业板指')]['change'][17]
        zxrate = self.df[operator.eq(self.df['name'], '中小板指')]['change'][16]


        # shlowVal = 1800;
        # shpowerVal = 2500;
        # sh50lowVal = 300;
        # sh50powerVal = 400;
        # szlowVal = 2300;
        # szpowerVal = 3000
        # zxlowVal = 900;
        # zxlowVal = 1300
        # cylowVal = 800;
        # cypowerVal = 1100
        self.shValStatus = self.getValStatus(shamount,self.shlowVal,self.shpowerVal);
        self.szValStatus = self.getValStatus(szamount, self.szlowVal, self.szpowerVal);
        self.sh50ValStatus = self.getValStatus(sh50amount, self.sh50lowVal, self.sh50powerVal);
        self.cyValStatus = self.getValStatus(cyamount, self.cylowVal, self.cypowerVal);
        self.zxValStatus = self.getValStatus(zxamount, self.zxlowVal, self.zxpowerVal);

        self.shStatusHit = self.getTodayStatusHit(self.shDire,self.shValStatus,shrate)
        self.szStatusHit = self.getTodayStatusHit(self.szDire, self.szValStatus, szrate)
        self.sh50StatusHit = self.getTodayStatusHit(self.sh50Dire, self.sh50ValStatus, sh50rate)
        self.cyStatusHit = self.getTodayStatusHit(self.cyDire, self.cyValStatus, cyrate)
        self.zxStatusHit = self.getTodayStatusHit(self.zxDire, self.zxValStatus, zxrate)


    def getValStatus(self,amount,low,power):
        if(amount<low):
            return self.tup3[0];
        if(amount>=low and amount <power):
            return self.tup3[1];
        if(amount>=power):
            return self.tup3[2];

    def getMACDHit(self,ma5array,ma20array):
        MACDHit = '';
        if (ma5array[0] < ma20array[15]
                and ma5array[1] < ma20array[16]
                and ma5array[2] < ma20array[17]
                and ma5array[3] < ma20array[18]
                and ma5array[4] >= ma20array[19]):
            MACDHit = 'MA5金叉MA20|red';
        elif (ma5array[0] > ma20array[15]
              and ma5array[1] > ma20array[16]
              and ma5array[2] > ma20array[17]
              and ma5array[3] > ma20array[18]
              and ma5array[4] <= ma20array[19]):
            MACDHit = 'MA5死叉MA20|green';

        return MACDHit;

    def getMACDHitDay(self,dayK,ma20array,dire,ma5array):
        MACDHit = '';
        if(operator.eq(dire,'多头') or operator.eq(dire,'多平衡')):
            if ( ma5array[0]> ma20array[14]
                   and ma5array[1] > ma20array[15]
                   and ma5array[2] > ma20array[16]
                   and ma5array[3] > ma20array[17]
                    and ma5array[4] > ma20array[18]
                   and dayK <= ma20array[19]):
                MACDHit = '今日股价回踩20日均线|blue';
        elif(operator.eq(dire,'空头') or operator.eq(dire,'空平衡')):
            if ( ma5array[0]< ma20array[14]
                   and ma5array[1] < ma20array[15]
                   and ma5array[2] < ma20array[16]
                   and ma5array[3] < ma20array[17]
                    and ma5array[4] < ma20array[18]
                   and dayK >= ma20array[19]):
                MACDHit = '今日股价上探20日均线|green';
        return MACDHit;

    def getTodayStatusHit(self,dire,valstatus,rate):
        statusHit = '';
        if (operator.eq('多头', dire) and operator.eq(self.tup3[0], valstatus) and rate > 0):
            statusHit = '观察持有股票上涨是否持续，仓位不动'
        elif (operator.eq('多头', dire) and operator.eq(self.tup3[0], valstatus) and rate < 0):
            statusHit = '可能回调，仓位不动'
        elif (operator.eq('多头', dire) and operator.eq(self.tup3[2], valstatus) and rate > 0):
            statusHit = '寻找多个领涨板块多个领涨股买入或者加仓，加仓|red'
        elif (operator.eq('多头', dire) and operator.eq(self.tup3[2], valstatus) and rate < 0):
            statusHit = '是否是上涨过程中第一次回调？仓位无建议'
        else:
            print()

        if (operator.eq('多平衡', dire) and operator.eq(self.tup3[0], valstatus) and rate > 0):
            statusHit = '只持有单一上涨板块个股，可能即将回调，仓位不变'
        elif (operator.eq('多平衡', dire) and operator.eq(self.tup3[0], valstatus) and rate < 0):
            statusHit = '回调开始，注意支撑位低吸，减仓|green'
        elif (operator.eq('多平衡', dire) and operator.eq(self.tup3[2], valstatus) and rate > 0):
            statusHit = '持有单一上涨板块个股，加仓|red'
        elif (operator.eq('多平衡', dire) and operator.eq(self.tup3[2], valstatus) and rate < 0):
            statusHit = '回调开始，注意支撑位能否支撑，减仓|green'
        else:
            print();


        if (operator.eq('空平衡', dire) and operator.eq(self.tup3[0], valstatus) and rate < 0):
            statusHit = '板块分化，持有均线多头防御（白酒医药）板块板块，持有多头个股，3分之一或者空仓'
        elif (operator.eq('空平衡', dire) and operator.eq(self.tup3[2], valstatus) and rate < 0):
            statusHit = '板块分化，持有均线多头防御（白酒医药）板块，持有多头个股，3分之一或者空仓'
        elif (operator.eq('空平衡', dire) and operator.eq(self.tup3[2], valstatus) and rate > 0):
            statusHit = '注意是否突破，继续板块是否继续上涨，1/3金额短线操作，不变或者加仓'
        elif (operator.eq('空平衡', dire) and operator.eq(self.tup3[0], valstatus) and rate > 0):
            statusHit = '持有均线多头防御（白酒医药）板块，持有多头个股，3分之一'
        else:
            print()

        if (operator.eq('空头', dire) and operator.eq(self.tup3[2], valstatus) and rate < 0):
            statusHit = '观察优质股是否跌出价值坑，空仓'
        elif (operator.eq('空头', dire) and operator.eq(self.tup3[0], valstatus) and rate < 0):
            statusHit = '观察优质股是否跌出价值坑，空仓'
        elif (operator.eq('空头', dire) and operator.eq(self.tup3[2], valstatus) and rate > 0):
            statusHit = '观察是否反弹，短线操作1/4资金博反弹快入快出，切勿追高|blue'
        elif (operator.eq('空头', dire) and operator.eq(self.tup3[0], valstatus) and rate > 0):
            statusHit = '观察是否反弹，空仓'
        else:
            statusHit = '空仓'

        return statusHit

    def getIndexDire(self,array): #通过ma20分析均线上涨还是下降

        var = getLineK(array);
        # tup2 = ('多头', '空头','多平衡','空平衡','平衡')
        if(var > 1):
            return self.tup2[0];
        elif(var >0.5 and var <=1):
            return self.tup2[2];
        elif (var < -1):
            return self.tup2[1];
        elif (var > -1 and var < -0.5):
            return self.tup2[3];
        else:
            return self.tup2[4];



    def getHisData(self,array,maarray,data,count,today):
        for str in data:
            array.append(str);
        if(today>0):
            array.append(today)
        array.reverse();
        for i in range(0,count):
            sum = float(array[i]);
            for j in range(i+1,count+i):
                sum += float(array[j])
            maarray.append(round(sum/count,2));
        maarray.reverse();



# getHisData = AnalysisIndexData();
# getHisData.analysisIndexData();