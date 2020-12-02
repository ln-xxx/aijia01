from alipay import AliPay
import os


def order_pay():
    a =  os.path.join(os.path.dirname(__file__), "/keys/app_private_key.txt")
    b = os.path.join(os.path.dirname(__file__), "/keys/alipay_public_key.txt")
    # print(a)

    # 创建支付宝sdk的工具对象
    alipay_client = AliPay(
        appid="2016102300744378",
        app_notify_url=None,  # 默认回调url
        app_private_key_path= a, # 私钥
        alipay_public_key_path=b,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,

        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    # order_string = alipay_client.api_alipay_trade_wap_pay(
    #     out_trade_no=1,  # 订单编号
    #     total_amount=str(10000),   # 总金额
    #     subject=u"爱家租房 %s" % 123,  # 订单标题
    #     return_url="http://127.0.0.1:5000/payComplete.html",  # 返回的连接地址
    #     notify_url=None  # 可选, 不填则使用默认notify url
    # )

    # 构建让用户跳转的支付连接地址
    # pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
order_pay()