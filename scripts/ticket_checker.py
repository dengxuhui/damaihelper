import time
import json
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TicketChecker:
    def __init__(self, config: dict):
        self.config = config
        self.target_url = config.get('target_url', '')
        self.check_interval = config.get('check_interval', 30)
        self.is_running = False
        self.scheduler = BackgroundScheduler()
        self.driver = None

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })

    def _check_ticket(self):
        if not self.driver:
            self._init_driver()
        
        try:
            self.driver.get(self.target_url)
            time.sleep(2)
            
            page_source = self.driver.page_source
            
            if '售罄' in page_source or '已售罄' in page_source or 'sold out' in page_source.lower():
                self._on_no_ticket()
            elif '有票' in page_source or '可购买' in page_source or '购买' in page_source:
                self._on_ticket_available()
            else:
                self._on_unknown_status()
                
        except Exception as e:
            print(f"检查票务状态时出错: {e}")

    def _on_no_ticket(self):
        print(f"[{self._get_time()}] 暂无可购票")

    def _on_ticket_available(self):
        print(f"[{self._get_time()}] 🎉 发现可购票！请尽快手动购买！")
        self._notify_user()

    def _on_unknown_status(self):
        print(f"[{self._get_time()}] 票务状态未知，请手动查看")

    def _notify_user(self):
        notification_config = self.config.get('notifications', {})
        if notification_config.get('enabled', False):
            methods = notification_config.get('methods', [])
            if 'email' in methods:
                self._send_email()
            if 'sms' in methods:
                self._send_sms()

    def _send_email(self):
        print("发送邮件通知...")

    def _send_sms(self):
        print("发送短信通知...")

    def _get_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def start(self):
        self.is_running = True
        self.scheduler.add_job(
            self._check_ticket, 
            'interval', 
            seconds=self.check_interval,
            id='ticket_checker'
        )
        self.scheduler.start()
        print(f"票务查询任务已启动，每 {self.check_interval} 秒检查一次")
        print(f"监控地址: {self.target_url}")

    def stop(self):
        self.is_running = False
        self.scheduler.shutdown()
        if self.driver:
            self.driver.quit()
        print("票务查询任务已停止")

    def check_once(self):
        self._check_ticket()


def load_config():
    with open('config/config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def start_ticket_checker(config: dict = None):
    if config is None:
        config = load_config()
    
    checker = TicketChecker(config)
    checker.start()
    return checker


if __name__ == '__main__':
    checker = start_ticket_checker()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止...")
        checker.stop()
