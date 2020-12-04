from celery_app1.task1 import add  # 在这里我只调用了task1

if __name__ == '__main__':
    print("Start Task ...")
    re = add.delay(7, 5)
    print(re.id)
    # print(re.status)
    print("End Task ...")
