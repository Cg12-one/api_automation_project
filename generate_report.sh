#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 切换到脚本所在目录
cd "$SCRIPT_DIR"

echo "===生成测试报告==="

#运行所有测试并生成报告
pytest tests/ \
   -v \
   -s \
   --html=reports/pytest_report.html \
   --self-contained-html \
   --cov=common \
   --cov=tests \
   --cov-report=html \
   --cov-report=xml \
   --alluredir=reports/allure-results

echo ""
echo "===报告生成完成==="
echo "Pytest HTML报告：reports/pytest_report.html"
echo "覆盖率报告：reports/htmlcov/index.html"
echo "Allure结果：reports/allure-results/"

#如果有allure-commandline,生成HTML
if command -v allure &> /dev/null; then
    allure generate reports/allure-results -o reports/allure-report --clean
    echo "Allure报告：reports/allure-report/index.html"
fi
