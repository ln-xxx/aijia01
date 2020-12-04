from celery_app1 import app


# 加入装饰器变成异步的函数
@app.task
def add(x, y):


    print('Enter call function ...')
    return x + y
