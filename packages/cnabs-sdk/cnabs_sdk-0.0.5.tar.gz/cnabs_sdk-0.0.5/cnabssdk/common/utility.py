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

class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)