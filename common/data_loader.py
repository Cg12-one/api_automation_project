"""数据加载器"""
import json
import yaml
import csv
import os

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

