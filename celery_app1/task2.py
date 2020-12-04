from celery_app1 import app


@app.task
def multiply(x, y):


    print('Enter call function ...')
    return x * y
