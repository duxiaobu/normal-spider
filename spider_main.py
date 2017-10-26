import html_downloader
import html_outputer
from Utils import get_md5


class SpiderMain(object):

    def __init__(self, path):
        self.downloader = html_downloader.HtmlDownloader(path)
        self.outputer = html_outputer.HtmlOutputer()

    def crawl(self, root_url, parents_url=None):
        current_url, data_dcit = self.downloader.download(root_url, parent_url=parents_url)
        self.outputer.collect_data(current_url, data_dcit)
        # 判断返回的列表中是否有子链接
        if data_dcit['children']:
            for new_url in data_dcit['children']:
                item = get_md5(new_url)
                # 判断该链接是否爬取过,不存在就继续爬取
                if item not in self.outputer.url_fingerprint:
                    self.crawl(root_url=new_url, parents_url=current_url)
                # 存在了，就在该子链接的父链接列表中增加该url
                else:
                    self.outputer.all_data[new_url]['parents'].append(current_url)

if __name__ == "__main__":
    root_url = "http://127.0.0.1:8080/main.html"
    phantomjs_path = r"D:\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe"   # 测试机上phantomjs的地址
    obj_spider = SpiderMain(phantomjs_path)
    obj_spider.crawl(root_url)
    '''等待spider递归爬取完成，再输出列表。
       因为页面的数据较少，为了速度，就直接保存在内存的列表中，最后再输出到txt文件中；
       如果爬取页面丰富的页面，则可以爬取一个页面的数据就持久化保存到文件或数据库中。'''
    obj_spider.outputer.out_to_file()
    # 关闭driver
    obj_spider.downloader.driver_close()

