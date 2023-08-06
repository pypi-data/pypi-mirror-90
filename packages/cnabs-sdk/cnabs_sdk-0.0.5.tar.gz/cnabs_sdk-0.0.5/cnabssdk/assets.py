import cnabssdk.clients


def get_distribution_names(dealNameOrId):
    '''
    资产分布的名称
    参考文档: https://www.cn-abs.com/openapi.html#/detail/documents?id=8

    Args:
        dealNameOrId: 产品全称或者ID
    
    Returns: Array
        code: 代码
        name: 名称
        short_name:  简称
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/distributions"
    return cnabssdk.clients.cnabsclient().get(url, {})


def get_distributions(dealNameOrId, distribute_name = "", date = ""):
    '''
    资产分布的明细数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=9
    
    Args:
        dealNameOrId: 产品全称或者Id 
        date: 产品偿付日期
        name: 分布类别
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/distributions/"+ distribute_name +"/"+ date
    params = {}
    return cnabssdk.clients.cnabsclient().get(url, params)


def get_deliquencies(dealNameOrId, date = ""):
    '''
    获得产品的逾期数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=10
    
    Args:
        dealNameOrId: 产品全称或者Id 
        date: 日期
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/distributions/overdue/"+ date
    params = {}
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_defaulted_process(dealNameOrId, date = ""):
    '''
    获得产品的违约处置数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=11
    
    Args:
        dealNameOrId: 产品全称或者Id 
        date: 日期
    Returns:
        
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/distributions/default_process/"+ date
    params = {}
    return cnabssdk.clients.cnabsclient().get(url, params)


def get_promised_cashflows (dealNameOrId, date = ""):
    '''
    获得该期报告的预测归集现金流
    https://www.cn-abs.com/openapi.html#/detail/documents?id=12
    
    Args:
        dealNameOrId: 产品全称或者Id 
        date: 日期
    Returns:
        
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/cashflows/forecast/report/"+ date
    params = {}
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_repayment(dealNameOrId, date = ""):
    '''
    获得该期偿付报告的资产归集现金流
    https://www.cn-abs.com/openapi.html#/detail/documents?id=13
    
    Args:
        dealNameOrId: 产品全称或者Id 
        date: 日期
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/cashflows/"+ date
    params = {"date": date}
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_dates(dealNameOrId):
    '''
    获得该产品的资产偿付时间序列
    https://www.cn-abs.com/openapi.html#/detail/documents?id=14
    
    Args:
        dealNameOrId: 产品全称或者Id
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/dates"
    dates = cnabssdk.clients.cnabsclient().get(url, {})
    result = []
    for item in dates:
        result.append(item.date)
    return result


def get_statistics(dealNameOrId, date, itemName = ""):
    '''
    获得该产品的该期的资产特征数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=15
    
    Args:
        dealNameOrId: 产品全称或者Id 
        itemName: 指标名称(为空返回全部指标)
        date: 日期（yyyy-MM-dd）
    '''
    url = "assets/openapi/assets/"+ dealNameOrId +"/statistics"
    params = {"itemName": itemName, "date": date}
    return cnabssdk.clients.cnabsclient().get(url, params)


