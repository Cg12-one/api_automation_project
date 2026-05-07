#API自动化测试框架

##项目简介
基于Python + pytest 的接口自动化测试框架，支持数据驱动，Allure报告。CI/CD集成


##项目结构
api_framework/
-。github/workflows/ #CI/CD配置
-common/    #公共租界
    -config.py  #配置
    -request.py #请求封装
    -base_test.py   #测试基类
    -assertions.py  #断言工具
    -data_loaderpy  #数据加载
-test_data  #测试数据
    -api_cases/ #YAML测试用例
    -user_cases.json
    -order_cases.yaml
-tests/ #测试用例
    -test_user_api.py
    -test_order_api.py
    -test_data_driven.py
    -ecommerce/ #业务模块测试
-utils/ #工具脚本
    -dingtalk_notify.py
-reports/   #测试报告
-requirements.txt   #依赖
-pytest.ini #pytest配置
-README.md  #本文档

###环境要求
-python 3.8+
-pytest 7.0+
-requests 2.28+

###安装依赖
```bash
pip install -r requirements.txt

运行测试

#运行所有测试
pytest tests/ -v

#运行指定模块
pytest tests/ecommerce/ -v

#生成HTML报告
pytest tests/ --html=reports/report.html --self-contained-html

#生成Allure报告
pytest tests/ --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

#生产覆盖率报告
pytest tests/ --cov=common --cov=tests --cov-report=html

CI/CD配置
项目已配置GitHub Actions，代码推送到main分支自动执行测试。

通知配置
-钉钉通知
    1.创建钉钉机器人
    2.获取webhook URL
    3.添加到GitHub Secrets：DINGTALK_WEBHOOK

运行报告上传脚本
./generate_report.sh




功能特性
-请求封装（支持各种HTTP方法）
-数据驱动（JSON/YAML/CSV）
-断言工具类
-Allure报告集成
-覆盖率统计
-CI/CD配置

作者
Cg12-one
1610941369@qq.com