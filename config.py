# coding:utf-8

import redis


class Config(object):
    """配置信息"""
    SECRET_KEY = "XHSOI*Y9dfs9cshd9"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/ihome_python04"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位秒

    # 邮箱验证信息
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '1158951251@qq.com'
    MAIL_PASSWORD = 'eluxwwizhpvagefi'


# 邮箱验证
# bzoaoyqhgybtjegd

# kkanjvzixtwhhbcf

class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
