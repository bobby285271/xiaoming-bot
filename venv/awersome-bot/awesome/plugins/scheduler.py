from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
import json
import requests
from bs4 import BeautifulSoup


def judge(years):
    if years % 4 == 0 and years % 100 != 0:
        return True
    else:
        return False


def change(date, hour, minute):
    min = date.minute
    hr = date.hour
    day = date.day
    month = date.month
    year = date.year
    min += minute
    if min >= 60:
        min -= 60
        hr += 1
    hr += hour
    if hr >= 24:
        hr -= 1
        day += 1
    if day == 30 and month == 2 and judge(year):  # 判断是否为闰年
        month += 1
        day -= 29
    elif day == 29 and month == 2 and judge(year) == False:
        day -= 28
        month += 1
    elif day == 31 and month in (4, 6, 9, 11):
        day -= 30
        month += 1
    elif day == 32:
        day -= 31
        month += 1
    if month > 12:
        month = 1
        year += 1
    if min < 10:
        time = ("%s-%s-%s %s:0%s") % (year, month, day, hr, min)
        return time

    time = ("%s-%s-%s %s:%s") % (year, month, day, hr, min)
    return time


def getNiuKeSchool():
    url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    div = soup.find_all("div", class_='platform-item js-item')

    name = []
    time = []
    url = []

    for it in div:
        div1 = it.find("div", class_='platform-item-cont')
        # print(div1)
        a = div1('a')
        i = div1('i')
        li = div1.find("li", class_='match-time-icon')

        if (len(i) > 0):
            if ("加密" in i[0]['title']):
                continue

        name.append(a[0].string)
        url.append("https://ac.nowcoder.com" + a[0]['href'])
        time.append(li.string[5:21])

    data = {}
    data1 = {}

    for i in range(0, len(name)):
        data[name[i]] = time[i]
        data1[name[i]] = url[i]

    fp = open("niuke_school.json", 'w', encoding='utf-8')
    item_json = json.dumps(data, ensure_ascii=False)
    fp.write(item_json)
    fp.close()
    fp1 = open("niuke_link_school.json", 'w', encoding='utf-8')
    item_json = json.dumps(data1, ensure_ascii=False)
    fp1.write(item_json)
    fp1.close()


