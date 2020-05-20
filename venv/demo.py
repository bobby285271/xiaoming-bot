
from nonebot import on_command, CommandSession
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import random
import pymysql
account = {
    'user' : 'root',
    'password' : 'zhaobo123..',
    'host' : 'localhost',
    'database' : 'daan'
}

def mysqlConnect(account):
    connect = pymysql.connect(**account)
    return connect

def insertMsg(qq, question, answer):
    connect = mysqlConnect(account)
    cursor = connect.cursor(cursor = pymysql.cursors.DictCursor)
    try:
        sql = "INSERT INTO msg VALUES(\'%s\', \'%s\', \'%s\')"%(question, answer, qq)
        cursor.execute(sql)
        connect.commit()
        print(sql)
    except:
        pass
insertMsg("1234","sad", "222")