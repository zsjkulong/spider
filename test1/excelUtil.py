import openpyxl
import datetime
import operator
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, Fill,PatternFill
from openpyxl.cell import Cell
class excelUtil:
    sheetName = '每日领涨概念板块'
    path = 'D:/stock.xlsx'
    numberOfGet = 5;
    yesterdayNumber = numberOfGet*1;
    beforeYesterdayNumber = numberOfGet*2;
    #exit = ['BK0815','BK0816']
    color = 'FFEEE8AA';

    #startRows = 0;

    def top3GaiNianBanKuai(self,item,startRow):#设置item的值到excel中
        #print(item);
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name(self.sheetName)
        sheet['B'+str(startRow)] = item['title']
        sheet['C' + str(startRow)] = item['code']
        self.setValAndFontColor(sheet['D' + str(startRow)],item['upRate'])
        self.setValAndFontColor(sheet['E' + str(startRow)], item['amount'])
        sheet['F' + str(startRow)] = item['ytitle']
        sheet['G' + str(startRow)] = item['ycode']
        self.setValAndFontColor(sheet['H' + str(startRow)],item['yupRate']);
        self.setValAndFontColor(sheet['I' + str(startRow)],item['yamount']);
        sheet['J' + str(startRow)] = item['bytitle']
        sheet['K' + str(startRow)] = item['bycode']
        self.setValAndFontColor(sheet['L' + str(startRow)],item['byupRate'])
        self.setValAndFontColor(sheet['M' + str(startRow)],item['byamount'])
        wb.save(self.path)
        #print("写入数据成功！")


    def makeSheetAndHeader(self):#写excel的header
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = self.sheetName
        sheet.merge_cells('B1:E1')
        sheet['B1'] = '当日领涨板块';sheet['B2'] = '板块名称';sheet['C2'] = '板块编码';sheet['D2'] = '涨幅';sheet['E2'] = '主力金额'
        sheet.merge_cells('F1:I1')
        sheet['F1'] = '昨日领涨板块';sheet['F2'] = '板块名称';sheet['G2'] = '板块编码';sheet['H2'] = '涨幅';sheet['I2'] = '主力金额'
        sheet.merge_cells('J1:M1')
        sheet['J1'] = '前日领涨板块';sheet['J2'] = '板块名称';sheet['K2'] = '板块编码';sheet['L2'] = '涨幅';sheet['M2'] = '主力金额'
        sheet['A2'] = '日期'
        wb.save(self.path)


    def readExcelRows(self):#获取excel的行数
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name(self.sheetName)
        return sheet.max_row+1;
        # sheet.get

    def readYesterday(self,startRowin):#读取昨天数据
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name(self.sheetName)
        if(startRowin and startRowin>0):
            startRow = startRowin;
        else:
            startRow = sheet.max_row+1
        list = [];
        if(startRow<=self.yesterdayNumber):
            return list;
        for cell in sheet['C'+str(startRow-self.yesterdayNumber):'C'+str(startRow-1)]:
            #print(cell[0].value);
            list.append(cell[0].value)
        print(list);
        return list;

    def readBeforeYesterday(self,startRowin):#读取前天数据
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name(self.sheetName)
        if (startRowin and startRowin > 0):
            startRow = startRowin;
        else:
            startRow = sheet.max_row + 1
        list = [];
        if (startRow <= self.beforeYesterdayNumber):
            return list;
        for cell in sheet['C' + str(startRow - self.beforeYesterdayNumber):'C' + str(startRow - 1 - self.yesterdayNumber)]:
            # print(cell[0].value);
            list.append(cell[0].value)
        #print(list);
        return list;

    def writerDate(self):#写日期
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name(self.sheetName)
        startRow = self.readExcelRows();
        mergeCell = 'A' + str(startRow - self.numberOfGet)+':A' + str(startRow - 1);
        sheet.merge_cells(mergeCell);
        sheet['A' + str(startRow - self.numberOfGet)] = datetime.datetime.now().strftime('%Y-%m-%d')
        wb.save(self.path)

    def setValAndFontColor(self,cell,val):#根据数字正负设置红绿
        if(operator.eq(val,'')):
            cell.value = val;
            return;

        if(float(val) > 0):
            ft = Font(color=colors.RED)
            cell.font = ft;
        elif(float(val) < 0):
            ft = Font(color=colors.GREEN)
            cell.font = ft;
        else:
            ft = Font(color=colors.BLACK)
            cell.font = ft;
        cell.value = val;


    def setCellColor(self):#设置隔一天数据的颜色
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name(self.sheetName)
        startRow = self.readExcelRows();
        #i = 0
        if(startRow%2==0):
            for cells in sheet['A'+str(startRow-self.numberOfGet):'M'+str(startRow-1)]:
                for cell in cells:
                    cell.fill = PatternFill(fill_type='solid',fgColor=self.color)
                    #i += 1;
        #sheet['B' + str(startRow - 2):'M' + str(startRow - 1)].style.fill.start_color.index = Color.DARKBLUE;
        wb.save(self.path);
        #cell.style.fill.fill_type = Fill.FILL_SOLID
        #cell.style.fill.start_color.index = Color.DARKBLUE;

    def makeItRed(self):#标记重复上榜的数据为红色或者紫色
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name(self.sheetName)
        startRow  = sheet.max_row +1;
        yesterday = self.readYesterday(startRow-self.numberOfGet);
        beforeYesterday = self.readBeforeYesterday(startRow-self.numberOfGet);
        if (len(yesterday)==0):
            return;
        if(len(beforeYesterday)==0):
            return;

        i = self.numberOfGet;
        for cells in sheet['C' + str(startRow - self.numberOfGet):'C' + str(startRow - 1)]:
            if( cells[0].value in yesterday and  cells[0].value in beforeYesterday):
                ft = Font(color=colors.RED)
                sheet['B'+str(startRow - i)].font = ft;
            elif(cells[0].value in yesterday  or  cells[0].value in beforeYesterday):
                ft = Font(color='FF9932CC')
                sheet['B' + str(startRow - i)].font = ft;
            else:
                i -= 1;
                continue;
            i-=1;
        wb.save(self.path);