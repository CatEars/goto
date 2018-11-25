def cond(predicateAndHandlers):
    def do_handler(handler_or_value, args, kwargs):
        if not callable(handler_or_value):
            return handler_or_value
        return handler_or_value(*args, **kwargs)

    def inner(*args, **kwargs):
        for predicate, handler_or_value in predicateAndHandlers:
            if callable(predicate) and predicate(*args, **kwargs):
                return do_handler(handler_or_value, args, kwargs)
            elif not callable(predicate) and predicate:
                return do_handler(handler_or_value, args, kwargs)
    return inner

def ident(val):
    def f():
        return val
    return f

def truthy():
    return True
