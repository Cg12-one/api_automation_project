import os

#基础URL
BASE_URL = "https://httpbin.org"

#超时时间
TIMEOUT = 30

#日志配置
LOG_LEVEL = "INFO"

#报告路径
REPORT_DIR = os.path.join(os.path.dirname(__file__),"../reports")
# __file__ = 当前文件的绝对路径
# os.path.join() = 拼接路径（自动处理 / 或 \）
