# coding: utf-8
# 2023/9/23  更新
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import asyncio
from .base.utils import Logger
from .Flow import XFlow, InstagramFlow


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 非同期処理にて並列処理を実行していく

class AsyncProcess:
    def __init__(self, debugMode=True) -> None:
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.xFlow = XFlow(debugMode=debugMode)
        self.instagramFlow = InstagramFlow(debugMode=debugMode)


# ----------------------------------------------------------------------------------
# それぞれのaccount_idにて実行をしていく

    async def flowTaskProcess(self):
        tasks = []

        xFlow = self.xFlow.xProcess()
        instagramFlow = self.instagramFlow.instagramProcess()
        tasks.extend([xFlow, instagramFlow])

        # すべてのタスクを非同期にて並列処理を実行する
        self.logger.info(f"task一覧\n{tasks}")
        await asyncio.sleep(3)

        self.logger.info("これより並列処理を実行")
        await asyncio.gather(*tasks)


# ----------------------------------------------------------------------------------
# **********************************************************************************