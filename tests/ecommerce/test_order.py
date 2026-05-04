import pytest
import allure
from common.base_test import BaseTest
from common.assertions import APIAssert
from datetime import datetime

@allure.feature("订单模式")
class TestOrderAPI(BaseTest):

    @pytest.fixture
    def order_data(self):
        """订单测试数据"""
        return {
            "user_id":123,
            "items":[
                {"product_id":1001,"quantity":2},
                {"product_id":1002,"quantity":1}
            ],
            "address":"测试地址",
            "payment":"online"
        }
    
    @allure.story("订单创建")
    @allure.title("正常创建订单")
    def test_create_order(self,order_data,assert_response):
        """创建订单"""
        resp = self.api.post("/post",json=order_data)
        result = assert_response(resp,status_code=200)
        assert result["json"]["user_id"] == 123

    @allure.story("订单查询")
    @allure.title("根据订单号查询")
    def test_query_order(self):
        """查询订单"""
        resp = self.api.get("/get",params={"order_no":"ORD20260425001"})
        assert resp.status_code == 200 

    @allure.story("订单状态")
    @allure.title("更新订单状态")
    @pytest.mark.parametrize("from_status,to_status",[
        ("pending","paid"),
        ("paid","shipped"),
        ("shipped","completed"),
    ])
    def test_update_status(self,from_status,to_status):
        """更新订单状态"""
        payload = {
            "order_no":"ORD20260425001",
            "from":from_status,
            "to":to_status
        }
        resp = self.api.put("/put",json=payload)
        assert resp.status_code == 200

    @allure.story("订单取消")
    @allure.title("取消未支付订单")
    def test_cancel_order(self):
        """取消订单"""
        resp = self.api.delete("/delete",json={
            "order_no":"ORD20260425001",
            "reason":"用户取消"
        })
        assert resp.status_code == 200

    @allure.story("订单列表")
    @allure.title("分页查询用户订单")
    def test_order_list(self,assert_response):
        """订单列表"""
        resp = self.api.get("/get",params={
            "user_id":123,
            "page":1,
            "page_size":10,
            "status":"all"
        })
        result = assert_response(resp,status_code=200)
        assert "args" in result