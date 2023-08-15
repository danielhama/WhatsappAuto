import threading


def convert_to_float(num) -> float:
    if type(num) == int:
        return num
    else:
        num = num.replace(',', '.')
        num = float(num)
        return num

def threaded(func):
    def proxy(*args, **kwargs):
        thr = threading.Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
        return thr
    return proxy