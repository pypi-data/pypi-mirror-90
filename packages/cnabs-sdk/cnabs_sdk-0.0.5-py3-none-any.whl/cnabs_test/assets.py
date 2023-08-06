import sys
import types
import cnabssdk
import cnabssdk.assets
import cnabs_test.tools

def run_test(token):
    cnabssdk.init(token)
    dealName = '建元2019年第十二期个人住房抵押贷款资产支持证券'

    print('get assets info by deal name: ' + dealName)

    diss = cnabssdk.assets.get_distribution_names(dealName)
    cnabs_test.tools.print_tables(diss)

    print('get dates: ')
    dates = cnabssdk.assets.get_dates(dealName)
    cnabs_test.tools.print_array('Date', dates)

    print('cutoff date: ' + dates[0])

    print('get distribution data by: ' + diss[0].name + ' date: ' + dates[0])
    orignalDis = cnabssdk.assets.get_distributions(dealName, diss[0].name, dates[0])
    cnabs_test.tools.print_tables(orignalDis)

    print('获得资产特征: ' + dates[0])
    factors = cnabssdk.assets.get_statistics(dealName, dates[0])
    cnabs_test.tools.print_tables(factors)

    cashs = cnabssdk.assets.get_promised_cashflows(dealName, dates[1])
    cnabs_test.tools.print_tables(cashs)
