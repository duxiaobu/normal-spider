from Utils import get_md5
import json


class HtmlOutputer(object):
    def __init__(self):
        # 初始化收集数据的列表
        self.all_data = {}
        # 初始化当前页面的url指纹集合，避免重复爬取
        self.url_fingerprint = set()

    def collect_data(self, current_url, data_dict):
        url_md5 = get_md5(current_url)
        # 如果这个页面的url第一次被访问，就添加数据和相应链接的指纹
        if url_md5 not in self.url_fingerprint:
            self.url_fingerprint.add(url_md5)
            self.all_data[current_url] = data_dict
            print("成功保存了{}的页面".format(current_url))
        else:
            print("{}的页面数据已经存在".format(current_url))

    def out_to_file(self):
        # 保存到txt文件中
        try:
            my_file = open("links.txt", "w")
            json.dump(self.all_data, my_file, indent=4)
        except Exception as e:
            print(e)
        finally:
            my_file.close()