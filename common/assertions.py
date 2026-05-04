
import json
import re

class APIAssert:
    """API断言封装"""

    @staticmethod
    def assert_status_code(response,expected):
        """断言状态码"""
        assert response.status_code == expected,\
            f"状态码错误：{response.status_code} != {expected}"
        return True

    @staticmethod
    def assert_json_key(response,key,expected=None):
        """断言JSON包含指定2键"""
        data = response.json()
        assert key in data,f"响应缺少键：{key}"
        if expected is not None:
            assert data[key] == expected,\
                f"值不匹配:{data[key]} != {expected}"
        return True


    @staticmethod
    def assert_json_path(response,path,expected):
        """断言JSON路径值"""
        data = response.json()
        keys = path.split(".")
        
        for key in keys:
            if "[" in key:
                #处理数组索引：items[0]
                k,idx = key.split("[")
                idx = int(idx.rstrip("]"))
                data = data[k][idx]
            else:
                data = data[key]

        
        assert data == expected,f"路径值不匹配：{data} != {expected}"
        return True

        @staticmethod
        def assert_response_time(response,max_mx):
            """断言响应时间"""   # resp.elapsed：datetime.timedelta 对象
            assert response.elapsed.total_seconds() * 1000 < max_mx, \
                f"响应时间超限：{response.elapsed.total_seconds() * 1000:.of}ms >{max_mx}ms"
            return True

        @staticmethod
        def assert_schema(response,schema):
            """断言响应结构"""
            data = response.json()
            for key,value_type in schema.items():
                assert key in data,f"缺少字段：{key}"
                assert isinstance(data[key],value_type),\
                    f"类型错误：{key} 应为 {value_type.__name__}"
                return True
