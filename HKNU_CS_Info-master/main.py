from crawler import Crawler
from classification import Classification
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading, time


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on port 8000...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        # pass
        httpd.server_close()
        print("Server stopped.")


server_thread = threading.Thread(target=run_server)
server_thread.daemon = False
server_thread.start()

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument('--start-fullscreen')
driver = webdriver.Chrome(options=chrome_options)


driver.get("http://localhost:8000")


#### 공지 갱신하는 부분 ####
while True:
    
    crawler1 = Crawler('haksa')
    crawler2 = Crawler('janghak')
    crawler3 = Crawler('hankyong')
    crawler4 = Crawler('chaeyong')
    crawler5 = Crawler('changup')

    crawler1.crawl()
    crawler2.crawl()
    crawler3.crawl()
    crawler4.crawl()
    crawler5.crawl()

    classfier = Classification()
    classfier.process_data()
    print("공지 새로고침 완료")
    time.sleep(100000)