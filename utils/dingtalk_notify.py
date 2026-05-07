import requests
import json
from datetime import datetime
import os

class DingTalkNotifier:
    """钉钉通知器"""
    
    def __init__(self, webhook_url):    #：构造函数，初始化时传入 webhook URL
        self.webhook_url = webhook_url
    
    def send_test_result(self, test_result):
        """发送测试结果通知"""
        
        # 根据测试结果设置颜色
        if test_result["failed"] > 0:
            color = "#FF0000"  # 红色 - 失败
            emoji = "❌"
            title = "测试失败告警"
        elif test_result["skipped"] > 0:
            color = "#FFA500"  # 橙色 - 有跳过
            emoji = "⚠️"
            title = "测试完成（有跳过）"
        else:
            color = "#00AA00"  # 绿色 - 通过
            emoji = "✅"
            title = "测试通过"
        
        # 构建消息
        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"""## {emoji} {title}

**项目**: API自动化测试
**执行时间**: {test_result["execute_time"]}
**执行环境**: {test_result["environment"]}

### 📊 测试结果
| 指标 | 数量 |
|------|------|
| 总计 | {test_result["total"]} |
| 通过 | {test_result["passed"]} |
| 失败 | {test_result["failed"]} |
| 跳过 | {test_result["skipped"]} |
| 耗时 | {test_result["duration"]} |

### 🔴 失败用例
{self._format_failed_cases(test_result["failed_cases"])}

### 📎 报告链接
- [Allure报告]({test_result["allure_report_url"]})
- [HTML报告]({test_result["html_report_url"]})

---
*此消息由CI/CD自动发送*
"""
            },
            "at": {
                "isAtAll": True  # @所有人
            }
        }
        
        # 发送请求
        response = requests.post(
            self.webhook_url,
            json=message,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    def _format_failed_cases(self, failed_cases):
        """格式化失败用例列表"""
        if not failed_cases:
            return "无"
        
        result = ""
        for case in failed_cases[:5]:  # 最多显示5个
            result += f"- `{case}`\n"   #反引号 `：Markdown 代码格式
        
        if len(failed_cases) > 5:
            result += f"- ... 还有{len(failed_cases)-5}个失败用例"
        
        return result


# 使用示例
if __name__ == "__main__":
     # 从环境变量读取 webhook
    webhook = os.getenv("DINGTALK_WEBHOOK")
    
    if not webhook:
        print("❌ 错误：请设置 DINGTALK_WEBHOOK 环境变量")
        print("用法：export DINGTALK_WEBHOOK='https://...'")
        exit(1)
    
    notifier = DingTalkNotifier(webhook)
    
    
    # 模拟测试结果
    test_result = {
        "execute_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),   #datetime.now().strftime()格式化当前时间
        "environment": "GitHub Actions / Ubuntu",
        "total": 20,
        "passed": 18,
        "failed": 2,
        "skipped": 0,
        "duration": "45.6s",
        "failed_cases": [
            "test_login_fail[wrong_password]",
            "test_create_user"
        ],
        "allure_report_url": "https://your-allure-server/report",
        "html_report_url": "https://your-server/report.html"
    }
    
    result = notifier.send_test_result(test_result)
    print(result)
