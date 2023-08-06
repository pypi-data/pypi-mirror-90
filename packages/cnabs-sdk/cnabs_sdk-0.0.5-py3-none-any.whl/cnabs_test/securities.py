import sys
import types
import cnabssdk
import cnabssdk.securities
import cnabs_test.tools

def run_test(token):
    cnabssdk.init(token)
    
    security_list = cnabssdk.securities.get_list(keywords="建元", year= 2020)
    print("获得2020发行的建元系列证券列表: " + str(len(security_list)))
    cnabs_test.tools.print_tables(security_list)
    
    security_name = '建元2020年第一期个人住房抵押贷款资产支持证券优先A-1档资产支持证券'
    security_code = "2089063.IB"
    print("以下使用证券: ", security_name, '进行测试')

    sec = cnabssdk.securities.get_detail(security_code)
    cnabs_test.tools.print_object(sec)
    current = sec.current
    print('证券最新动态')
    cnabs_test.tools.print_object(current)

    coupon = cnabssdk.securities.get_coupon(security_code)
    print('证券利率')
    cnabs_test.tools.print_object(coupon)
    print('评级历史')
    ratings = cnabssdk.securities.get_ratings(security_code)
    cnabs_test.tools.print_tables(ratings)

    print('偿付列表')
    payments = cnabssdk.securities.get_payments(security_code)
    cnabs_test.tools.print_tables(payments)

    print('获得增信')
    credit_list = cnabssdk.securities.get_credits(security_code)
    cnabs_test.tools.print_tables(credit_list)

    print('获得截面历史')
    snaps = cnabssdk.securities.get_snapshots(security_code)
    cnabs_test.tools.print_tables(snaps)
    