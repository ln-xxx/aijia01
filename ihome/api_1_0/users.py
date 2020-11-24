# coding:utf-8
import re
from flask import g, current_app, jsonify, request, session, make_response
from ihome.utils.captcha1.captcha import captcha
from ihome.utils.sms_conde111 import send_sms, get_code
from . import api
from ihome.utils.response_code import RET
from ihome import db, models, redis_store
from flask import current_app, request
from ihome.models import *

#注册
@api.route('/register', methods=["POST"])
def register():
    name = request.form.get('mobile')
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    print(mobile,password2,password)
    if not all([mobile,password,password2,name]):
        return jsonify(errno= RET.PARAMERR  , errmsg="参数错误")
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次输入的密码不一样")
    user = User.query.filter(User.mobile== mobile).all()
    if user is None:
        return jsonify(errno=RET.PARAMERR, errmsg="改手机号已存在")
    name1= User.query.filter(User.name==name).all()
    if name1:
        return jsonify(errno=RET.PARAMERR, errmsg="用户已存在")
    name2 = User.query.filter(User.mobile ==mobile).all()
    if name2:
        return jsonify(errno=RET.PARAMERR, errmsg="手机号已存在！！！！")

    mobile11 = User(mobile=mobile,password=password,name=name)
    db.session.add(mobile11)
    db.session.commit()
    return jsonify(errno=RET.OK, errmsg="注册成功")

#登录页面
@api.route("/login",methods=["POST"])
def login():
    mobile=request.form.get('mobile')
    password=request.form.get('password')
    # 校验参数
    # 参数完整的校验
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 手机号的格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： "access_nums_请求的ip": "次数"
    user_ip = request.remote_addr  # 用户的ip地址
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    # 从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or not user.check_password(password):
        # 如果验证失败，记录错误次数，返回信息
        try:
            # redis的incr可以对字符串类型的数字数据进行加一操作，如果数据一开始不存在，则会初始化为1
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

    # 如果验证相同成功，保存登录状态， 在session中
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    # print(session.get('user_id'))



    return jsonify(errno=RET.OK, errmsg="登录成功")

# 退出登录
@api.route('/quit',methods=['GET'])
def quit():
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")


#实名认证
@api.route("/auth",methods=["POST"])
def auth():
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    if not all([real_name,id_card]):
        return jsonify(errno=RET.DATAERR, errmsg="数据不完整")
    if not re.match(r"[1-9]\d{13,16}[0-9x]",id_card):
        return jsonify(errno=RET.DATAERR, errmsg="身份证信息错误")
    # a = session.get("user_id")
    # b = User.query.filter(User.id==a).first()
    # b.real_name=real_name
    # b.id_card = id_card
    # db.session.commit()



    return jsonify(errno=RET.OK, errmsg="实名认证完成")

#个人信息

@api.route('/info',methods=['GET'])
def info():
    a = session.get("user_id")
    b = User.query.get(int(a))
    return jsonify(errno=RET.OK, errmsg="OK", data=b.auth_to_dict())


#修改个人信息
#先查看个人信息
@api.route('/upinfo',methods=['GET'])
def upinfo():
    a = session.get("user_id")
    b = User.query.get(int(a))
    return jsonify(errno=RET.OK, errmsg="OK", data=b.to_dict())

#在修改个人信息
@api.route('upinfo1',methods=['POST'])
def upinfo1():
    a = session.get("user_id")
    print(a)
    mobile = request.form.get("mobile")
    name = request.form.get('name')
    if not all([mobile,name]):
        return jsonify(errno=RET.DATAERR, errmsg="检查数据的完整")
    b = User.query.get(a)
    b.mobile=mobile
    b.name=name
    db.session.commit()
    return jsonify(errno=RET.OK, errmsg="修改成功")

#短信验证
@api.route('sms_conde/<mm>',methods=['GET'])
def smsz_conde(mm):
    bb=get_code(6, False)
    print(bb)
    send_sms(mm,bb )
    return jsonify(errno=RET.OK, errmsg="短信发送成功！！！")


#图片验证
@api.route('/img_conde',methods=['GET'])
def img_conde():
    #调用图形验证
    # img,draw,text  = generate_captcha()
    # response = make_response(img)
    # response.headers["Content-Type"] = "image/jpg"
    name, text, image = captcha.generate_captcha()
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    print(text)
    return response

