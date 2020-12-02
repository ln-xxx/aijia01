# coding:utf-8
import re

from flask import current_app, request
from flask import jsonify, session, make_response

from ihome import redis_store
from ihome.models import *
from ihome.utils.captcha1.captcha import captcha
from ihome.utils.img_qiniu import storage
from ihome.utils.response_code import RET
from ihome.utils.sms_conde111 import send_sms, get_code
from . import api






@api.route("/users/avatar",methods=["POST"])

def set_user_avatar():
    """
    设置用户头像
    参数：图片(多媒体表单格式的),user_id(g.user_id)
    :return:
    """
    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    # user_id = g.user_id
    user_id = 6

    # 获取图片
    image_file = request.files.get("avatar")

    if image_file is  None:
        return jsonify(errno=RET.PARAMERR,errmsg="未上传图片")

    image_data = image_file.read()
    # print(image_data)
    # 调用七牛上传图片
    try:
        file_name = storage(image_data)
        print(file_name)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg="上传图片失败")

    # 保存文件名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar_url":file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存图片信息失败")

    avatar_url = constants.QINIU_URL_DOMAIN + file_name
    # 保存成功返回
    return jsonify(errno=RET.OK,errmsg="保存成功",data={"avatar_url":avatar_url})
