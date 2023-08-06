import cnabssdk.clients
import time

def get_list(keywords="", begin="", end="", dealStatus="", year="", catalog="", orgName=""):
    '''
    证券列表 最大返回5000行数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=56
    Args:
        keywords: 关键字
        orgName: 机构名称
        catalog: 产品分类
        year: 年份
        dealStatus: 产品状态 支持中英文参数，选项如下（中文／英文）：过会中/Auditing 、发行中/Issueing 、存续期/Issued 、已清算/End 、停售/Stop 
        begin: 开始日期
        end: 结束日期
    '''
    url = "products/openapi/securities"
    params = {
        "keywords": keywords,
        "begin": begin,
        "end": end,
        "status": dealStatus,
        "year": year,
        "catalog": catalog,
        "orgName": orgName
    }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_detail(codeOrId):
    '''
    证券详情
    https://www.cn-abs.com/openapi.html#/detail/documents?id=57

    Args:
        codeOrId: 代码或者证券Id: 111111.SH
    Returns:
    '''
    url = "products/openapi/securities/" + codeOrId
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_rating_snapshot(codeOrId, date = "", ratingAgency = ""):
    '''
    证券评级截面数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=58
    
    Args:
        codeOrId: 代码或者证券Id
        date: 日期
        ratingAgency: 评级机构
    '''
    url = "products/openapi/securities/"+ codeOrId +"/ratings/snapshot"
    params = {
        "date": date
    }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_ratings(codeOrId, begin = None, end = None, ratingAgency = None):
    '''
    证券评级历史
    https://www.cn-abs.com/openapi.html#/detail/documents?id=59
    
    Args:
        codeOrId: 代码或者证券Id
        begin: 开始时间
        end: 结束时间
        ratingAgency: 评级机构
    Returns:

    '''
    url = "products/openapi/securities/"+ codeOrId +"/ratings"
    params = {
        "begin": begin,
        "end": end,
        "ratingAgency": ratingAgency
    }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_payment_by_date(codeOrId, paymentDate):
    '''
    证券偿付明细
    https://www.cn-abs.com/openapi.html#/detail/documents?id=60
    
    Args:
        codeOrId: 代码或者证券Id
        paymentDate: 偿付日期
    '''
    url = "products/openapi/securities/"+ codeOrId +"/payments/"+ paymentDate
    params = {}
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_payments(codeOrId):
    '''
    证券偿付历史
    https://www.cn-abs.com/openapi.html#/detail/documents?id=61
    
    Args:
        codeOrId: 代码或者证券Id
    '''
    url = "products/openapi/securities/"+ codeOrId +"/payments"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_snapshots(codeOrId, begin = "", end = ""):
    '''
    证券的动态截面的历史数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=62
    
    Args:
        codeOrId: 代码或者证券Id
        begin: 开始日期
        end: 结束日期
    '''
    url = "products/openapi/securities/"+ codeOrId +"/snapshots"
    params = {
        "begin": begin,
        "end": end
    }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_snapshot(codeOrId, date = ""):
    '''
    证券的最新截面数据
    https://www.cn-abs.com/openapi.html#/detail/documents?id=63
    
    Args:
        codeOrId: 代码或者证券Id
        date: 日期
    '''
    url = "products/openapi/securities/"+ codeOrId +"/snapshot"
    params = {
        "date": date
    }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_scheduled_payments(codeOrId):
    '''
    证券的固定摊还表
    https://www.cn-abs.com/openapi.html#/detail/documents?id=64
    
    Args:
        codeOrId: 代码或者证券Id

    '''
    url = "products/openapi/securities/"+ codeOrId +"/payments/scheduled"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_coupon(codeOrId):
    '''
    证券的发行利率信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=65
    
    Args:
        codeOrId: 代码或者证券Id
    '''
    url = "products/openapi/securities/"+ codeOrId +"/coupon"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_credits(codeOrId):
    '''
    证券增信
    https://www.cn-abs.com/openapi.html#/detail/documents?id=66
    
    Args:
        codeOrId: 代码或者证券Id    
    '''
    url = "products/openapi/securities/"+ codeOrId +"/credits"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_updated(requestTime = ""):
    '''
    获取证券更新历史
    https://www.cn-abs.com/openapi.html#/detail/documents?id=69
    
    Args: 
        requestTime: 更新时间（默认当天）
    '''
    if requestTime == "":
        requestTime = time.strftime("%Y-%m-%d", time.localtime)
    url = "products/openapi/securities/updated/"+ requestTime
    params= {}
    return cnabssdk.clients.cnabsclient().get(url, params)