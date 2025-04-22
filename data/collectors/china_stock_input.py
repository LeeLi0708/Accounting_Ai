import re
from datetime import datetime
from typing import Tuple, Optional

# 声明全局变量
global_ticker = ""
global_date_std = ""

class ChinaStockValidator:
    """中国沪深股市股票代码和日期验证器"""

    def __init__(self):
        # 定义各市场代码规则
        self.market_rules = {
            'SH': {  # 上海证券交易所
                'pattern': r'^6[0-9]{5}$',  # 沪市主板(600/601/603等)和科创板(688)
                'description': "沪市股票应以6开头(主板600+/科创板688)",
                'examples': ['600519', '601318', '688981']
            },
            'SZ': {  # 深圳证券交易所
                'pattern': r'^[03][0-9]{5}$',  # 深市主板(000-004)/中小板(003)/创业板(30)
                'description': "深市股票应以0(主板)或3(创业板)开头",
                'examples': ['000001', '002352', '300750']
            },
            'BJ': {  # 北京证券交易所(可选支持)
                'pattern': r'^8[0-9]{5}$',  # 北交所股票(8开头)
                'description': "北交所股票应以8开头",
                'examples': ['830799', '835185']
            }
        }

        # 交易日历(示例，实际应用中应该使用完整的交易日历)
        self.trading_days = {
            '2023-01-03', '2023-01-04', '2023-01-05',  # 示例日期
            '2023-04-27', '2023-04-28', '2023-05-04'  # 示例日期
        }

    def validate_ticker(self, raw_input: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """验证并标准化沪深股票代码

        参数:
            raw_input: 用户输入的股票代码(可带或不带后缀)

        返回:
            tuple: (是否有效, 标准化代码, 错误信息)
        """
        # 1. 输入清洗
        cleaned = raw_input.strip().upper()

        # 2. 空输入检查
        if not cleaned:
            return False, None, "输入不能为空"

        # 3. 分离代码和后缀
        if '.' in cleaned:
            parts = cleaned.split('.')
            if len(parts) > 2:
                return False, None, "股票代码格式不正确"
            code_part, suffix = parts[0], parts[1].upper()
        else:
            code_part, suffix = cleaned, None

        # 4. 基础代码格式验证
        if not code_part.isdigit():
            return False, None, "股票代码必须为纯数字"
        if len(code_part) != 6:
            return False, None, "股票代码必须为6位数字"

        # 5. 智能后缀补全
        if not suffix:
            # 根据代码开头自动判断市场
            if code_part.startswith('6'):
                suffix = 'SH'
            elif code_part.startswith(('0', '3')):
                suffix = 'SZ'
            elif code_part.startswith('8'):  # 北交所
                suffix = 'BJ'
            else:
                return False, None, "无法识别的股票代码开头"
        else:
            # 验证后缀是否合法
            if suffix not in self.market_rules:
                return False, None, f"不支持的市场后缀: {suffix}，请使用.SH(沪市)或.SZ(深市)"

        # 6. 验证代码规则
        market_rule = self.market_rules.get(suffix)
        if not market_rule:
            return False, None, f"未知市场类型: {suffix}"

        if not re.match(market_rule['pattern'], code_part):
            return False, None, market_rule['description']

        # 7. 返回标准化代码
        standardized = f"{code_part}.{suffix}"
        return True, standardized, None

    def validate_date(self, date_str: str, check_trading_day: bool = False) -> Tuple[bool, Optional[str], Optional[str]]:
        """验证日期格式是否正确

        参数:
            date_str: 日期字符串(YYYY-MM-DD格式)
            check_trading_day: 是否检查是否为交易日

        返回:
            tuple: (是否有效, 标准化日期, 错误信息)
        """
        try:
            # 1. 尝试解析日期
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.now().date()

            # 2. 检查是否为未来日期
            if date_obj > today:
                return False, None, "日期不能是未来日期"

            # 3. 检查历史日期(示例: 中国股市大约从1990年开始)
            if date_obj.year < 1990:
                return False, None, "日期过早，中国股市始于1990年"

            # 4. 检查是否为交易日(如果需要)
            if check_trading_day and date_str not in self.trading_days:
                return False, None, "该日期不是交易日"

            # 5. 返回标准化的日期字符串
            return True, date_str, None

        except ValueError:
            return False, None, "日期格式不正确，请使用YYYY-MM-DD格式"

def china_stock_import():
    """主交互程序"""
    global global_ticker, global_date_std  # 声明使用全局变量

    validator = ChinaStockValidator()

    print("""\n=== 中国沪深股市分析系统 ===
输入示例：
- 沪市股票：600519 或 600519.SH
- 深市股票：000001 或 300750.SZ
- 北交所股票：830799 或 830799.BJ
- 日期格式：2023-01-01\n""")

    while True:
        try:
            # 1. 获取股票代码输入
            user_input = input("\n请输入股票代码(输入q退出): ").strip()
            if user_input.lower() == 'q':
                print("退出系统")
                break

            # 2. 验证股票代码
            valid, ticker, error = validator.validate_ticker(user_input)
            if not valid:
                print(f"\n❌ 股票代码错误: {error}")
                print(f"示例: {', '.join(validator.market_rules['SH']['examples'])} (沪市)")
                print(f"      {', '.join(validator.market_rules['SZ']['examples'])} (深市)")
                continue

            # 3. 获取日期输入
            date_input = input("请输入日期(YYYY-MM-DD): ").strip()
            date_valid, date_std, date_error = validator.validate_date(date_input)

            if not date_valid:
                print(f"\n❌ 日期错误: {date_error}")
                print("请使用正确的日期格式，如: 2023-01-01")
                continue

            # 4. 所有验证通过
            print(f"\n✅ 验证通过 | 标准代码: {ticker} | 日期: {date_std}")
            print("启动分析流程...\n")

            # 更新全局变量
            global_ticker = ticker
            global_date_std = date_std

            return ticker, date_std

        except KeyboardInterrupt:
            print("\n操作已取消")
            break
        except Exception as e:
            print(f"\n系统错误: {str(e)}")
            break

# if __name__ == "__main__":
#     # 调用函数并获取返回值
#     ticker, date_std = china_stock_import()
#
#     # 也可以通过全局变量访问
#     print(f"\n通过全局变量获取的值:")
#     print(f"股票代码: {global_ticker}")
#     print(f"日期: {global_date_std}")
#
#     # 这里可以使用返回的ticker和date_std或全局变量进行后续处理