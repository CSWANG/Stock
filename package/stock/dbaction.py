#-*- coding: utf-8 -*-

#standoard package and module load
import os
import sqlite3
import sys
import traceback
import datetime

from package.stock import configload
from package.stock import stocklog

#config load
cfg = configload.loadcfg()

#log initial
dblog = stocklog.dbloginitial(cfg)


def connectDB():
    try:
        dbfilename = cfg['DatabaseInfo']['dbfilename']
        dbfilepath = './' + cfg['path']['dbPath'] + '/' + dbfilename
        conn = sqlite3.connect(dbfilepath)
        return conn
    except:
        dblog.error('資料庫連結失敗')
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())


def checkTableisExist(table_name):
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('PRAGMA table_info({})'.format(table_name))
    data = curs.fetchall()
    return data


'''-----------create start-----------'''

def createTable_DailyQuotes():
    conn = connectDB()
    curs = conn.cursor()
    try:
        curs.execute('''CREATE TABLE dailyQuotes
            (StockDate VARCHAR(8) not null,
            SecurityCode VARCHAR(10) not null,
            StockName VARCHAR(20),
            TradingVolume INT,
            TransAmount INT,
            TradingValue INT,
            OpenPrice decimal(5,2),
            HighestPrice decimal(5,2),
            LowestPrice decimal(5,2),
            ClosingPrice decimal(5,2),
            Dir char(1),
            Change decimal(5,2),
            LastBestBidPrice decimal(5,2),
            LastBestBidVolume INT,
            LastBestAskPrice decimal(5,2),
            LastBestAskVolume INT,
            PriceEarningRatio decimal(5,2),
            primary key(stockDate,SecurityCode))''')
    except Exception:
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()

def createTable_stockIndustryType():
    conn = connectDB()
    curs = conn.cursor()
    try:
        curs.execute('''CREATE TABLE stockCategoryType (
                    categorytypename TEXT)''')
    except Exception:
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()

def createTable_simpledailyquotes():
    conn = connectDB()
    curs = conn.cursor()
    try:
        curs.execute('''CREATE TABLE simpledailyquoates (
                        stockdate TEXT,
                        stockid   INTEGER,
                        tradingvolume INTEGER,
                        tradingamount INTEGER,
                        openprice decimal(5.2),
                        closeprice decimal(5.2),
                        highestprice decimal(5.2),
                        lowestprice decimal(5.2),
                        primary key (stockdate,stockid))''')
    except Exception:
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()

def createTable_analysisdata():
    conn = connectDB()
    curs = conn.cursor()
    try:
        curs.execute('''CREATE TABLE analysisdata (
                        'analysistype' TEXT,
                        'stockid varchar(10),
                        'createdate TEXT,
                        'pricedate' TEXT,
                        'maprice' decimal(5,2),
                        'sigma1' INTEGER,
                        'sigma2' INTEGER)''')
    except Exception:
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()

'''-----------create end------------'''

'''-----------query start-----------'''

def queryDailyQuites():
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('''select * from DailyQuotes''')
    row = curs.fetchall()


def qStockIndustryType(value):
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('''select * from stockIndustryType
                 where industryName = ?''',(value,))
    if len(curs.fetchall()) == 0:
        return False
    else:
        dblog.info('已有重覆紀錄：' + str(value))
        return True

def qStockMaster(value):
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('''select * from stockMaster
                 where stockid = ?''', (value[0],))
    if len(curs.fetchall()) == 0:
        return False
    else:
        dblog.info('已有重覆紀錄：' + str(value))
        return True

def qGetAllStock():
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('''select stockid from stockMaster''')
    row = curs.fetchall()
    return row

def qGetAllStockByCategoryType(value):
    conn = connectDB()
    curs = conn.cursor()
    data = []
    trecord = [value,]
    curs.execute('''select a.stockid from stockMaster as a
                    inner join stockCategoryType as c
                    on a.stockindustrytypeid = c.categoryTypeid
                    where c.categoryTypeid = ? ''',trecord)
    row = curs.fetchall()
    for i in row :
        data.append(str(i[0]))
    return data

def qGetMarketAll(value):
    conn = connectDB()
    curs = conn.cursor()
    data = []
    trecord = [value,]
    curs.execute('''select stockdate,stockid from simpledailyquotes
                    where stockid = ? ''',trecord)
    row = curs.fetchall()

    return row


def qStockHolderListByMonthly(value):
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('''select * from stockdirectorholder
                 where year = ?
                 and month = ?
                 and holdername = ?
                 and holdertype = ?
                 and holdstockquantity = ?
                 and pledgequantity = ?
                 and pledgeratio = ?
                 and stockid = ?''', value)
    if len(curs.fetchall()) == 0:
        return False
    else:
        dblog.info('已有重覆紀錄：' + str(value))
        return True

def qStockHolderListByMonthlyId(value):
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('''
    select stockid from stockdirectorholder
    where stockid = ?''', value)
    if len(curs.fetchall()) == 0:
        return False
    else:
        dblog.info('已有重覆紀錄：' + str(value))
        return True


