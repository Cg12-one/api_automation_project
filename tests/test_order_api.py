import pytest
from common.base_test import BaseTest
from common.data_loader import DataLoader
import os

class TestOrderAPI(BaseTest):
    """订单接口测试"""

    #加载yaml数据
    ORDER_CASES = DataLoader.load_yaml(
        os.path.join(os.path.dirname(__file__),
                        "../test_data/order_cases.yaml")
    )


    @pytest.mark.parametrize("case_name,case_data",ORDER_CASES.items())
    def test_order_operations(self,case_name,case_data,assert_response):
        """测试订单操作"""
        endpoint = case_data['endpoint']
        method = case_data['method'].lower()

        if method == 'get':
            resp = self.api.get(endpoint,params=case_data.get("params"))
        elif method == 'post':
            resp = self.api.post(endpoint,json=case_data.get("json"))
        elif method == 'delete':
            resp = self.api.delete(endpoint,json=case_data.get("json"))

        expected = case_data["expected"]
        if "status_code" in expected:
            assert resp.status_code == expected["status_code"]
        
        print(f"\n√ {case_name}测试通过")