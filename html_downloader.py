import requests
from lxml import etree
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class HtmlDownloader(object):

    def __init__(self, path):
        self.phantomjs_path = path
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap['phantomjs.page.settings.userAgent'] = UserAgent().random     # 随机生成user_agent
        self.dcap['phantomjs.page.settings.loadImages'] = False   # 不加载图片(根据需要设置)，还有更多设置，更具具体网页设置
        self.driver = webdriver.PhantomJS(executable_path=self.phantomjs_path, desired_capabilities=self.dcap)
        self.driver.implicitly_wait(10)       # 隐式等待时间为10s

    def download(self, root_url, parent_url):
        data_dict = {}
        child_urls = []
        parent_urls = [parent_url]
        try:
            # 判断验证码
            r = requests.get(root_url)
            # 如果为404，则为js生成的post表单的a标签，则使用requests.post()
            if r.status_code == 404:
                response = requests.post(root_url).text
                data_dict['body'] = response
                data_dict['parents'] = parent_urls
                selector = etree.HTML(response)
                link_nodes = selector.xpath("//a/@href")
                data_dict['children'] = link_nodes
                return root_url, data_dict
            else:
                self.driver.get(root_url)
                # 保存原页面
                data_dict['body'] = self.driver.page_source
                # 爬取所有的a标签
                link_nodes = self.driver.find_elements_by_tag_name('a')
                # 为了使element在当前driver的缓存中，因为driver的跳转，会清空所属的缓存。
                for i in range(len(link_nodes)):
                    # 通过点击链接，跳转页面，再返回其链接的方式获取子链接，这样就可以收集各种js方式的链接
                    self.driver.find_elements_by_tag_name('a')[i].click()
                    child_url = self.driver.current_url
                    child_urls.append(child_url)
                    self.driver.back()
                data_dict['children'] = child_urls
                data_dict['parents'] = parent_urls
                return self.driver.current_url, data_dict

        except Exception as e:
            print(e)

    def driver_close(self):
        # 关闭driver
        if self.driver:
            self.driver.close()