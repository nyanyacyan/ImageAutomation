#  coding: utf-8
# ----------------------------------------------------------------------------------
# 2024/6/17 更新

# ----------------------------------------------------------------------------------


import time
import asyncio
from installer.src.method.const import AccountId

from method.base.utils import Logger
from method.AsyncProcess import AsyncProcess



# ------------------------------------------------------------------------------


class Main:
   def __init__(self, debugMode=True):

      # logger
      self.getLogger = Logger(__name__, debugMode=debugMode)
      self.logger = self.getLogger.getLogger()


   async def main(self):
      start_time = time.time()
      # (重い処理)
      account_ids = [
         # AccountId.account_id_a.value,
         # AccountId.account_id_b.value,
         # AccountId.account_id_c.value,
         AccountId.account_id_d.value,
         # AccountId.account_id_e.value,
         # AccountId.account_id_f.value,
         # AccountId.account_id_g.value,
         # AccountId.account_id_h.value,
         # AccountId.account_id_i.value,
         # AccountId.account_id_j.value
      ]

      asyncProcess = AsyncProcess(account_ids=account_ids)

      await asyncProcess.flow_task_process()

      end_time = time.time()

      diff_time = end_time - start_time

      self.logger.info(f"処理時間 : {diff_time}秒")


# ------------------------------------------------------------------------------



if __name__ == '__main__':
   main_process = Main()
   asyncio.run(main_process.main())
