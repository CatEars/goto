def cond(predicateAndHandlers):
    def inner(*args, **kwargs):
        for predicate, handler in predicateAndHandlers:
            if predicate(*args, **kwargs):
                return handler(*args, **kwargs)
    return inner

def ident(val):
    def f():
        return val
    return f

def truthy():
    return True
