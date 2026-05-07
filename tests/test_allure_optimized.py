import pytest
import allure
import json
from common.base_test import BaseTest
from common.data_loader import DataLoader
from pathlib import Path

@allure.feature("用户模块")
@allure.epic("电商API自动化")
class TestUserAllure(BaseTest):

    @allure.story("用户登录 ")
    @allure.title("TC001-成功登录测试")
    @allure.description("""
    测试目的：验证正确用户名密码可以成功登录

    前置条件：
    -用户已注册
    -账号状态正常

    测试步骤：
    1.准备测试数据
    2.发生登录请求
    3.验证响应状态码
    4.验证返回数据

    预期结果
    -状态码200
    -返回用户信息
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("owner","测试工程师")
    @allure.label("priority","P0")
    @allure.link("https://jira.example.com/PROJ-123",name="JIRA需求")
    def test_login_success(self,assert_response):
        """成功登录测试"""

        #步骤1：准备测试数据
        with allure.step("准备测试数据"):
            login_data = {
                "username":"admin",
                "password":"123456"
            }
            allure.attach(
                json.dumps(login_data,indent=2,ensure_ascii=False),
                name="请求数据",
                attachment_type=allure.attachment_type.JSON
            )

        #步骤2：发送登录请求
        with allure.step("发送登录请求"):
            resp = self.api.post("/post",json=login_data)

            # 附加请求信息
            request_info = f"""
URL:{resp.url}
Method:POST
Status Code:{resp.status_code}
Response Time:{resp.elapsed.total_seconds()*1000:.2f}ms
            """
            allure.attach(request_info,name="请求信息",
                        attachment_type=allure.attachment_type.TEXT)

        #步骤3：验证响应状态码
        with allure.step("验证响应状态码"):
            assert resp.status_code == 200,\
                f"状态码错误：{resp.status_code} != 200"


        #步骤4：验证返回数据
        with allure.step("验证返回数据"):
            result = resp.json()
            assert result["json"]["username"] == "admin"

            #附加响应数据
            allure.attach(
                json.dumps(result,indent=2,ensure_ascii=False),
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        #步骤5：验证响应时间
        with allure.step("验证响应时间"):
            response_time = resp.elapsed.total_seconds() * 1000
            assert response_time < 1000,\
                f"响应时间超限：{response_time}ms > 1000ms"
            allure.attach(f"响应时间：{response_time:.2f}ms",
                           name="性能数据",
                           attachment_type=allure.attachment_type.TEXT)

    @allure.story("用户登录")
    @allure.title("TC002-失败登录测试-参数化")
    @allure.description("验证错误密码、空密码等情况登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("password,expected_msg,priority",[
        ("wrong_password","密码错误","P0"),
        ("","密码不能为空","P1"),
        ("123","密码长度不足","P2"),
    ])
    @allure.label("test_type","异常场景")
    def test_login_fail(self,password,expected_msg,priority,assert_response):
        """失败登录参数化测试"""

        with allure.step(f"测试密码：{password if password else '(空)'}"):
            login_data = {
                'username':"admin",
                "password":password
            }

            allure.attach(
                json.dumps(login_data,indent=2,ensure_ascii=False),
                name="请求数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("发送登录请求"):
            resp = self.api.post("/post",json=login_data)

        with allure.step("验证状态码"):
            assert resp.status_code == 200

        #动态设置优先级
        allure.dynamic.label("priority",priority)

        print(f"密码：'{password}'测试通过")
        