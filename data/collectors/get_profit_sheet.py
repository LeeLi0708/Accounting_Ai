import requests
from datetime import datetime, timedelta

# 全局变量存储解析后的数据
financial_profit_sheet_data_by_period = {}

def parse_financial_profit_data(response_data):
    """
    解析财务数据并按报告期存储到全局变量
    """
    global financial_profit_sheet_data_by_period

    if not response_data.get('success'):
        print("API请求失败:", response_data.get('message'))
        return

    data_list = response_data.get('result', {}).get('data', [])

    for item in data_list:
        # 提取报告日期并格式化为YYYY-MM-DD
        report_date = item.get('REPORT_DATE', '').split(' ')[0]

        # 按报告期存储数据
        financial_profit_sheet_data_by_period[report_date] = {
            '基本信息': {
                '股票代码': item.get('SECUCODE'),
                '股票名称': item.get('SECURITY_NAME_ABBR'),
                '报告类型': item.get('REPORT_TYPE'),
                '货币单位': item.get('CURRENCY'),
                '公告日期': item.get('NOTICE_DATE', '').split(' ')[0]
            },
            '利润表': {
                '营业总收入': item.get('TOTAL_OPERATE_INCOME', 0) or 0,
                '营业收入': item.get('OPERATE_INCOME', 0) or 0,
                '利息收入': item.get('INTEREST_INCOME', 0) or 0,
                '已赚保费': item.get('EARNED_PREMIUM', 0) or 0,
                '手续费及佣金收入': item.get('FEE_COMMISSION_INCOME', 0) or 0,
                '其他业务收入': item.get('OTHER_BUSINESS_INCOME', 0) or 0,
                '营业总收入其他项目': item.get('TOI_OTHER', 0) or 0,
                '营业总成本': item.get('TOTAL_OPERATE_COST', 0) or 0,
                '营业成本': item.get('OPERATE_COST', 0) or 0,
                '利息支出': item.get('INTEREST_EXPENSE', 0) or 0,
                '手续费及佣金支出': item.get('FEE_COMMISSION_EXPENSE', 0) or 0,
                '研发费用': item.get('RESEARCH_EXPENSE', 0) or 0,
                '退保金': item.get('SURRENDER_VALUE', 0) or 0,
                '赔付支出净额': item.get('NET_COMPENSATE_EXPENSE', 0) or 0,
                '提取保险合同准备金净额': item.get('NET_CONTRACT_RESERVE', 0) or 0,
                '保单红利支出': item.get('POLICY_BONUS_EXPENSE', 0) or 0,
                '分保费用': item.get('REINSURE_EXPENSE', 0) or 0,
                '其他业务成本': item.get('OTHER_BUSINESS_COST', 0) or 0,
                '营业税金及附加': item.get('OPERATE_TAX_ADD', 0) or 0,
                '销售费用': item.get('SALE_EXPENSE', 0) or 0,
                '管理费用': item.get('MANAGE_EXPENSE', 0) or 0,
                '财务费用': item.get('FINANCE_EXPENSE', 0) or 0,
                '利息费用': item.get('FE_INTEREST_EXPENSE', 0) or 0,
                '利息收入(财务费用)': item.get('FE_INTEREST_INCOME', 0) or 0,  # 重命名避免重复
                '资产减值损失': item.get('ASSET_IMPAIRMENT_LOSS', 0) or 0,
                '信用减值损失': item.get('CREDIT_IMPAIRMENT_LOSS', 0) or 0,
                '营业总成本其他项目': item.get('TOC_OTHER', 0) or 0,
                '公允价值变动收益': item.get('FAIRVALUE_CHANGE_INCOME', 0) or 0,
                '投资收益': item.get('INVEST_INCOME', 0) or 0,
                '对联营企业和合营企业的投资收益': item.get('INVEST_JOINT_INCOME', 0) or 0,
                '净敞口套期收益': item.get('NET_EXPOSURE_INCOME', 0) or 0,
                '汇兑收益': item.get('EXCHANGE_INCOME', 0) or 0,
                '资产处置收益': item.get('ASSET_DISPOSAL_INCOME', 0) or 0,
                '其他收益': item.get('OTHER_INCOME', 0) or 0,
                '营业利润其他项目': item.get('OPERATE_PROFIT_OTHER', 0) or 0,
                '营业利润平衡项目': item.get('OPERATE_PROFIT_BALANCE', 0) or 0,
                '营业利润': item.get('OPERATE_PROFIT', 0) or 0,
                '营业外收入': item.get('NONBUSINESS_INCOME', 0) or 0,
                '非流动资产处置利得': item.get('NONCURRENT_DISPOSAL_INCOME', 0) or 0,
                '营业外支出': item.get('NONBUSINESS_EXPENSE', 0) or 0,
                '非流动资产处置净损失': item.get('NONCURRENT_DISPOSAL_LOSS', 0) or 0,
                '影响利润总额的其他项目': item.get('EFFECT_TP_OTHER', 0) or 0,
                '利润总额平衡项目': item.get('TOTAL_PROFIT_BALANCE', 0) or 0,
                '利润总额': item.get('TOTAL_PROFIT', 0) or 0,
                '所得税': item.get('INCOME_TAX', 0) or 0,
                '影响净利润的其他项目': item.get('EFFECT_NETPROFIT_OTHER', 0) or 0,
                '未确认投资损失': item.get('UNCONFIRM_INVEST_LOSS', 0) or 0,
                '净利润': item.get('NETPROFIT', 0) or 0,
                '被合并方在合并前实现利润': item.get('PRECOMBINE_PROFIT', 0) or 0,
                '持续经营净利润': item.get('CONTINUED_NETPROFIT', 0) or 0,
                '终止经营净利润': item.get('DISCONTINUED_NETPROFIT', 0) or 0,
                '归属于母公司股东的净利润': item.get('PARENT_NETPROFIT', 0) or 0,
                '少数股东损益': item.get('MINORITY_INTEREST', 0) or 0,
                '扣除非经常性损益后的净利润': item.get('DEDUCT_PARENT_NETPROFIT', 0) or 0,
                '净利润其他项目': item.get('NETPROFIT_OTHER', 0) or 0,
                '基本每股收益': item.get('BASIC_EPS', 0) or 0,
                '稀释每股收益': item.get('DILUTED_EPS', 0) or 0,
                '其他综合收益': item.get('OTHER_COMPRE_INCOME', 0) or 0,
                '归属于母公司股东的其他综合收益': item.get('PARENT_OCI', 0) or 0,
                '归属于少数股东的其他综合收益': item.get('MINORITY_OCI', 0) or 0,
                '综合收益总额': item.get('TOTAL_COMPRE_INCOME', 0) or 0,
                '归属于母公司股东的综合收益总额': item.get('PARENT_TCI', 0) or 0,
                '归属于少数股东的综合收益总额': item.get('MINORITY_TCI', 0) or 0
            }
        }

