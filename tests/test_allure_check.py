import allure

@allure.feature("检查功能")
def test_check():
    allure.step("测试步骤")
    assert True