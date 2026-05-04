import sys
import os

# 只配置一次，所有测试文件都能用
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# 现在所有测试文件都能导入 common