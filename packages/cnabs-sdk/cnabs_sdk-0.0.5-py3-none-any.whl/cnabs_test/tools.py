import sys
import types
from prettytable import PrettyTable

CALLABLES = types.FunctionType, types.MethodType
def print_tables(data):
    '''
    打印表格
    '''
    if data == None or len(data) == 0:
        print('No Data')
        return
    titles = [key for key, value in data[0].__dict__.items() if not key.startswith("__")]
    tb = PrettyTable(titles)
    for item in data:
        values = [value for key, value in item.__dict__.items() if not key.startswith("__")]
        tb.add_row(values)
    print(tb)

def print_object(obj):
    '''
    打印单个对象
    '''
    # items = obj.__dict__.items()
    # for key, value in items:
    #     if not key.startswith("__"):
    #         print(key + ": " + str(value))

    titles = [key for key, value in obj.__dict__.items() if not key.startswith("__")]
    values = [value for key, value in obj.__dict__.items() if not key.startswith("__")]
    tb = PrettyTable()
    tb.add_column("Field", titles)
    tb.add_column("Value", values)
    tb._max_width = {'Value': 50}
    print(tb)


def print_array(title, array):
    '''
    打印数组
    '''
    tb = PrettyTable()
    tb.add_column(title, array)
    print(tb)
