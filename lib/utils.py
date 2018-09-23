class POJO: pass
def as_obj(dc):
    obj = POJO()
    for key, val in dc.items(): setattr(obj, key, val)
    return obj

def add_method(obj, method, name=None):
    if name is None:
        name = method.__name__
    setattr(obj, name, method)