def getAtcoder():
    url = 'https://atcoder.jp/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)Gecko/20100101 Firefox/66.0"
    }
    r = requests.get(url, timeout=30, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find("div", id="contest-table-upcoming")

    if div is None:

        print("最近没有比赛")
        data = {"最近没有比赛" : "......"}
        fp = open("atcoder.json", 'w', encoding='utf-8')
        item_json = json.dumps(data, ensure_ascii=False)
        fp.write(item_json)
        fp.close()


    else:
        name = []
        time = []
        link = []
        tbody = div.find("tbody")
        for it in tbody.find_all("tr"):
            a = it.find_all("a")
            print(a[1]['href'])
            link.append("https://atcoder.jp" + a[1]['href'])
            time.append(a[0].string)
            name.append(a[1].string)


        data = {}
        data1 = {}
        for i in range(0, len(name)):
            ti = time[i][:-8]
            date = datetime.strptime(ti, '%Y-%m-%d %H:%M')
           # print(date)
            #print(name[i])
            data[name[i]] = change(date=date, hour=-1, minute=0)  # 日本时差1小时
            #print(change(date=date, hour=-1, minute=0))
            data1[name[i]] = link[i]
       # print(data)
        fp = open("atcoder.json", 'w', encoding='utf-8')
        fp1 = open("atcoder_link.json", 'w', encoding='utf-8')
        item_json = json.dumps(data, ensure_ascii=False)
        fp.write(item_json)
        item_json = json.dumps(data1, ensure_ascii=False)
        fp1.write(item_json)
        fp.close()
        fp1.close()


def getCodeChef():
    url = 'https://www.codechef.com/contests'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)Gecko/20100101 Firefox/66.0"
    }
    r = requests.get(url, timeout=30, headers=headers)
    if (r.status_code != 200):  # 由于codechef网站访问比较慢当出错的时候就在进行访问一次
        r = requests.get(url, timeout=30, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find_all("table", class_="dataTable")
    table = table[1]
    tbody = table.find("tbody")
    name = []
    time = []
    link = []

    data_time = tbody.find_all("td", class_="start_date")
    for it in tbody.find_all('td'):
        # print(it)

        a = it.find("a")

        if a is not None:
            name.append(a.string)
            print(a['href'])
            link.append("https://www.codechef.com" + a['href'])

    for it in data_time:
        time.append(it.text)

    for i in range(0, len(time)):
        date = datetime.strptime(time[i], '%d %b %Y  %H:%M:%S')
        time[i] = change(date, hour=2, minute=30)  # 印度与中国时间相差2时30分
    # 创建字典 比赛名称-->时间

    data = {}
    data1 = {}

    for i in range(0, len(time)):
        data[name[i]] = time[i]
        data1[name[i]] = link[i]

    # 将获取的字典信息 导入json  不建议用数据库 因为信息比较少用json文件方便
    fp = open("codechef.json", 'w', encoding='utf-8')
    fp1 = open("codechef_link.json", 'w', encoding='utf-8')
    item_json = json.dumps(data, ensure_ascii=False)
    fp.write(item_json)
    item_json = json.dumps(data1, ensure_ascii=False)
    fp1.write(item_json)
    fp.close()
    fp1.close()


def getCodefores():
    contest_name = []
    contest_time = []
    urls = 'https://codeforces.com/contests'
    r = requests.get(urls, timeout=30)
    if r.status_code != 200:
        return
    else:

        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find("div", class_="contestList")
        table = div.find("table", class_="")
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                contest_name.append(td.string)
                break

        for tr in table.find_all('tr'):
            # print(tr)
            for td in tr.find_all('td'):
                span = td.find("span", class_='format-time')
                if span:
                    contest_time.append(span.string)

        t = []
        for it in contest_time:
            dete = datetime.strptime(it, '%b/%d/%Y %H:%M')
            #print(dete)
            times = change(date=dete, hour=5, minute=0)
            t.append(times)
        cnt = {}
        for i in range(0, len(contest_time)):
            if 'Div. 1' in contest_name[i][2:-6]:
                continue
            cnt[contest_name[i][2:-6]] = t[i]
        fp = open("cf.json", 'w', encoding='utf-8')
        item_json = json.dumps(cnt, ensure_ascii=False)
        fp.write(item_json)
        fp.close()

def getNiuKe():
    url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13'
    html = requests.get(url)
    if html.status_code != 200:
        return
    else:
        soup = BeautifulSoup(html.text, "html.parser")
        data = {}
        data1 = {}

        div = soup.find("div", class_="nk-main with-banner-page clearfix js-container")
        div_content = div.find("div", class_="nk-content")
        div_contest = div_content.find("div", class_="platform-mod js-current")
        for contest in div_contest.find_all("div", class_="platform-item js-item"):
            next = contest.find("div", class_="platform-item-cont")
            a = next.find("a")
            li = next.find('li', class_='match-time-icon')
            link = a['href']
            name = a.string
            if "小白" in name or "练习赛" in name or "周周" in name or "挑战赛" in name:
                data[name] = li.string
                data1[name] = "https://ac.nowcoder.com" + link
        name = list(data)
        f = 0
        for it in name:
            time = data[it][:21]
            time = time[5:]
            data[it] = time

        fp = open("niuke.json", 'w', encoding='utf-8')
        item_json = json.dumps(data, ensure_ascii=False)
        fp.write(item_json)
        fp.close()
        fp1 = open("niuke_link.json", 'w', encoding='utf-8')
        item_json = json.dumps(data1, ensure_ascii=False)
        fp1.write(item_json)
        fp1.close()


### 获取每场比赛最近的时间

def getFirstNiuke():
    file = open('niuke.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    niuke = {}
    niuke[name[0]] = data[name[0]]
    return niuke

def getFirstNiukeSchoolLink():
    file = open('niuke_link_school.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    return data[name[0]]

def getFirstNiukeSchool():
    file = open('niuke_school.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    niuke = {}
    niuke[name[0]] = data[name[0]]
    return niuke

def getFirstCf():
    file = open('cf.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    cf = {}
    cf[name[0]] = data[name[0]]
    return cf


def getFirstCodeChef():
    file = open('codechef.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    codechef = {}
    codechef[name[0]] = data[name[0]]
    return codechef


def getFirstAtcoder():
    file = open('atcoder.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    atcoder = {}
    atcoder[name[0]] = data[name[0]]
    return atcoder


# 判断该时间 与先找的时间进行比较 相差小时进行通知

def getAns(date1, date2):
    days = (date1 - date2).days
    print("天")
    print(days)
    # month = (date1 - date2).month  # 年就不要考虑 概率比较小
    if days == 0 and date1.month == date2.month:
        hours = (date1.hour - date2.hour)
        min = (date1.minute - date2.minute)
        print("小时")
        print(hours)
        print("分钟")
        print(min)
        if hours == 1 and min == 0:
            return hours
    return -10000


# 导入要通知的群与 好友
def loadGroup() -> list:
    file = open('group.json', 'r', encoding='utf-8')
    js = file.read()
    group = json.loads(js)
    group_id = group['group']
    print("通知的群号")
    print(group_id)
    return group_id


def loadId() -> list:
    file = open('id.json', 'r', encoding='utf-8')
    js = file.read()
    id = json.loads(js)
    ID = id['user']
    print("通知的账号：")
    print(ID)
    return ID


def getFirstNiukeLink():
    file = open('niuke_link.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    return data[name[0]]


def getFirstCodeChefLink():
    file = open('codechef_link.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    return data[name[0]]

def getFirstAtcoderLink():
    file = open('atcoder_link.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    return data[name[0]]




# 'interval', minutes=10

@nonebot.scheduler.scheduled_job('interval', minutes=120)  # 2小时进行1次爬虫
async def loadMsg():
    getNiuKe()
    getCodefores()
    getCodeChef()
    getAtcoder()
    getNiuKeSchool()
    print("导入信息")


@nonebot.scheduler.scheduled_job('interval', minutes=1)
async def _():
    bot = nonebot.get_bot()
    now = datetime.now()
    cf = getFirstCf()
    niuke = getFirstNiuke()
    codechef = getFirstCodeChef()
    atcoder = getFirstAtcoder()
    niukeSchool = getFirstNiukeSchool()

    #  cf
    name = list(cf)
    time = cf[name[0]]
    print("*"*10 + "cf")
    print(time)
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    print(dates)
    ans = getAns(dates, now)
    # loadGroup()
    if ans == 1:
        link = 'https://codeforces.com/contests'
        if dates.minute < 10:
            text = "比赛通知！\r\n\r\n"+"比赛平台：codeforces  \r\n\r\n" +"比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : 0%s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) +"比赛链接："+link
        else:
            text = "比赛通知！\r\n\r\n"+"比赛平台：codeforces  \r\n\r\n" +"比赛名称：" + name[0] + "\r\n\r\n比赛时间：今天 %s : %s 举行\r\n\r\n" % (
            str(dates.hour), str(dates.minute))+"比赛链接："+link
        group = loadGroup()
        for it in group:
            if it == 818692628:
                try:
                    await bot.send_group_msg(group_id=it, message="[CQ:at,qq=1173007724] [CQ:at,qq=1206770096] [CQ:at,qq=1768278842] [CQ:at,qq=743742996]  [CQ:at,qq=1623821585][CQ:at,qq=1921639480]\r\n\r\n " + text)
                except CQHttpError:
                    await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
                continue
            try:
                await bot.send_group_msg(group_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        ID = loadId()
        for it in ID:
            try:
                await bot.send_private_msg(user_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        #await bot.send_private_msg(user_id=1173007724, message=text) #测试

    # 牛客

    name = list(niuke)
    time = niuke[name[0]]
    print("*"*10 + "牛客")
    print(time)
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    ans = getAns(dates, now)

    if ans == 1:
        text = ""
        link = getFirstNiukeLink()
        if dates.minute < 10:
            text ="比赛通知！\r\n\r\n"+ "比赛平台: 牛客  \r\n\r\n" + "比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : 0%s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) + "比赛链接：" + link
        else:
            text = "比赛通知！\r\n\r\n"+"比赛平台：牛客  \r\n\r\n" + "比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : %s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) + "比赛链接：" + link
        group = loadGroup()
        for it in group:
            if it == 818692628:
                try:
                    await bot.send_group_msg(group_id=it, message="[CQ:at,qq=1173007724] [CQ:at,qq=1206770096] [CQ:at,qq=1768278842] [CQ:at,qq=743742996]  [CQ:at,qq=1623821585][CQ:at,qq=1921639480]\r\n " + text)
                except CQHttpError:
                    await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
                continue
            try:
                await bot.send_group_msg(group_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        ID = loadId()
        for it in ID:
            try:
                await bot.send_private_msg(user_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        #await bot.send_private_msg(user_id=1173007724, message=text)  # 测试

    #牛客高校
    name = list(niukeSchool)
    time = niukeSchool[name[0]]
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    print("牛客高校：")
    print(time)
    ans = getAns(dates, now)
    if(ans == 1):
        text = ""
        link = getFirstNiukeSchoolLink()
        if dates.minute < 10:
            text = "比赛通知！\r\n\r\n" + "比赛平台: 牛客  \r\n\r\n" + "比赛名称：" + name[
                0] + "\r\n\r\n比赛时间： 今天 %s : 0%s 举行\r\n\r\n" % (
                       str(dates.hour), str(dates.minute)) + "比赛链接：" + link
        else:
            text = "比赛通知！\r\n\r\n" + "比赛平台：牛客  \r\n\r\n" + "比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : %s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) + "比赛链接：" + link
        group = loadGroup()
        for it in group:
            if it == 818692628:
                try:
                    await bot.send_group_msg(group_id=it,
                                             message="[CQ:at,qq=1173007724] [CQ:at,qq=1206770096] [CQ:at,qq=1768278842] [CQ:at,qq=743742996]  [CQ:at,qq=1623821585][CQ:at,qq=1921639480]\r\n " + text)
                except CQHttpError:
                    await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
                continue
            try:
                await bot.send_group_msg(group_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        ID = loadId()
        for it in ID:
            try:
                await bot.send_private_msg(user_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        #await bot.send_private_msg(user_id=1173007724, message=text)  # 测试


    # codechef


    name = list(codechef)
    time = codechef[name[0]]
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    print("*" * 10 + "codechef")
    print(dates)
    ans = getAns(dates, now)
    if ans == 1:
        text = ""
        link = getFirstCodeChefLink()
        if dates.minute < 10:
            text ="比赛通知！\r\n\r\n"+ "比赛平台: codechef  \r\n\r\n" + "比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : 0%s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) + "比赛链接：" + link
        else:
            text ="比赛通知！\r\n\r\n"+ "比赛平台: codechef  \r\n\r\n" + "比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : %s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) + "比赛链接：" + link

        group = loadGroup()
        for it in group:
            if it == 818692628:
                try:
                    await bot.send_group_msg(group_id=it,
                                             message="[CQ:at,qq=1173007724] [CQ:at,qq=1206770096] [CQ:at,qq=1768278842] [CQ:at,qq=743742996]  [CQ:at,qq=1623821585][CQ:at,qq=1921639480]\r\n " + text)
                except CQHttpError:
                    await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
                continue
            try:
                await bot.send_group_msg(group_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        ID = loadId()
        for it in ID:
            try:
                await bot.send_private_msg(user_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        #await bot.send_private_msg(user_id=1173007724, message=text)  # 测试




    # atcoder

    name = list(atcoder)
    time = atcoder[name[0]]
    if(name[0] == "最近没有比赛"):
        return
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    print("**"*5 + "atcoder")
    print(dates)
    ans = getAns(dates, now)
    if ans == 1:
        text = ""
        link = getFirstAtcoderLink()
        if dates.minute < 10:
            text ="比赛通知！\r\n\r\n"+ "比赛平台: atcoder  \r\n\r\n" + "比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : 0%s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) + "比赛链接：" + link
        else:
            text ="比赛通知！\r\n\r\n"+ "比赛平台: atcoder  \r\n\r\n" + "比赛名称：" + name[0] + "\r\n\r\n比赛时间： 今天 %s : %s 举行\r\n\r\n" % (
                str(dates.hour), str(dates.minute)) + "比赛链接：" + link

        group = loadGroup()
        for it in group:
            if it == 818692628:
                try:
                    await bot.send_group_msg(group_id=it, message="[CQ:at,qq=1173007724] [CQ:at,qq=1206770096] [CQ:at,qq=1768278842] [CQ:at,qq=743742996]  [CQ:at,qq=1623821585][CQ:at,qq=1921639480]\r\n " + text)
                except CQHttpError:
                    await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
                continue
            try:
                await bot.send_group_msg(group_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        ID = loadId()
        for it in ID:
            try:
                await bot.send_private_msg(user_id=it, message=text)
            except CQHttpError:
                await bot.send_private_msg(user_id=1173007724, message="debug: " + str(it))
        #await bot.send_private_msg(user_id=1173007724, message=text)  # 测试

#{"user": [877509477, 1779755626, 2318558791, 1660895700, 1377294687, 839070790, 1527148777, 1729529198, 1115089836, 2622447282, 1280256162, 1085503007, 1909000478, 503040162, 505494142, 202367038, 1623821585, 664105959, 3197301325, 403567557, 491105703, 851644905, 768276454, 2474691665, 1173007724, 771773505, 2107917115, 1085980958, 1544356662,  1203162819, 1071059972, 1095322940, 965729491, 996423542, 953978752, 814295903]}
#{"group": [818692628, 593466006, 854591549, 818049647, 906994965, 956251287, 689873462, 923675729, 829710328, 610732077, 1082871924, 881795822]}