"""测试基类"""
import pytest
import logging
from .request import APIRequest

#配置日志
logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    # 格式：时间 - 模块名 - 级别 - 消息
)

class BaseTest:
    """测试基类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前执行"""
        self.api = APIRequest()
        yield
        self.api.close()

    @pytest.fixture
    def assert_response(self):
        """断言响应工具"""
        def _assert(resp,status_code=200,contains=None):
            assert resp.status_code == status_code, \
                f"状态码错误：{resp.status_code} != {status_code}"
            if contains:
                assert contains in resp.text, \
                    f"响应不包含：{contains}"
            # 返回 JSON 数据
            return resp.json()
        return _assert