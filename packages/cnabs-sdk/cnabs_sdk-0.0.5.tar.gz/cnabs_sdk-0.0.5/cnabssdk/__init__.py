import cnabssdk.configs

print("Import CNABS SDK")

def init(token, api = "https://api.cn-abs.com"):
    configs.TOKEN = token
    configs.API_HOST  = api