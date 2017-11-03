import hashlib
import time


class Cath(object):
    def __init__(self, *args, **kwargs):
        self.session_data = {}

    def __contains__(self, item):
        '''当示例对象被用in判断是否里面包含某个参数的时候调用'''
        return item in self.session_data

    def set_item(self, random_str, key, value):
        self.session_data[random_str][key] = value

    def get_item(self, random_str, key):
        return self.session_data[random_str].get(key)

    def delete_item(self, random_str, key):
        del self.session_data[random_str][key]

    def clear(self, random_str):
        del self.session_data[random_str]


P = Cath()


class Session(object):
    '''
    自定义的一个session框架
    美丽的杰作
    '''

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.random_str = None
        self.now_time = time.time()
        self.session_data = P
        client_random_str = self.request.get_cookie('session_id')
        if not client_random_str:
            self.random_str = self.create_random_str()
            self.session_data.session_data[self.random_str] = {}

        else:
            if client_random_str in self.session_data:
                self.random_str = client_random_str
            else:
                self.random_str = self.create_random_str()
                self.session_data.session_data[self.random_str] = {}
        self.request.set_cookie(
            'session_id', self.random_str, expires=self.now_time + 1800)

    def create_random_str(self):
        v = str(time.time())
        m = hashlib.md5()
        m.update(bytes(v, encoding='utf-8'))
        return m.hexdigest()

    def __setitem__(self, key, value):
        self.session_data.set_item(self.random_str, key, value)

    def __getitem__(self, key):
        return self.session_data.get_item(self.random_str, key)

    def __delitem__(self, key):
        self.session_data.delete_item(self.random_str, key)

    def clear(self):
        self.session_data.clear(self.random_str)
