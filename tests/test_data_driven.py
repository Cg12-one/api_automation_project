"""
数据驱动测试说明：

注意：本测试使用 httpbin.org 作为测试服务
- httpbin 只回显请求数据，不做业务验证
- 所有请求都返回 200 状态码
- 实际项目中应使用真实 API 或 Mock 服务

测试目的：
1. 验证数据驱动测试框架
2. 验证 YAML 数据加载
3. 验证参数化测试
4. 演示测试失败场景处理
"""

import pytest
import allure
from common.base_test import BaseTest
from common.data_loader import DataLoader
from pathlib import Path

# 加载测试数据
BASE_DIR = Path(__file__).parent.parent / 'test_data' / 'api_cases'

@allure.feature("数据驱动测试")
class TestDataDriven(BaseTest):
    
    # ========== 登录测试 ==========
    @pytest.mark.parametrize("case_name,case_data", 
        DataLoader.load_yaml(BASE_DIR / 'login_cases.yaml').items())
    @allure.story("登录接口")
    def test_login_cases(self, case_name, case_data, assert_response):
        """数据驱动登录测试"""
        
        with allure.step(f"测试场景：{case_data['description']}"):
            endpoint = case_data["endpoint"]
            method = case_data["method"].lower()
            
            # 发送请求
            if method == "post":
                resp = self.api.post(endpoint, json=case_data.get("json"))
            elif method == "get":
                resp = self.api.get(endpoint, params=case_data.get("params"))
            
            # 断言
            expected = case_data["expected"]
            assert resp.status_code == expected["status_code"]
            
            # 优先级标记
            allure.dynamic.label("priority", case_data.get("priority", "P2"))
            
            print(f"✓ {case_data['description']}")
    
    # ========== 用户管理测试 ==========
    @pytest.mark.parametrize("case_name,case_data",
        DataLoader.load_yaml(BASE_DIR / 'user_cases.yaml').items())
    @allure.story("用户管理接口")
    def test_user_cases(self, case_name, case_data, assert_response):
        """数据驱动用户管理测试"""
        
        with allure.step(f"测试场景：{case_data['description']}"):
            endpoint = case_data["endpoint"]
            method = case_data["method"].lower()
            
            if method == "post":
                resp = self.api.post(endpoint, json=case_data.get("json"))
            elif method == "get":
                resp = self.api.get(endpoint, params=case_data.get("params"))
            elif method == "put":
                resp = self.api.put(endpoint, json=case_data.get("json"))
            elif method == "delete":
                resp = self.api.delete(endpoint, json=case_data.get("json"))
            
            expected = case_data["expected"]
            assert resp.status_code == expected["status_code"]
            
            allure.dynamic.label("priority", case_data.get("priority", "P2"))
            
            print(f"✓ {case_data['description']}")