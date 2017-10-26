import hashlib


def get_md5(url):
    # MD5加密，返回十六进制结果，可以加快查询。
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    print(get_md5("http://www.baidu.com"))


