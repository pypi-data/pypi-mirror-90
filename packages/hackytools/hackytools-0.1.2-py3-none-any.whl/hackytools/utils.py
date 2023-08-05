from functools import wraps
import sys
import requests
import socket
import time
import shutil


def whatsmyip():
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['local', '-local', '--local']:
            return socket.gethostbyname(socket.gethostname())
    return requests.get('https://api.ipify.org').text.strip()

def icanhazip():
    return requests.get('https://ipv4.icanhazip.com').text.strip()

def ftime(ns):
    if ns < 1000:
        return f"{ns:.2f} ns"
    elif ns < 1000000:
        return f"{ns/1000:.2f} \u00B5s"
    elif ns < 1000000000:
        return f"{ns/1000000:.2f} ms"
    else:
        return f"{ns/1000000000:.2f} s"

def ftime_ns(ns):
    return ftime(ns)

def elapsed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ts = time.perf_counter_ns()
        result = func(*args, **kwargs)
        te = time.perf_counter_ns() - ts
        sys.stdout.write(f"{func.__qualname__!r} elapsed: {ftime(te)}\n")
        return result
    return wrapper

def bestof(argument=None, freq=7):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = []
            for _ in range(freq):
                ts = time.perf_counter_ns()
                result = func(*args, **kwargs)
                te = time.perf_counter_ns() - ts
                times.append(te)
            avg, best, worst = sum(times)/len(times), min(times), max(times)
            sys.stdout.write(f"{func.__qualname__!r} elapsed (best of {freq}): avg: {ftime(avg)} | best: {ftime(best)} | worst: {ftime(worst)}\n")
            return result
        return wrapper
    if callable(argument):
        return decorator(argument)
    elif isinstance(argument, int):
        freq = argument
    return decorator

# def flatten(data, depth=None):
#     if depth is None:
#         return sum(([x] if not isinstance(x, list) else flatten(x) for x in data), [])
#     else:
#         results = []
#         d = 0
#         for item in data

def sprint(text):
    return sys.stdout.write(str(text))

def spout(text, pos=None):
    if pos:
        x,y = pos
        return sys.stdout.write(f"\x1b[s\x1b[{x};{y}H{text}\x1b[u")
    return sys.stdout.write(f"{text}")
