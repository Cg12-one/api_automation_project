from dingtalk_notify import DingTalkNotifier
from datetime import datetime

# 替换成你的 webhook
WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=9a31720b5e0c915ec85b07fa0875f8c53acbdc9c105cd6f848b8892e3f08a08f"

notifier = DingTalkNotifier(WEBHOOK)

test_result = {
    "execute_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "environment": "测试环境",
    "total": 5,
    "passed": 5,
    "failed": 0,
    "skipped": 0,
    "duration": "3.2s",
    "failed_cases": [],
    "allure_report_url": "http://example.com",
    "html_report_url": "http://example.com/report.html"
}

result = notifier.send_test_result(test_result)
print(f"发送结果：{result}")