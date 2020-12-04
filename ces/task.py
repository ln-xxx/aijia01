import time

from celery import Celery

"""
本地有redis，那就localhost,云服务器就写IP地址,redis有密码格
式:"redis://:332572@127.0.0.1:6379/2"
"""
broker = 'redis://127.0.0.1:6379/1'
backend = 'redis://127.0.0.1:6379/2'
# 参数1 自动生成任务名的前缀
# 参数2 broker 是我们的redis的消息中间件(消息队列)
# 参数3 backend 用来存储我们的任务结果的(结果存储)
app = Celery('t1', broker=broker, backend=backend)


# 加入装饰器变成异步函数 @对象名.task
@app.task
def add(x, y):
    print('进入任务函数...')
    time.sleep(4)  # 模拟耗时
    return x + y


@app.task
def add2(x, y):
    print('进入任务函数...')
    time.sleep(4)  # 模拟耗时
    return x + y
