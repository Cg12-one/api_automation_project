#修改测试文件添加Allure装饰器
import pytest
import allure
from common.base_test import BaseTest

# @allure.feature() 作用：将测试按功能模块分类
# 报告显示：用户模块 → 用户登录

@allure.feature("用户模块") 

# @allure.story作用：描述用户如何使用该功能
# 属于 feature 的子分类

@allure.story("用户登录")
class TestUserLogin(BaseTest):
    # allure.title() - 自定义测试名称。报告显示：成功登录测试
    @allure.title("成功登录测试")
    @allure.description("验证正确用户名密码可以成功登录")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self,assert_response):
        """成功登录"""
        with allure.step("准备测试数据"):   #step作用：在报告中显示测试步骤， 每一步可以展开/折叠，失败时知道哪一步出错
            payload = {
                "username":"admin",
                "password":123456
            }

        with allure.step("发送登录请求"):
            resp = self.api.post("/post",json=payload)

        with allure.step("验证响应"):
            result = assert_response(resp,status_code=200)
            assert result["json"]["username"] == "admin"

        allure.attach(  #allure附件
            resp.text,
            name="响应体",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.title("失败登录测试")
    @allure.description("验证错误密码返回失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("password,expected_msg",[
        ("wrong","密码错误"),
        ("","密码不能为空"),
        ("123","密码长度不足"),
    ])
    def test_login_fail(self,password,expected_msg):
        """失败登录参数化"""
        with allure.step(f"参数密码：{password}"):
            resp = self.api.post("/post",json={
                "username":"admin",
                "password":password
            })
            #实际业务中验证错误消息
            assert resp.status_code == 200

# tests/test_user_api_allure.py
# import pytest
# import allure
# from common.base_test import BaseTest

# @allure.feature("用户模块")
# @allure.story("用户登录")
# class TestUserLogin(BaseTest):
    
#     @allure.title("成功登录")
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_login_success(self, assert_response):
#         """测试登录成功"""
#         with allure.step("发送登录请求"):
#             resp = self.api.post("/post", json={
#                 "username": "admin",
#                 "password": "123456"
#             })
        
#         with allure.step("验证响应"):
#             result = assert_response(resp, status_code=200)
#             assert result["json"]["username"] == "admin"
    
#     @allure.title("失败登录")
#     @allure.severity(allure.severity_level.NORMAL)
#     def test_login_fail(self):
#         """测试登录失败"""
#         with allure.step("发送错误密码"):
#             resp = self.api.post("/post", json={
#                 "username": "admin",
#                 "password": "wrong"
#             })
        
#         with allure.step("验证状态码"):
#             assert resp.status_code == 200