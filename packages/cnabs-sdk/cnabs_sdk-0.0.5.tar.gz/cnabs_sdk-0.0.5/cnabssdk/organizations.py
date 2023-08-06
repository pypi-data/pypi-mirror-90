import cnabssdk.clients

def get_organization(orgNameOrId):
    '''
    机构信息
    https://www.cn-abs.com/openapi.html#/detail/documents?id=16
    
    Args:
        orgNameOrId: 机构名称或者Id
    '''
    url = "organization/openapi/organizations/"+ orgNameOrId
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_industries():
    '''
    行业列表
    https://www.cn-abs.com/openapi.html#/detail/documents?id=67
    
    Args:
        source: 行业类别，默认为证监会行业分类
    '''
    url = "organization/openapi/organizations/industry/证监会行业分类"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_organizations(keywords = "", industry = ""):
    '''
    机构列表
    https://www.cn-abs.com/openapi.html#/detail/documents?id=17
    
    Args:
        keywords: 查询关键字
        industry: 证监会行业
    '''
    url = "organization/openapi/organizations"
    params = {"keywords": keywords, "industry": industry }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_organization_ratings(orgNameOrId):
    '''
    机构评级
    https://www.cn-abs.com/openapi.html#/detail/documents?id=18
    
    Args:
        orgNameOrId: 机构名称或者Id
    '''
    url = "organization/openapi/organizations/"+ orgNameOrId +"/ratings"
    return cnabssdk.clients.cnabsclient().get(url, {})

