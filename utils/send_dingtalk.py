import argparse
import requests
import json
import os
from datetime import datetime

def send_notification(webhook,total,passed,failed,status):
    """发送钉钉通知"""

    if status == "failed":
        color = "red"
        title = "测试失败"
    else:
        color = "green"
        title = "测试通过"

     # 获取仓库信息
    repo = os.getenv("GITHUB_REPOSITORY", "Cg12-one/api_automation_project")
    
    # 计算通过率（添加除零保护）
    if total > 0:
        success_rate = passed/total*100
    else:
        success_rate = 0.0

    message = {
        "msgtype":"markdown",
        "markdown":{
            "title":title,
            "text":f"""##{title}

**项目**: API自动化测试
**执行时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**总计**：{total}
**通过**：{passed}
**失败**：{failed}
**通过率**：{passed/total*100:.1f}%

[查看详情](https://github.com/{repo}/actions)
"""
#repo是个占位符，实际位置更换为自己的地址，例如Cg12-one/api_automation_project
        }
    }


    response = requests.post(webhook,json=message)
    return response.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--webhook",required=False)  # 必需参数
    parser.add_argument("--total",type=int,required=True)
    parser.add_argument("--passed",type=int,required=True)
    parser.add_argument("--failed",type=int,required=True)
    parser.add_argument("--status",required=True)
    args = parser.parse_args()  # 解析

     # 优先使用命令行参数，否则从环境变量读取
    webhook = args.webhook or os.getenv("DINGTALK_WEBHOOK")

    print(f"使用 webhook: {webhook[:50]}...")  # 调试信息
    print(f"环境变量 DINGTALK_WEBHOOK: {os.getenv('DINGTALK_WEBHOOK', '未设置')[:50] if os.getenv('DINGTALK_WEBHOOK') else '未设置'}...")
    
    if not webhook:
        print("❌ 错误：请提供 --webhook 参数或设置 DINGTALK_WEBHOOK 环境变量")
        exit(1)
    
    result = send_notification(
        webhook,args.total,args.passed,args.failed,args.status
    )
    print(result)