def print_financial_data():
    """
    打印存储的财务数据
    """
    global financial_balance_sheet_data_by_period

    if not financial_profit_sheet_data_by_period:
        print("没有可用的财务数据")
        return

    # 按报告日期排序
    sorted_dates = sorted(financial_profit_sheet_data_by_period.keys(), reverse=True)

    for date in sorted_dates:
        print(f"\n=== {date} {financial_profit_sheet_data_by_period[date]['基本信息']['报告类型']} ===")
        print(f"股票: {financial_profit_sheet_data_by_period[date]['基本信息']['股票名称']}({financial_profit_sheet_data_by_period[date]['基本信息']['股票代码']})")
        print(f"公告日期: {financial_profit_sheet_data_by_period[date]['基本信息']['公告日期']}")

        # 显示关键财务指标
        print("\n关键财务指标:")
        print(f"营业收入: {financial_profit_sheet_data_by_period[date]['利润表']['营业收入']:,.2f}")
        print(f"营业利润: {financial_profit_sheet_data_by_period[date]['利润表']['营业利润']:,.2f}")
        print(f"净利润: {financial_profit_sheet_data_by_period[date]['利润表']['净利润']:,.2f}")
        print(f"归属于母公司股东的净利润: {financial_profit_sheet_data_by_period[date]['利润表']['归属于母公司股东的净利润']:,.2f}")



def find_closest_report_date(target_date_str):
    """找到目标日期之前最近的财务报告期（通常是季度末）"""
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")

    # 财务报告期通常是 3-31, 6-30, 9-30, 12-31
    # 计算最近的报告期
    year = target_date.year
    month = target_date.month

    if month >= 10:
        closest_report_date = datetime(year, 12, 31)
    elif month >= 7:
        closest_report_date = datetime(year, 9, 30)
    elif month >= 4:
        closest_report_date = datetime(year, 6, 30)
    else:
        closest_report_date = datetime(year - 1, 12, 31)

    # 如果目标日期比计算出的报告期还早，则再往前推一个季度
    if target_date < closest_report_date:
        if closest_report_date.month == 3:
            closest_report_date = datetime(year - 1, 12, 31)
        elif closest_report_date.month == 6:
            closest_report_date = datetime(year, 3, 31)
        elif closest_report_date.month == 9:
            closest_report_date = datetime(year, 6, 30)
        else:  # 12月
            closest_report_date = datetime(year, 9, 30)

    return closest_report_date.strftime("%Y-%m-%d")

def get_previous_report_dates(report_date_str, count=4):
    """获取前 count 个报告期（默认前4个季度）"""
    report_date = datetime.strptime(report_date_str, "%Y-%m-%d")
    report_dates = [report_date.strftime("%Y-%m-%d")]

    for _ in range(count):
        year = report_date.year
        month = report_date.month

        if month == 3:  # 前一个季度是去年12月
            report_date = datetime(year - 1, 12, 31)
        elif month == 6:  # 前一个季度是今年3月
            report_date = datetime(year, 3, 31)
        elif month == 9:  # 前一个季度是今年6月
            report_date = datetime(year, 6, 30)
        else:  # 12月，前一个季度是今年9月
            report_date = datetime(year, 9, 30)

        report_dates.append(report_date.strftime("%Y-%m-%d"))

    return sorted(report_dates)  # 按时间顺序排序

def get_financial_Profit_data(stock_code, target_date_str):
    """获取财务数据"""
    # 找到最近的报告期
    closest_report_date = find_closest_report_date(target_date_str)

    # 获取前4个报告期
    report_dates = get_previous_report_dates(closest_report_date, 4)

    # 构建API请求URL
    url = (
        "https://datacenter.eastmoney.com/securities/api/data/get?"
        "type=RPT_F10_FINANCE_GINCOMEQC&"
        "sty=PC_F10_GINCOMEQC&"
        f"filter=(SECUCODE=\"{stock_code}\")"
        f"(REPORT_DATE in ('" + "','".join(report_dates) + "'))&"
        "p=1&ps=5&sr=-1&st=REPORT_DATE&"
        "source=HSF10&client=PC&v=0538802348949726"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


# 示例使用
if __name__ == "__main__":
    stock_code = "600519.SH"  # 股票代码
    target_date = "2024-05-01"  # 输入目标日期

    financial_data = get_financial_Profit_data(stock_code, target_date)

    parse_financial_profit_data(financial_data)
    print_financial_data()
    print(financial_balance_sheet_data_by_period)


    if financial_data:
        print("获取数据成功:")
        print(financial_data)
    else:
        print("获取数据失败")