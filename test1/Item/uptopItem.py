import scrapy

class uptopItem(scrapy.Item):

    #是否是概念板块
    isConcept = scrapy.Field();

    #板块名称
    title = scrapy.Field();
    #编号
    code = scrapy.Field();
    #增长率
    upRate = scrapy.Field();
    #成交量
    vol = scrapy.Field();
    #主力流入金额
    amount = scrapy.Field();

    # 昨天领涨板块名称
    ytitle = scrapy.Field();
    # 昨天编号
    ycode = scrapy.Field();
    # 昨天增长率
    yupRate = scrapy.Field();
    # 昨天成交量
    yvol = scrapy.Field();
    # 昨天主力流入金额
    yamount = scrapy.Field();

    # 前天领涨板块名称
    bytitle = scrapy.Field();
    # 前天编号
    bycode = scrapy.Field();
    # 前天增长率
    byupRate = scrapy.Field();
    # 前天成交量
    byvol = scrapy.Field();
    # 前天主力流入金额
    byamount = scrapy.Field();



