import asyncio

async def steam_baozi(n):            # async def + yield = 异步生成器
    for i in range(1, n + 1):
        print("蒸包子", i)
        await asyncio.sleep(1)       # 【await 停】蒸1秒,期间让别的任务跑
        yield f"包子{i}"              # 【yield 停】递出去,等消费者要下一个

async def waiter():                  # 一个"别的任务",证明蒸包子时没人被卡住
    for _ in range(6):
        await asyncio.sleep(0.5)
        print("        (服务员在倒水...)")

async def main():
    async def eat():
        async for baozi in steam_baozi(3):   # 每圈: await __anext__()
            print("吃掉", baozi)

    await asyncio.gather(eat(), waiter())    # 老朋友 gather!

asyncio.run(main())