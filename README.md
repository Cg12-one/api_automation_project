#API自动化测试框架

##项目结构
api_framework/
-common/    #公共租界
    -config.py  #配置
    -request.py #请求封装
    -base_test.py   #测试基类
    -assertions.py  #断言工具
    -data_loaderpy  #数据加载
-test_data  #测试数据
    -user_cases.json
    -order_cases.yaml
-tests/ #测试用例
    -test_user_api.py
    -test_order_api.py
    -ecommerce/ #业务模块测试
-reports/   #测试报告
-requirements.txt   #依赖
-pytest.ini #pytest配置
-README.md  #本文档



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