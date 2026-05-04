"""请求封装类"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging  #日志模块
from .config import BASE_URL,TIMEOUT

logger = logging.getLogger(__name__)    # __name__ = 当前模块名 输出：'api_framework.common.request'    作用：给日志打标签，知道是哪个模块产生的日志

class APIRequest:
    """API请求封装"""

    #__前缀 私有方法，外部无法访问  __init__ = 构造函数（创建对象时自动调用）
    def __init__(self,base_url=None):
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=3,  # 最多重试3次
            backoff_factor=1,  # 重试间隔：1, 2, 4秒
            status_forcelist=[429, 500, 502, 503, 504],  # 这些状态码重试
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    #_ 表示方法只在类内部使用，外部代码不应该直接调用

    def _build_url(self,endpoint):
        """构建完整URL"""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"    # lstrip('/') 的作用：去掉开头的 /

    def _log_request(self,method,url,**kwargs):
        """记录请求日志"""
        logger.info(f"{method} {url}")
        if kwargs.get("params"):
            logger.debug(f"Params:{kwargs['params']}")
        if kwargs.get("json"):
            logger.debug(f"JSON:{kwargs['json']}")

    def _log_response(self,response):
        """记录响应日志"""
        logger.info(f"Status:{response.status_code}")
        logger.debug(f"Response:{response.text[:200]}") # 记录响应内容（前200个字符）

    def request(self,method,endpoint,**kwargs):
        """通用请求方法"""
        url = self._build_url(endpoint)
        kwargs.setdefault("timeout",TIMEOUT)

        self._log_request(method.upper(),url,**kwargs)

        response = self.session.request(method,url,**kwargs)

        self._log_response(response)
        return response

    def get(self,endpoint,**kwargs):
        return self.request("GET",endpoint,**kwargs)

    def post(self,endpoint,**kwargs):
        return self.request("POST",endpoint,**kwargs)

    def put(self,endpoint,**kwargs):
        return self.request("PUT",endpoint,**kwargs)

    def delete(self,endpoint,**kwargs):
        return self.request("DELETE",endpoint,**kwargs)
        
    def close(self):
        """关闭Session"""
        self.session.close()
           


