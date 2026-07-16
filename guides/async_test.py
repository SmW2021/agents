import asyncio

async def ok_task(name):
    await asyncio.sleep(1)
    return f"{name} 成功"

async def bad_task():
    await asyncio.sleep(0.5)
    raise ValueError("邮局关门了!")

# 模式一:默认,异常直接抛出
async def strict_mode():
    try:
        await asyncio.gather(ok_task("面包"), bad_task(), ok_task("苹果"))
    except ValueError as e:
        print(f"任务失败: {e}")

# 模式二:return_exceptions=True,异常变成结果的一部分
async def tolerant_mode():
    results = await asyncio.gather(
        ok_task("面包"), bad_task(), ok_task("苹果"),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"出错了: {r}")
        else:
            print(f"拿到: {r}")

asyncio.run(strict_mode())
asyncio.run(tolerant_mode())