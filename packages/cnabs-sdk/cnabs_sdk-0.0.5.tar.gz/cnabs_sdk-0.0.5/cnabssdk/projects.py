import cnabssdk.clients


def get_statistic_by_exchanges(begin = "", end = "", statisticItem = "amount"):
    '''
    统计交易所、ABN市场的审批项目
    https://www.cn-abs.com/openapi.html#/detail/documents?id=39
    
    Args:
        begin: 开始时间
        end : 结束时间
        statisticItem: 按单数还是金额统计,number表示单数,amount表示金额
    '''
    url = "projects/openapi/projects/exchanges"
    params = {
        begin: begin,
        end: end,
        statisticItem: statisticItem
    }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_project_timelines(id):
    '''
    获取单个项目的审批周期
    https://www.cn-abs.com/openapi.html#/detail/documents?id=40
    
    Args:
        id: 产品id
    '''
    url = "projects/openapi/projects/"+ id +"/timelines"
    return cnabssdk.clients.cnabsclient().get(url, {})

def get_projects(keywords = "", begin = "", end = "", status= ""):
    '''
    获取交易所、ABN审批项目列表
    https://www.cn-abs.com/openapi.html#/detail/documents?id=41
    
    Args:
        keywords: keywords
        end: 结束时间
        begin: 开始时间
        status: 状态
    '''
    url = "projects/openapi/projects"
    params = {
        "keywords": keywords,
        "begin": begin,
        "end": end,
        "status": status
    }
    return cnabssdk.clients.cnabsclient().get(url, params)