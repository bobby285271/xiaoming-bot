from os import path
from cqhttp import CQHttp
import nonebot

import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )
    # bot = nonebot.get_bot()


    # @bot.on_message('private')
    # async def _1(ctx):
    #     if (ctx['user_id'] == 3300408883):
    #         msg = ctx['message']
    #         msg = str(msg)
    #         if ("问题" in msg):
    #             print("*************")


    nonebot.run()
