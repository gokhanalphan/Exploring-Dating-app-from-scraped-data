import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
import time

class RedditSpider(scrapy.Spider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = [
        "https://www.reddit.com/r/Tinder/comments/5kdsfy/using_tinder_for_friends_only_bf_is_being_weird/"
    ]

    def __init__(self, *args, **kwargs):
        super(RedditSpider, self).__init__(*args, **kwargs)
        # WebDriverManager kullanarak ChromeDriver'ı kurun
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get(response.url)

        # Sayfanın sonuna kadar scroll yaparak tüm yorumların yüklenmesini sağla
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Yorumların yüklenmesi için bekle
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        sel = Selector(text=self.driver.page_source)

        # Ana yorumları seçmek için CSS seçiciyi kullanın
        comments = sel.css('#-post-rtjson-content p')
        for comment in comments:
            text = comment.css('::text').get()
            if text:
                yield {
                    'text': text
                }

        self.driver.quit()
