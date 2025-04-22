import sys
from data.collectors.china_stock_input import china_stock_import
from data.collectors.get_balance_sheet import parse_financial_balance_data, print_financial_data, get_financial_balance_data
from datetime import datetime
from data.collectors.get_profit_sheet import get_financial_Profit_data, parse_financial_profit_data

# 全局变量，用于存储按期间分类的财务数据
financial_balance_sheet_data_by_period = {}
financial_profit_sheet_data_by_period = {}

def main():
    # 1. 获取用户输入的股票代码和日期
    ticker, date_std = china_stock_import()

    # 2. 获取该股票在指定日期的财务数据
    financial_BS_data = get_financial_balance_data(ticker, date_std)
    financial_PS_data = get_financial_Profit_data(ticker, date_std)

    # 3. 解析财务数据并存储到全局变量中
    parse_financial_balance_data(financial_BS_data)
    parse_financial_profit_data(financial_PS_data)

    # 4. 打印财务数据
    print_financial_data()

if __name__ == "__main__":
    main()