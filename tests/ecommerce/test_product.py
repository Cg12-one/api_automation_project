import pytest
import allure
from common.base_test import BaseTest
from common.assertions import APIAssert

@allure.feature("商品模块")
class TestProductAPI(BaseTest):

    @allure.story("商品查询")
    @allure.title("根据分类查询商品")
    def test_query_by_category(self,assert_response):
        """按分类查询商品"""
        resp = self.api.get("/get",params={
            "category":"electronics",
            "page":1,
            "limit":10
        })
        result = assert_response(resp,status_code=200)
        assert "args" in result

    @allure.story("商品创建")
    @allure.title("创建新商品")
    def test_create_product(self,assert_response):
        """创建商品"""
        payload = {
            "name":"测试商品",
            "price":99.99,
            "stock":100,
            "category":"test"
        }
        resp = self.api.post("/post",json=payload)
        result = assert_response(resp,status_code=200)
        assert result["json"]['name'] == "测试商品"

    @allure.story("商品删除")
    @allure.title("关键词搜索商品")
    @pytest.mark.parametrize("keyword,expected_count",[
        ("手机",5),
        ("电脑",3),
        ("不存在的商品",0),
    ])
    def test_search_product(self,keyword,expected_count):
        """搜索商品"""
        resp = self.api.get("/get",params={"q":keyword})
        assert resp.status_code == 200
        #实际业务中验证搜索结果数量
        print(f"\n搜索'{keyword}',预期{expected_count}条结果")