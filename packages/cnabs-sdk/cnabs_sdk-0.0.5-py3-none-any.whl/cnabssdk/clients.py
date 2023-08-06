import requests
import json
import cnabssdk
import cnabssdk.configs

class cnabsclient:
    def __init__(self, accessToken = "", apiHost = 'https://api.cn-abs.com'):
        self.apiHost = apiHost
        self.accessToken = accessToken
        if(self.accessToken == ""):
            self.accessToken = cnabssdk.configs.TOKEN
        if(self.apiHost == ""):
            self.apiHost = cnabssdk.configs.API_HOST
        if self.accessToken == "" or self.accessToken == None:
            raise Exception("Please Get Access Token From: https://www.cn-abs.com/openapi.html#/my-token")

        self.head = {
            'user-agent': 'cnabs python client v1.0',
            'Authorization': 'Bearer ' + self.accessToken
        }

    def __checkResponse(self, jsonObj):
        obj = obj_dic(jsonObj)
        code = obj.code
        message = obj.message
        data = obj.data
        if code != 200:
            raise Exception("服务错误: " + message)
        return data
        
        
    def __get_urls(self, resource):
        if resource.startswith('http'):
            return resource
        else:
            return self.apiHost + '/' + resource
        return ""

    def get(self, resource, parameters = {}):
        url = self.__get_urls(resource)
        response = requests.get(url, parameters, headers= self.head)
        if response.status_code != 200:
            raise Exception("服务错误: status_code: " + response.status_code)
        jsonObj = json.loads(response.text)
        return self.__checkResponse(jsonObj)
        
    
def obj_dic(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i, 
                type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top