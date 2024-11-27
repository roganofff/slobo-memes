import inspect


class Provide:
    def __init__(self, value):
        self.value = value


def inject(f):
    sig = inspect.signature(f)
    async def wrapper(*args, **kwargs):
        for param in sig.parameters.values():
            if isinstance(param.default, Provide):
                async for db in param.default.value():
                    kwargs[param.name] = db
                    return await f(*args, **kwargs)
    return wrapper
