import pytest
import json
import os
# 添加父目录到路径
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.base_test import BaseTest

#加载测试数据
DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "../test_data/user_cases.json"
)

with open(DATA_FILE,'r',encoding='utf-8') as f:
    TEST_CASES = json.load(f)

class TestUserAPI(BaseTest):
    """用户接口测试"""

    @pytest.mark.parametrize("case_name,case_data",TEST_CASES.items())
    def test_user_scenarios(self,case_name,case_data,assert_response):
        """数据驱动测试用户场景"""
        endpoint = case_data["endpoint"]
        method = case_data["method"].lower()

        #发送请求
        if method == "get":
            resp = self.api.get(endpoint,params=case_data.get("params"))
        elif method == "post":
            if "json" in case_data:
                resp = self.api.post(endpoint,json=case_data["json"])
            else:
                reap = self.api.post(endpoint,data=case_data["data"])

        #断言
        expected = case_data["expected"]
        if "status_code" in expected:
            assert resp.status_code == expected["status_code"]

        print(f"\n√ {case_name}测试通过")


    def test_login_success(self,assert_response):
        """测试登录成功"""
        resp = self.api.post("/post",json={
            "username":"admin",
            "password":"123456"
        })
        result = assert_response(resp,status_code=200)      # result 现在等于：result = {    "args": {},    "data": "",    "files": {},    "form": {},    "headers": {...},    "json": {        "username": "admin",        "password": "123456"    },    "origin": "120.197.120.174",    "url": "https://httpbin.org/post"}
        assert result["json"]["username"] == "admin"

    def test_login_fail(self):
        """测试登录失败"""
        resp = self.api.post("/post",json={
            "username":"admin",
            "password":"wrong"
        })
        
        assert resp.status_code == 200
        #实际业务中这里应该验证错误信息
        print("\n√ 登录失败场景测试通过")  

    