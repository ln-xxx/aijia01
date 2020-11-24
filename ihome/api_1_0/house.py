# coding:utf-8
#房屋信息
from kombu.utils import json

from ihome.utils.response_code import RET
from . import api
from ihome import db, models
from flask import current_app, request, jsonify, session
from ihome.models import *

#客户订单
@api.route('/goods1')
def goods1():
    
    pass


#预定
@api.route("/reserve")
def reserve():
    #获取前端的时间 和结束时间
    #获取前端的价钱
    #计算价钱
    #保存redis 数据库
    #返回预定成功页面
    pass
   # aaa = request.form.get('aaa')
   # bbb = request.form.get('bbb')
#搜索页面

@api.route("/find7")
def find7():
    #获取前端的数据  城区 和时间
    #判断前端数据是否有效
    # 数据库多条件查询
    #返回展示页面
    pass


#房屋详情页面
@api.route('details1')
def details1():
    # 前端给的 房屋id
    # 按照id   去数据库查找
    #返回数据
    pass


#发布房源
@api.route('/issue',methods=['POST'])
def issue():
    user_id =session.get("user_id")
    # user_id = request.form.get('user_id')
    title = request.form.get('title')  #房屋标题
    price= request.form.get('price')   #每晚价格
    area_id = request.form.get('area_id')  #所在城区
    address = request.form.get('address')  #详细地址
    room_count = request.form.get('room_count') #出租房屋数量
    acreage = request.form.get('acreage')  #房屋面积
    unit = request.form.get('unit')  #如：三室两厅两卫
    beds = request.form.get('beds')  #卧床配置
    deposit = request.form.get('deposit')#押金
    min_days = request.form.get('min_days')  #入住最少天数
    max_days = request.form.get('max_days')  #入住最多天数
    facility = request.form.get('facility')
    if not all([title,price,area_id,address,room_count,acreage,unit,beds
                ,deposit,min_days,max_days]):
        return jsonify(errno=RET.OK, errmsg="检查数据的完整")
    a = House(title=title, price=price, area_id=area_id, address=address, room_count=room_count, acreage=acreage,
              unit=unit, beds=beds
              , deposit=deposit, min_days=min_days, max_days=max_days, user_id=user_id, )
    try:
        # select  * from ih_facility_info where id in []
        facilities = Facility.query.filter(Facility.id.in_(facility)).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if facilities:
        # 表示有合法的设施数据
        # 保存设施数据
        a.facilities = facilities


    db.session.add(a)
    db.session.commit()

    return jsonify(errno=RET.OK, errmsg="发布成功")


# 显示全部的房源信息
@api.route('/look_over',methods=['GET'])
def look_over():
    area_dict_li = []
    a = House.query.all()
    for area in a:
        area_dict_li.append(area.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data=area_dict_li)
