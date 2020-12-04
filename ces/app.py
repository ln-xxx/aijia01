from task import add
from ces.task import add2

if __name__ == '__main__':
    print('Start task...')
    resutl = add.delay(2, 3)
    print(resutl.id)  # 获取任务id
    print(resutl.get())  # 获取任务执行结果
    print('End task...')
