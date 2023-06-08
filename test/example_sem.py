import asyncio
import random
from asyncio import CancelledError


async def send(n,sem):
    async with sem:
        print(f"send {n} start")
        await asyncio.sleep(1)
        print(f"send {n} end")

        # return f"睡眠成功"


async def main():
    sem = asyncio.Semaphore(50)
    tasks=[]
    for i in range(100):
        task = asyncio.create_task(send(i,sem),name=f"send-{i}")
        tasks.append(task)


    try:

        done,pending = await asyncio.wait(tasks)


    except CancelledError:
        # print("取消任务")
        for task in tasks:
            task.cancel()
            print(task.get_name() + "取消成功")
    finally:
        print(tasks)
        for task in tasks:
            if task.done():
                print(task.get_name() + "任务完成")
            else:
                print(task.get_name() + "未完成")




        # # print(done)
    for item in done:
        print(item.get_name() + "任务完成")
        #
        # for item in pending:
        #     print(item.get_name() + "未完成")

if __name__ == '__main__':
    asyncio.run(main())

