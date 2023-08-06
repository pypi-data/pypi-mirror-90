import cnabssdk.common.utility

class base_entry(object):
    def __init__(self,id= '' ,code = '', name = ''):
        self.id = id
        self.code = code
        self.name = name

    def load_from_dict(self, obj):
        self.id = obj['id']
        self.code = obj['code']
        self.name = obj['name']

class deal_list_entry(base_entry):
    def __init__(self, id = "", name = "", code = "", status = "", shortname = ""):
        super().__init__(id, code, name)
        self.status = status
        self.short_name = shortname
