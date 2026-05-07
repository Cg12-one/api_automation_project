"""数据加载器"""
import json
import yaml
import csv
import os
from pathlib import Path

class DataLoader:
    """数据加载器"""

    @staticmethod
    def load_json(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def load_yaml(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            return yaml.safe_load(f)    ##安全加载 YAML（防止恶意代码）

    @staticmethod
    def load_csv(filepath):
        cases = []
        with open(filepath,'r',encoding='uft-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cases.append(dict(row))
            return cases

    @staticmethod
    def get_test_data(case_name,data_file='login_cases.yaml'):
        """获取特定测试用例数据"""
        base_dir = Path(__file__).parent.parent / 'test_data' / 'api_cases'
        filepath = base_dir / data_file
        data = DataLoader.load_yaml(filepath)
        return data.get(case_name)