def qStockIndustryIdByName(value):
    conn = connectDB()
    curs = conn.cursor()
    trecord = [value,]
    curs.execute('''
    select industrytypeid from stockindustrytype
    where industryname = ?''', trecord)
    row = curs.fetchall()
    if len(row) == 0:
        return 0
    else:
        return row[0][0]

def qGetMaxIndustryID():
    conn = connectDB()
    curs = conn.cursor()
    curs.execute('''
    select max(industrytypeid) from stockindustrytype''')
    row = curs.fetchall()
    if row[0][0] is None:
        return 1
    else:
        return row[0][0] + 1

def qGetLastDateDataByStockId(value):
    conn = connectDB()
    curs = conn.cursor()
    trecord = [value, ]
    curs.execute('''
    select max(stockdate) from simpledailyquotes
    where stockid = ?''',trecord)
    row = curs.fetchall()
    if row[0][0] is None:
        return None
    else:
        lastdate_tmp = row[0][0].split(sep='/')
        lastdate_str = str(int(lastdate_tmp[0])+1911) +str(lastdate_tmp[1]) + str(lastdate_tmp[2]) +' 00:00:00'
        lastdate = datetime.datetime.strptime(lastdate_str,'%Y%m%d %H:%M:%S').date()
        return lastdate

def qGetPeriodHistoryClosePriceByStockNo(value,period=365):
    conn = connectDB()
    curs = conn.cursor()
    today = datetime.datetime.today().date()
    to_date = today - datetime.timedelta(days=365)
    to_date = str(to_date.year - 1911) + '/' + str(to_date.month).zfill(2) + '/' + str(to_date.day).zfill(2)
    trecord = [value,to_date]
    curs.execute('''
        select stockdate,closeprice from simpledailyquotes
        where stockid = ?
        and stockdate >= ? order by stockdate Desc''', trecord)
    row = curs.fetchall()
    return row

'''-----------query end-----------'''

'''-----------insert start-----------'''


def insertDailyQuotes(record):
    conn = connectDB()
    curs = conn.cursor()

    '''    if checkTableisExist('dailyQuotes'):
        pass
    else:
        createTable_DailyQuotes()'''
    try:
        trecord = tuple(record)
        curs.execute('''insert into DailyQuotes values
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', trecord)
        conn.commit()
        dblog.info('建立資料成功(dailyQuotes)：' + str(record))
    except Exception:
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()

def insertSimpleDailyQuotes(record):
    conn = connectDB()
    curs = conn.cursor()
    if checkTableisExist('simpledailyquotes'):
        pass
    else:
        createTable_simpledailyquotes()
    try:
        trecord = tuple(record)
        curs.execute('''insert into simpledailyquotes values
            (?,?,?,?,?,?,?,?)''', trecord)
        conn.commit()
        dblog.info('建立資料成功(simpledailyquotes)：' + str(record))
    except Exception:
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()



def insertStock(record):
    conn = connectDB()
    curs = conn.cursor()
    if checkTableisExist('dailyQuotes'):
        pass
    else:
        createTable_DailyQuotes()
    try:
        trecord = tuple(record)
        curs.execute('''insert into DailyQuotes values
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', trecord)
        conn.commit()
        dblog.info('建立資料成功：' + str(record))
    except Exception as e:
        conn.rollback()
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()

def insertStockIndustryType(record):
    conn = connectDB()
    curs = conn.cursor()
    try:
        curs.execute('''insert into stockIndustryType values
            (?,?,?)''', record)
        conn.commit()
        dblog.info('建立資料成功：' + str(record))
    except Exception:
        conn.rollback()
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()

def inserStockMaster(record):
    conn = connectDB()
    curs = conn.cursor()
    trecord = tuple(record)
    try:
        curs.execute('''insert into stockmaster values
            (?,?,?,?)''', trecord)
        conn.commit()
        dblog.info('建立資料成功：' + str(trecord))
    except Exception:
        conn.rollback()
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()


def insertStockHolderList(record):
    conn = connectDB()
    curs = conn.cursor()

    try:
        trecord = tuple(record)
        curs.execute('''insert into stockdirectorholder values
            (?,?,?,?,?,?,?,?)''', trecord)
        conn.commit()
        dblog.info(trecord)
        dblog.info('insertStockHolderList執行完畢')
    except Exception:
        conn.rollback()
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()


def insertanalysisData(record):
    conn = connectDB()
    curs = conn.cursor()
    if checkTableisExist('analysisdata'):
        pass
    else:
        createTable_analysisdata()
    try:
        for x in record:
            qrecord = (x[0],x[1],x[2],x[3])
            trecord = tuple(x)
            curs.execute('''select * from analysisdata
                            where analysistype = ?
                            and stockid = ?
                            and createdate = ?
                            and pricedate = ?''',qrecord)
            row = curs.fetchall()
            if len(row) == 0:
                curs.execute('''insert into analysisdata values
                    (?,?,?,?,?,?,?,?)''', trecord)
                conn.commit()
                dblog.info('建立資料成功(insertanalysisData)：' + str(record))
            else :
                dblog.info('已有重覆記錄(insertanalysisData)：' + str(record))
    except Exception:
        dblog.error(sys.exc_info())
        dblog.error(traceback.print_exc())
    finally:
        if conn:
            conn.close()




'''-----------insert end-----------'''






