import functools
import requests
import sys
from collections import OrderedDict


def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                deco._cache[cache_key]['frequency'] += 1
                return deco._cache[cache_key]['content']
            result = f(*args, **kwargs)
            # видаляємо якшо досягли ліміта
            if len(deco._cache) >= max_limit:
                # search elements in cache with minimal frequency using
                found_key = [key for key in deco._cache.keys() if deco._cache.get(key) == min(
                    deco._cache.values(), key=lambda value_dict: value_dict["frequency"])][0]
                deco._cache.pop(found_key)
            deco._cache[cache_key] = {'content': result, 'frequency': 1}
            print(f'Object cache: {deco._cache}')
            # output for human - URLs in cash
            print('_' * 10, 'In cache', '_' * 10)
            for key in deco._cache.keys():
                print(key[0][0])
            print('_' * 30)
            return result

        deco._cache = OrderedDict()
        return deco
    return internal


def mem_quantity(f):
    @functools.wraps(f)
    def internal(*args, **kwargs):
        result = f(*args, **kwargs)
        print(f'Memory quantity for object: {f} bytes: {sys.getsizeof(result)}')
        return result
    return internal


@mem_quantity
@cache(max_limit=2)
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    try:
        res = requests.get(url)
        return res.content[:first_n] if first_n else res.content
    except BaseException:
        return f'Error connection'


if __name__ == "__main__":
    # fetch_url('https://google.com', first_n=100)
    print(fetch_url('https://google.com', first_n=100))
    print(fetch_url('https://google.com', first_n=100))
    print(fetch_url('http://linuxlog.su', first_n=100))
    print(fetch_url('http://linuxlog.su', first_n=100))
    print(fetch_url('https://google.com', first_n=100))
    # print(fetch_url('http://linuxlog.su', first_n=100))
    # print(fetch_url('https://google.com', first_n=100))
    # print(fetch_url('http://linuxlog.su', first_n=100))
    # print(fetch_url('https://google.com', first_n=100))
    # print(fetch_url('https://google.com.ua', first_n=100))
    # print(fetch_url('https://google.com.ua', first_n=100))
    # print(fetch_url('https://google.com.ua', first_n=100))
    print(fetch_url('https://ithillel.ua', first_n=100))
    print(fetch_url('https://ithillel.ua', first_n=100))
    # print(fetch_url('https://google.com.ua', first_n=100))
    # #print(fetch_url('https://google.com', first_n=None))
