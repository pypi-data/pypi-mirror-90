from functools import partial
import asyncio
from function_scheduling_distributed_framework.concurrent_pool.custom_threadpool_executor import ThreadPoolExecutorShrinkAble

async_executor_default = ThreadPoolExecutorShrinkAble(20)


async def simple_run_in_executor(f, *args, async_executor=None, async_loop=None, **kwargs):
    """
    使任意同步同步函数f，转化成asyncio异步api语法，
    例如 r = await  simple_run_in_executor(block_fun, 20)，可以不阻塞事件循环。

    :param f:  f是一个同步的阻塞函数，f前面不能是由async定义的。
    :param args:
    :async_executor: 线程池
    :param async_loop: async的loop对象
    :param kwargs:
    :return:
    """
    loopx = async_loop or asyncio.get_event_loop()
    async_executorx = async_executor or async_executor_default
    # print(id(loopx))
    result = await loopx.run_in_executor(async_executorx, partial(f, *args, **kwargs))
    return result


if __name__ == '__main__':
    import time
    import requests


    def block_fun(x):
        time.sleep(5)
        print(x)
        return x * 10


    async def enter_fun(xx):  # 入口函数，盈利为一旦异步，必须处处异步。不能直接调用block_fun，否则阻塞其他任务。
        await asyncio.sleep(1)
        # r = block_fun(xx)  # 如果这么用就完蛋了，阻塞事件循环， 运行完所有任务需要更久。
        r = await  simple_run_in_executor(block_fun, xx)
        print(r)


    loopy = asyncio.get_event_loop()
    print(id(loopy))
    tasks = []
    tasks.append(simple_run_in_executor(requests.get, url='http://www.baidu.com', timeout=10))  # 同步变异步用法。

    tasks.append(simple_run_in_executor(block_fun, 1))
    tasks.append(simple_run_in_executor(block_fun, 2))
    tasks.append(simple_run_in_executor(block_fun, 3))

    tasks.append(enter_fun(4))
    tasks.append(enter_fun(5))
    tasks.append(enter_fun(6))

    print('开始')
    loopy.run_until_complete(asyncio.wait(tasks))
    print('结束')
