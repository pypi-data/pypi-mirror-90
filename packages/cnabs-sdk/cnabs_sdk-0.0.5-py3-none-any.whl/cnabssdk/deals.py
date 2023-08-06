import cnabssdk.clients

def get_list(keywords = "", status = "", year = "", catalog = "", orgname = ""):
    '''
    获得产品列表信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=45
    
    Args:
        keywords: 关键字
        status:  产品状态，支持中英文参数，选项如下（中文／英文）：过会中/Auditing 、发行中/Issueing 、存续期/Issued 、已清算/End 、停售/Stop 
        year: 年份
        catalog: 产品分类
        orgName: 机构名称
    '''
    url = "products/openapi/deals"
    params = {
        "keywords": keywords,
        "status": status,
        "year": year,
        "catalog": catalog,
        "orgname": orgname
        }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_detail(dealIdOrName):
    '''
    产品详情
    https://www.cn-abs.com/openapi.html#/detail/documents?id=46
    
    Args:
        nameOrId: 产品全称或者Id
    '''
    url = "products/openapi/deals/" + dealIdOrName
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_dates(nameOrId, dateType = ""):
    '''
    产品相关日期
    https://www.cn-abs.com/openapi.html#/detail/documents?id=47
    
    Args:
        nameOrId: 产品全称或者Id
        dateType: 时间类型（默认为空）
    '''
    url = "products/openapi/deals/"+ nameOrId +"/dates"
    params = {"dateType": dateType }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_payments_dates(nameOrId):
    '''
    产品的偿付列表
    https://www.cn-abs.com/openapi.html#/detail/documents?id=48
    
    Args:
        nameOrId: 产品全称或者Id
    '''
    url = "products/openapi/deals/"+ nameOrId +"/payments/schedule"
    return  cnabssdk.clients.cnabsclient().get(url, {})

def get_deal_orgs(nameOrId):
    '''
    产品的相关机构信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=49
    
    Args:
        nameOrId: 产品全称或者Id
    '''
    url = "products/openapi/deals/"+ nameOrId +"/orgs"
    return  cnabssdk.clients.cnabsclient().get(url, {})
 
def get_deal_orgs_by_role(nameOrId, role = ""):
    '''
    通过角色获得参与机构信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=50
    
    Args:
        nameOrId: 产品全称或者Id
        role: 机构角色
    '''
    url = "products/openapi/deals/"+ nameOrId +"/orgs/"+ role
    params = {"role": role }
    return  cnabssdk.clients.cnabsclient().get(url, params)

def get_executions(nameOrId):
    '''
    产品承销信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=51
    
    Args:
        nameOrId: 产品全称或者Id
    '''
    url = "products/openapi/deals/"+ nameOrId +"/orgs/execution"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_snapshot(nameOrId, date = ""):
    '''
    产品动态信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=52
    
    Args:
        nameOrId: 产品全称或者Id
        date：日期 
    '''
    url = "products/openapi/deals/"+ nameOrId +"/snapshot"
    params = {"date": date }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_snapshots(nameOrId, begin = None, end = None):
    '''
    产品动态信息历史
    https://www.cn-abs.com/openapi.html#/detail/documents?id=53
    
    Args:
        nameOrId: 产品全称或者Id
        begin: 开始时间
        end: 结束时间
    '''
    url = "products/openapi/deals/"+ nameOrId +"/snapshots"
    params = {"begin": begin , "end": end }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_securities(nameOrId):
    '''
    产品证券简略信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=54
    
    Args:
        nameOrId: 产品全称或者Id
    '''
    url = "products/openapi/deals/"+ nameOrId +"/securities"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_feePayment(nameOrId, paymentDate = ""):
    '''
    产品费用偿付
    https://www.cn-abs.com/openapi.html#/detail/documents?id=55
    
    Args:
        nameOrId: 产品全称或者Id
        paymentDate: 支付日
    '''
    url = "products/openapi/deals/"+ nameOrId +"/feePayment"
    params = {"paymentDate": paymentDate}
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_categories():
    '''
    产品类别列表
    https://www.cn-abs.com/openapi.html#/detail/documents?id=68
    
    Args:
        source: 产品类别的分类
    '''
    url = "products/openapi/deals/category/" 
    params = {}
    return cnabssdk.clients.cnabsclient().get(url, params)





