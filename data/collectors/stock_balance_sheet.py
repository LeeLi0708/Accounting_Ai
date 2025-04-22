import requests
import pandas as pd
import re
from threading import Lock
from typing import Dict, Optional

# 全局存储结构
class FinancialDataStore:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._balance_sheets: Dict[str, Dict[str, pd.DataFrame]] = {}
                cls._instance._cache_lock = Lock()
            return cls._instance

    def update_balance_sheet(self, stock_code: str, date: str, data: pd.DataFrame):
        """线程安全的数据更新"""
        with self._cache_lock:
            if stock_code not in self._balance_sheets:
                self._balance_sheets[stock_code] = {}
            self._balance_sheets[stock_code][date] = data.copy()

    def get_balance_sheet(self, stock_code: str, date: str) -> Optional[pd.DataFrame]:
        """安全获取数据副本"""
        with self._cache_lock:
            try:
                return self._balance_sheets[stock_code][date].copy()
            except KeyError:
                return None

    def clear_cache(self, max_items=1000):
        """缓存清理机制"""
        with self._cache_lock:
            total = sum(len(v) for v in self._balance_sheets.values())
            if total > max_items:
                self._balance_sheets.clear()

# 单例初始化
global_store = FinancialDataStore()

def get_balance_sheet(stock_code: str, date: str = "20240331") -> pd.DataFrame:


    """
    增强版数据获取函数，自动缓存到全局存储
    """
    try:
        # 优先检查缓存
        cached_data = global_store.get_balance_sheet(stock_code, date)
        if cached_data is not None:
            return cached_data

        # 使用 requests 获取数据
        params = {'date': date}
        response = requests.get(
            url='http://127.0.0.1:8080/api/public/stock_zcfz_em',  # 替换为实际地址
            params=params
        )

        # 检查响应状态
        response.raise_for_status()

        # 解析 JSON 数据并转换为 DataFrame
        data = response.json()
        print(data)
        df = pd.DataFrame(data)

        # 检查股票代码格式并过滤数据
        code_match = re.search(r"\d{6}", stock_code)
        if not code_match:
            raise ValueError("股票代码必须包含6位连续数字")

        clean_code = code_match.group()
        df["股票代码"] = df["股票代码"].astype(str)
        result_df = df[df["股票代码"] == clean_code]

        if result_df.empty:
            raise ValueError(f"未找到股票代码 {clean_code} 的资产负债表数据")

        # 更新全局存储
        global_store.update_balance_sheet(clean_code, date, result_df)

        return result_df.copy()

    except Exception as e:
        print(f"数据获取失败：{str(e)}")
        return pd.DataFrame()

# 使用示例
if __name__ == "__main__":
    # 首次查询并存储
    df1 = get_balance_sheet("600519.SS", "20240331")

    # 从全局存储获取
    cached_df = global_store.get_balance_sheet("600519", "20240331")

    # 打印存储结构
    print("当前存储的股票代码:", list(global_store._balance_sheets.keys()))
    print("600519的报表日期:", list(global_store._balance_sheets["600519"].keys()))
