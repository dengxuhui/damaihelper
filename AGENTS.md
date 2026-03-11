# AGENTS.md - 项目开发指南

本文件为 Agentic Coding 代理提供项目开发规范。

## 1. 项目概述

- **项目名称**: TicketMaster Pro (大麦网抢票工具)
- **语言**: Python 3.10+
- **主要依赖**: selenium==4.1.0, appium-python-client==2.0.0, pillow==8.4.0, apscheduler==3.8.0, pytesseract==0.3.8
- **入口文件**: ticket_script.py, scripts/main.py, GUI.py

## 2. 环境配置

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
# 主脚本方式
python ticket_script.py

# 模块方式
python scripts/main.py

# GUI 方式
python GUI.py
```

## 3. 代码风格指南

### 3.1 导入规范

- 每个导入单独占一行
- 标准库导入放在最前面
- 第三方库导入放在中间
- 本地模块导入放在最后
- 使用 `from x import y` 风格而非 `import x` 当只用到模块的少数几个功能
- 避免使用通配符导入 `from x import *`

```python
# 正确示例
import json
import time
from os.path import exists

from selenium import webdriver
from selenium.webdriver.common.by import By

from scripts.captcha_solver import solve_captcha
from scripts.scheduler import schedule_tasks
```

### 3.2 命名规范

- **变量名**: 使用小写字母加下划线 (snake_case)
  - 正确: `ticket_price`, `user_account`
  - 错误: `ticketPrice`, `useraccount`

- **函数名**: 使用小写字母加下划线 (snake_case)
  - 正确: `def get_cookie():`
  - 错误: `def getCookie():`

- **类名**: 使用 CapWords (PascalCase)
  - 正确: `class Concert(object):`
  - 错误: `class concert:`

- **常量**: 使用全大写字母加下划线
  - 正确: `MAX_RETRY = 5`
  - 错误: `max_retry = 5`

- **私有变量/函数**: 前缀单下划线
  - 正确: `_private_method()`, `_internal_var`
  - 错误: `__private_method__()` (双下划线是 name mangling)

### 3.3 函数和类

- 类定义前后各留两个空行
- 方法之间留一个空行
- 函数不宜过长，建议不超过 50 行
- 每个函数应有单一职责
- 使用类型注解 (type hints) 提高可读性

```python
# 正确示例
class Concert:
    def __init__(self, date: int, session: int, price: int):
        self.date = date
        self.session = session
        self.price = price

    def get_cookie(self) -> None:
        """获取账号的 cookie 信息"""
        pass
```

### 3.4 错误处理

- 优先使用具体的异常类型
- 避免裸 `except:` 语句，使用 `except Exception as e:`
- 记录异常信息供调试

```python
# 正确示例
try:
    cookies = load(open("cookies.pkl", "rb"))
except Exception as e:
    print(f"Cookie 加载失败: {e}")
    # 处理逻辑
```

- 使用 finally 清理资源

```python
try:
    driver = webdriver.Chrome()
    # 操作
finally:
    if driver:
        driver.quit()
```

### 3.5 代码格式化

- 使用 4 空格缩进 (不用 Tab)
- 行长度不超过 120 字符
- 运算符两侧加空格
- 逗号后加空格

```python
# 正确示例
prefs = {"profile.managed_default_content_settings.images": 2,
         "profile.managed_default_content_settings.javascript": 1}
options.add_experimental_option("prefs", prefs)
```

- 使用 Black 格式化代码 (如有)

```bash
pip install black
black scripts/
```

### 3.6 类型注解

- 为公共函数添加类型注解
- 复杂类型使用 TypeAlias

```python
from typing import Optional, List, Dict

def get_account_info(account_id: str) -> Optional[Dict[str, str]]:
    pass

def process_tickets(tickets: List[int]) -> List[Dict]:
    pass
```

### 3.7 注释规范

- 使用中文注释
- 保持注释与代码同步更新
- 公共 API 添加 docstring

```python
def get_cookie(self):
    """获取账号的 cookie 信息"""
    pass
```

### 3.8 日志和输出

- 使用 `print()` 输出关键信息
- 中文输出使用 `u"中文内容"` 确保兼容性

```python
print(u"###请扫码登录###")
print(f"开始为账户 {account_id} 执行抢票任务")
```

## 4. 项目结构

```
damaihelper/
├── ticket_script.py       # 主抢票脚本
├── GUI.py                 # GUI 界面
├── requirements.txt       # 依赖列表
├── config/
│   ├── config.json        # 主配置文件
│   ├── platform_config.json
│   ├── proxy_pool.json
│   └── demo_config.json
├── scripts/
│   ├── __init__.py
│   ├── main.py            # 主入口模块
│   ├── selenium_driver.py # Selenium 驱动
│   ├── appium_simulator.py
│   ├── captcha_solver.py  # 验证码识别
│   ├── scheduler.py       # 任务调度
│   └── multi_account_manager.py
├── logs/                  # 日志目录
└── chromedriver          # 浏览器驱动
```

## 5. 开发注意事项

### 5.1 Selenium 使用

- 使用 `webdriver.ChromeOptions()` 配置浏览器选项
- 移除 webdriver 痕迹 (重要)
- 使用 `WebDriverWait` 等待元素

```python
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
WebDriverWait(self.driver, 10, 0.1).until(EC.title_contains('商品详情'))
```

### 5.2 配置文件

- 敏感信息不要硬编码
- 使用 config/config.json 存储配置

### 5.3 浏览器驱动

- 确保 chromedriver 版本与 Chrome 浏览器版本匹配
- Windows 使用 chromedriver.exe，macOS/Linux 使用 chromedriver

## 6. 代码审查清单

- [ ] 导入顺序正确
- [ ] 命名符合规范
- [ ] 包含适当的错误处理
- [ ] 函数/方法有类型注解
- [ ] 代码格式化正确
- [ ] 无硬编码敏感信息
