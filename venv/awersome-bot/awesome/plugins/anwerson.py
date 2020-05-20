# from nonebot import on_command, CommandSession
# from bs4 import BeautifulSoup
# import requests
# from datetime import datetime
# import json
# import random
# import pymysql
# import nonebot
#
# def mysqlConnect(account):
#     connect = pymysql.connect(**account)
#     return connect
#
# account = {
#         'user': 'root',
#         'password': 'zhaobo123..',
#         'host': 'localhost',
#         'database': 'daan'
#     }
# connect = mysqlConnect(account)
# cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
#
#
#
#
#
# def insertMsg(qq, question, answer):
#     try:
#         sql = "INSERT INTO msg VALUES(\'%s\', \'%s\', \'%s\');" % (question, answer, qq)
#         print(sql)
#         cursor.execute(sql)
#         connect.commit()
#         print("****")
#     except:
#        print("写入错误")
#
#
# def insertwrongMsg(qq, question):
#     try:
#         sql = "INSERT INTO wmsg VALUES(\'%s\', \'%s\');" % (question, qq)
#         cursor.execute(sql)
#         connect.commit()
#     except:
#         print("写入错误")
#
#
# def getMsg(qq, question):
#     url = "http://wk.xlqwlcm.cn/wkcx//web.php?question=%s" % (question)
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)Gecko/20100101 Firefox/66.0"
#     }
#     r = requests.get(url, timeout=30, headers=headers)
#     html = r.text
#     data = json.loads(html)
#     answer = data['answer']
#     if 'QQ' in answer:
#         print("找不到")
#         insertwrongMsg(qq, question)
#         return "@"
#     else:
#         insertMsg(qq, question, answer)
#         return answer
#
#
# queue_id = []
# queue_group = []
# que = []
#
# @on_command('question', aliases=('qs', 'answer'))
# async def getAnswer(session: CommandSession):
#     msg = session.ctx['message']
#     msg = str(msg)
#     msg = msg.split()
#     message_type = session.ctx['message_type']
#     qq = session.ctx['user_id']
#
#     question = "".join(msg[1:])
#     print(question)
#     #ans = getMsg(str(qq), question)
#
#     # if ans == '@':
#     #     if (message_type == 'group'):
#     #         await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=ai + "\r\n找不到该题[CQ:face,id=106]")
#     #     elif (message_type == 'private'):
#     #         await session.bot.send_private_msg(user_id=session.ctx['user_id'], message="找不到该题[CQ:face,id=106]")
#     # else:
#     #     if (message_type == 'group'):
#     #         await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=ai + "\r\n"+ans)
#     #     elif (message_type == 'private'):
#     #         await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=ans)
#
#     if message_type == 'group':
#         queue_group.append([session.ctx['group_id'], qq])
#     else:
#         queue_id.append(qq)
#     que.append(question)
#     await session.bot.send_private_msg(user_id=3300408883, message="查 " +question)
#
# bot = nonebot.get_bot()
# @bot.on_message('private')
# async def _1(ctx):
#     if (ctx['user_id'] == 3300408883):
#         print("****************")
#         msg = ctx['message']
#         msg = str(msg)
#         if "未查到该题" in msg:
#             msg = msg.replace("网课小助手查题", "小明")
#             print(msg)
#             if (len(queue_group) > 0):
#                 it = queue_group.pop(0)
#                 ai = "[CQ:at,qq=%s]" % it[1]
#                 insertwrongMsg(it[1], que.pop(0))
#                 await bot.send_group_msg(group_id=it[0], message=ai + "\r\n" + "\r\n找不到该题[CQ:face,id=106]")
#             if (len(queue_id) > 0):
#                 it = queue_id.pop(0)
#                 insertwrongMsg(it, que.pop(0))
#                 await bot.send_private_msg(user_id=it, message="\r\n找不到该题[CQ:face,id=106]")
#         elif ("答案" in msg):
#             print("&&&&")
#             msg = msg.replace("网课小助手查题机器人", "小明机器人(支持学习通 智慧树等平台正确率80%左右)\r\n")
#             msg = msg[:-1]
#             msg = msg.replace("答案", "\r\n答案")
#             print(msg)
#             if (len(queue_group) > 0):
#                 it = queue_group.pop(0)
#                 ai = "[CQ:at,qq=%s]" % it[1]
#                 insertMsg(it[1], que.pop(0), msg)
#                 await bot.send_group_msg(group_id=it[0], message=ai + "\r\n"+msg)
#             if (len(queue_id) > 0):
#                 it = queue_id.pop(0)
#                 insertMsg(it, que.pop(0), msg)
#                 await bot.send_private_msg(user_id=it, message=msg)
#         else:
#             print("SSS")
#
# @nonebot.scheduler.scheduled_job('interval', minutes=1.1)
# async def setMsg():
#     if(len(que) > 0):
#         await bot.send_private_msg(user_id=3300408883, message="查 " + que[0])
#
#
#
#
#
#
#
#
#
#
#
