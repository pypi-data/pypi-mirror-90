import cnabssdk
import cnabssdk.deals
import cnabs_test.tools

def run_test(token):
    cnabssdk.init(token)
    print('获得产品分类')
    cnabs_test.tools.print_tables(cnabssdk.deals.get_categories())
    print("获得2020年发行的 个人消费金融")
    deals = cnabssdk.deals.get_list(catalog= "个人消费金融", year= 2020)
    cnabs_test.tools.print_tables(deals)
    deal_name = deals[0].name
    print("开始提取该产品的相关信息: " + deal_name)
    deal = cnabssdk.deals.get_detail(deal_name)
    cnabs_test.tools.print_object(deal)
    print("获取参与机构: " + deal_name)
    orgs = cnabssdk.deals.get_deal_orgs(deal_name)
    cnabs_test.tools.print_tables(orgs)

    print("获取偿付日期表: " + deal_name)
    payments = cnabssdk.deals.get_payments_dates(deal_name)
    cnabs_test.tools.print_tables(payments)

    print("获取产品证券表: " + deal_name)
    notes = cnabssdk.deals.get_securities(deal_name)
    cnabs_test.tools.print_tables(notes)

    print("获取产品截面信息表: " + deal_name)
    snaps = cnabssdk.deals.get_snapshots(deal_name)
    cnabs_test.tools.print_tables(snaps)
