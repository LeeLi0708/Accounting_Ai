import requests
from datetime import datetime, timedelta

# 全局变量存储解析后的数据
financial_balance_sheet_data_by_period = {}

def parse_financial_balance_data(response_data):
    """
    解析财务数据并按报告期存储到全局变量
    """
    global financial_balance_sheet_data_by_period

    if not response_data.get('success'):
        print("API请求失败:", response_data.get('message'))
        return

    data_list = response_data.get('result', {}).get('data', [])

    for item in data_list:
        # 提取报告日期并格式化为YYYY-MM-DD
        report_date = item.get('REPORT_DATE', '').split(' ')[0]

        # 按报告期存储数据
        financial_balance_sheet_data_by_period[report_date] = {
            '基本信息': {
                '股票代码': item.get('SECUCODE'),
                '股票名称': item.get('SECURITY_NAME_ABBR'),
                '报告类型': item.get('REPORT_TYPE'),
                '货币单位': item.get('CURRENCY'),
                '公告日期': item.get('NOTICE_DATE', '').split(' ')[0]
            },
            '资产负债表': {
                '流动资产合计(元)': item.get('TOTAL_CURRENT_ASSETS', 0) or 0,
                '非流动资产合计(元)': item.get('TOTAL_NONCURRENT_ASSETS', 0) or 0,
                '总资产(元)': item.get('TOTAL_ASSETS', 0) or 0,
                '流动负债合计(元)': item.get('TOTAL_CURRENT_LIAB', 0) or 0,
                '非流动负债合计(元)': item.get('TOTAL_NONCURRENT_LIAB', 0) or 0,
                '总负债(元)': item.get('TOTAL_LIABILITIES', 0) or 0,
                '股东权益合计(元)': item.get('TOTAL_EQUITY', 0) or 0
            },
            '资产': {
                '货币资金': item.get('MONETARYFUNDS', 0) or 0,
                '结算备付金': item.get('SETTLE_EXCESS_RESERVE', 0) or 0,
                '拆出资金': item.get('LEND_FUND', 0) or 0,
                '交易性金融资产': item.get('TRADE_FINASSET_NOTFVTPL', 0) or 0,
                '融出资金': item.get('FIN_FUND', 0) or 0,
                '以公允价值计量且其变动计入当期损益的金融资产': item.get('FVTPL_FINASSET', 0) or 0,
                '指定以公允价值计量且其变动计入当期损益的金融资产': item.get('APPOINT_FVTPL_FINASSET', 0) or 0,
                '衍生金融资产': item.get('DERIVE_FINASSET', 0) or 0,
                '应收票据及应收账款': item.get('NOTE_ACCOUNTS_RECE', 0) or 0,
                '应收票据': item.get('NOTE_RECE', 0) or 0,
                '应收账款': item.get('ACCOUNTS_RECE', 0) or 0,
                '应收款项融资': item.get('FINANCE_RECE', 0) or 0,
                '预付款项': item.get('PREPAYMENT', 0) or 0,
                '应收保费': item.get('PREMIUM_RECE', 0) or 0,
                '应收分保账款': item.get('REINSURE_RECE', 0) or 0,
                '应收分保合同准备金': item.get('RC_RESERVE_RECE', 0) or 0,
                '其他应收款合计': item.get('TOTAL_OTHER_RECE', 0) or 0,
                '应收利息': item.get('INTEREST_RECE', 0) or 0,
                '应收股利': item.get('DIVIDEND_RECE', 0) or 0,
                '其他应收款': item.get('OTHER_RECE', 0) or 0,
                '应收出口退税': item.get('EXPORT_REFUND_RECE', 0) or 0,
                '应收补贴款': item.get('SUBSIDY_RECE', 0) or 0,
                '内部应收款': item.get('INTERNAL_RECE', 0) or 0,
                '买入返售金融资产': item.get('BUY_RESALE_FINASSET', 0) or 0,
                '以摊余成本计量的金融资产': item.get('AMORTIZE_COST_FINASSET', 0) or 0,
                '以公允价值计量且其变动计入其他综合收益的金融资产': item.get('FVTOCI_FINASSET', 0) or 0,
                '存货': item.get('INVENTORY', 0) or 0,
                '合同资产': item.get('CONTRACT_ASSET', 0) or 0,
                '持有待售资产': item.get('HOLDSALE_ASSET', 0) or 0,
                '一年内到期的非流动资产': item.get('NONCURRENT_ASSET_1YEAR', 0) or 0,
                '其他流动资产': item.get('OTHER_CURRENT_ASSET', 0) or 0,
                '流动资产其他项目': item.get('CURRENT_ASSET_OTHER', 0) or 0,
                '流动资产合计': item.get('TOTAL_CURRENT_ASSETS', 0) or 0,
                '发放贷款及垫款': item.get('LOAN_ADVANCE', 0) or 0,
                '债权投资': item.get('CREDITOR_INVEST', 0) or 0,
                '以摊余成本计量的金融资产（非流动）': item.get('AMORTIZE_COST_NCFINASSET', 0) or 0,
                '其他债权投资': item.get('OTHER_CREDITOR_INVEST', 0) or 0,
                '以公允价值计量且其变动计入其他综合收益的金融资产（非流动）': item.get('FVTOCI_NCFINASSET', 0) or 0,
                '可供出售金融资产': item.get('AVAILABLE_SALE_FINASSET', 0) or 0,
                '持有至到期投资': item.get('HOLD_MATURITY_INVEST', 0) or 0,
                '长期应收款': item.get('LONG_RECE', 0) or 0,
                '长期股权投资': item.get('LONG_EQUITY_INVEST', 0) or 0,
                '其他权益工具投资': item.get('OTHER_EQUITY_INVEST', 0) or 0,
                '其他非流动金融资产': item.get('OTHER_NONCURRENT_FINASSET', 0) or 0,
                '投资性房地产': item.get('INVEST_REALESTATE', 0) or 0,
                '固定资产': item.get('FIXED_ASSET', 0) or 0,
                '在建工程': item.get('CIP', 0) or 0,
                '使用权资产': item.get('USERIGHT_ASSET', 0) or 0,
                '工程物资': item.get('PROJECT_MATERIAL', 0) or 0,
                '固定资产清理': item.get('FIXED_ASSET_DISPOSAL', 0) or 0,
                '生产性生物资产': item.get('PRODUCTIVE_BIOLOGY_ASSET', 0) or 0,
                '油气资产': item.get('OIL_GAS_ASSET', 0) or 0,
                '无形资产': item.get('INTANGIBLE_ASSET', 0) or 0,
                '开发支出': item.get('DEVELOP_EXPENSE', 0) or 0,
                '商誉': item.get('GOODWILL', 0) or 0,
                '长期待摊费用': item.get('LONG_PREPAID_EXPENSE', 0) or 0,
                '递延所得税资产': item.get('DEFER_TAX_ASSET', 0) or 0,
                '其他非流动资产': item.get('OTHER_NONCURRENT_ASSET', 0) or 0,
                '非流动资产其他项目': item.get('NONCURRENT_ASSET_OTHER', 0) or 0,
                '非流动资产平衡项目': item.get('NONCURRENT_ASSET_BALANCE', 0) or 0,
                '非流动资产合计': item.get('TOTAL_NONCURRENT_ASSETS', 0) or 0,
                '资产其他项目': item.get('ASSET_OTHER', 0) or 0,
                '资产总计': item.get('TOTAL_ASSETS', 0) or 0
            },
            '负债': {
                '短期借款': item.get('SHORT_LOAN', 0) or 0,
                '向中央银行借款': item.get('LOAN_PBC', 0) or 0,
                '吸收存款及同业存放': item.get('ACCEPT_DEPOSIT_INTERBANK', 0) or 0,
                '拆入资金': item.get('BORROW_FUND', 0) or 0,
                '交易性金融负债': item.get('TRADE_FINLIAB_NOTFVTPL', 0) or 0,
                '以公允价值计量且其变动计入当期损益的金融负债': item.get('FVTPL_FINLIAB', 0) or 0,
                '指定以公允价值计量且其变动计入当期损益的金融负债': item.get('APPOINT_FVTPL_FINLIAB', 0) or 0,
                '衍生金融负债': item.get('DERIVE_FINLIAB', 0) or 0,
                '应付票据及应付账款': item.get('NOTE_ACCOUNTS_PAYABLE', 0) or 0,
                '应付票据': item.get('NOTE_PAYABLE', 0) or 0,
                '应付账款': item.get('ACCOUNTS_PAYABLE', 0) or 0,
                '预收款项': item.get('ADVANCE_RECEIVABLES', 0) or 0,
                '合同负债': item.get('CONTRACT_LIAB', 0) or 0,
                '卖出回购金融资产款': item.get('SELL_REPO_FINASSET', 0) or 0,
                '应付手续费及佣金': item.get('FEE_COMMISSION_PAYABLE', 0) or 0,
                '应付职工薪酬': item.get('STAFF_SALARY_PAYABLE', 0) or 0,
                '应交税费': item.get('TAX_PAYABLE', 0) or 0,
                '其他应付款合计': item.get('TOTAL_OTHER_PAYABLE', 0) or 0,
                '应付利息': item.get('INTEREST_PAYABLE', 0) or 0,
                '应付股利': item.get('DIVIDEND_PAYABLE', 0) or 0,
                '其他应付款': item.get('OTHER_PAYABLE', 0) or 0,
                '应付分保账款': item.get('REINSURE_PAYABLE', 0) or 0,
                '内部应付款': item.get('INTERNAL_PAYABLE', 0) or 0,
                '预计流动负债': item.get('PREDICT_CURRENT_LIAB', 0) or 0,
                '保险合同准备金': item.get('INSURANCE_CONTRACT_RESERVE', 0) or 0,
                '代理买卖证券款': item.get('AGENT_TRADE_SECURITY', 0) or 0,
                '代理承销证券款': item.get('AGENT_UNDERWRITE_SECURITY', 0) or 0,
                '以摊余成本计量的金融负债': item.get('AMORTIZE_COST_FINLIAB', 0) or 0,
                '应付短期债券': item.get('SHORT_BOND_PAYABLE', 0) or 0,
                '持有待售负债': item.get('HOLDSALE_LIAB', 0) or 0,
                '一年内到期的非流动负债': item.get('NONCURRENT_LIAB_1YEAR', 0) or 0,
                '其他流动负债': item.get('OTHER_CURRENT_LIAB', 0) or 0,
                '流动负债其他项目': item.get('CURRENT_LIAB_OTHER', 0) or 0,
                '流动负债平衡项目': item.get('CURRENT_LIAB_BALANCE', 0) or 0,
                '流动负债合计': item.get('TOTAL_CURRENT_LIAB', 0) or 0,
                '长期借款': item.get('LONG_LOAN', 0) or 0,
                '以摊余成本计量的金融负债（非流动）': item.get('AMORTIZE_COST_NCFINLIAB', 0) or 0,
                '应付债券': item.get('BOND_PAYABLE', 0) or 0,
                '永续债': item.get('PERPETUAL_BOND_PAYBALE', 0) or 0,
                '租赁负债': item.get('LEASE_LIAB', 0) or 0,
                '长期应付款': item.get('LONG_PAYABLE', 0) or 0,
                '长期应付职工薪酬': item.get('LONG_STAFFSALARY_PAYABLE', 0) or 0,
                '专项应付款': item.get('SPECIAL_PAYABLE', 0) or 0,
                '预计负债': item.get('PREDICT_LIAB', 0) or 0,
                '递延收益': item.get('DEFER_INCOME', 0) or 0,
                '递延所得税负债': item.get('DEFER_TAX_LIAB', 0) or 0,
                '其他非流动负债': item.get('OTHER_NONCURRENT_LIAB', 0) or 0,
                '非流动负债其他项目': item.get('NONCURRENT_LIAB_OTHER', 0) or 0,
                '非流动负债平衡项目': item.get('NONCURRENT_LIAB_BALANCE', 0) or 0,
                '非流动负债合计': item.get('TOTAL_NONCURRENT_LIAB', 0) or 0,
                '负债其他项目': item.get('LIAB_OTHER', 0) or 0,
                '负债平衡项目': item.get('LIAB_BALANCE', 0) or 0,
                '负债合计': item.get('TOTAL_LIABILITIES', 0) or 0
            },
            '股东权益': {
                '实收资本（或股本）': item.get('SHARE_CAPITAL', 0) or 0,
                '其他权益工具': (item.get('OTHER_EQUITY_TOOL', 0) or 0) + (item.get('OTHER_EQUITY_OTHER', 0) or 0),
                '优先股': item.get('PREFERRED_SHARES', 0) or 0,
                '永续债': item.get('PERPETUAL_BOND', 0) or 0,
                '资本公积': item.get('CAPITAL_RESERVE', 0) or 0,
                '减:库存股': item.get('TREASURY_SHARES', 0) or 0,
                '其他综合收益': item.get('OTHER_COMPRE_INCOME', 0) or 0,
                '专项储备': item.get('SPECIAL_RESERVE', 0) or 0,
                '盈余公积': item.get('SURPLUS_RESERVE', 0) or 0,
                '一般风险准备': item.get('GENERAL_RISK_RESERVE', 0) or 0,
                '未确定的投资损失': item.get('UNCONFIRM_INVEST_LOSS', 0) or 0,
                '未分配利润': item.get('UNASSIGN_RPOFIT', 0) or 0,
                '拟分配现金股利': item.get('ASSIGN_CASH_DIVIDEND', 0) or 0,
                '外币报表折算差额': item.get('CONVERT_DIFF', 0) or 0,
                '归属于母公司股东权益其他项目': item.get('PARENT_EQUITY_OTHER', 0) or 0,
                '归属于母公司股东权益平衡项目': item.get('PARENT_EQUITY_BALANCE', 0) or 0,
                '归属于母公司股东权益总计': item.get('TOTAL_PARENT_EQUITY', 0) or 0,
                '少数股东权益': item.get('MINORITY_EQUITY', 0) or 0,
                '股东权益其他项目': item.get('EQUITY_OTHER', 0) or 0,
                '股东权益平衡项目': item.get('EQUITY_BALANCE', 0) or 0,
                '股东权益合计': item.get('TOTAL_EQUITY', 0) or 0,
                '负债和股东权益其他项目': item.get('LIAB_EQUITY_OTHER', 0) or 0,
                '负债及股东权益平衡项目': item.get('LIAB_EQUITY_BALANCE', 0) or 0,
                '负债和股东权益总计': item.get('TOTAL_LIAB_EQUITY', 0) or 0
            },
            '关键科目': {
                '货币资金(元)': item.get('MONETARYFUNDS', 0) or 0,
                '应收账款(元)': item.get('ACCOUNTS_RECE', 0) or 0,
                '存货(元)': item.get('INVENTORY', 0) or 0,
                '固定资产(元)': item.get('FIXED_ASSET', 0) or 0,
                '无形资产(元)': item.get('INTANGIBLE_ASSET', 0) or 0,
                '应付账款(元)': item.get('ACCOUNTS_PAYABLE', 0) or 0,
                '合同负债(元)': item.get('CONTRACT_LIAB', 0) or 0,
                '应交税费(元)': item.get('TAX_PAYABLE', 0) or 0
            },
            '同比增长': {
                '总资产增长率(%)': item.get('TOTAL_ASSETS_YOY', 0) or 0,
                '股东权益增长率(%)': item.get('TOTAL_EQUITY_YOY', 0) or 0,
                '存货增长率(%)': item.get('INVENTORY_YOY', 0) or 0,
                '合同负债增长率(%)': item.get('CONTRACT_LIAB_YOY', 0) or 0
            }
        }

def print_financial_data():
    """
    打印存储的财务数据
    """
    global financial_balance_sheet_data_by_period

    if not financial_balance_sheet_data_by_period:
        print("没有可用的财务数据")
        return

    # 按报告日期排序
    sorted_dates = sorted(financial_balance_sheet_data_by_period.keys(), reverse=True)

    for date in sorted_dates:
        print(f"\n=== {date} {financial_balance_sheet_data_by_period[date]['基本信息']['报告类型']} ===")
        print(f"股票: {financial_balance_sheet_data_by_period[date]['基本信息']['股票名称']}({financial_balance_sheet_data_by_period[date]['基本信息']['股票代码']})")
        print(f"公告日期: {financial_balance_sheet_data_by_period[date]['基本信息']['公告日期']}")

        print("\n【资产负债表】")
        print(f"总资产: {financial_balance_sheet_data_by_period[date]['资产负债表']['总资产(元)']:,.2f}")
        print(f"总负债: {financial_balance_sheet_data_by_period[date]['资产负债表']['总负债(元)']:,.2f}")
        print(f"股东权益: {financial_balance_sheet_data_by_period[date]['资产负债表']['股东权益合计(元)']:,.2f}")
        print(f"资产负债率: {financial_balance_sheet_data_by_period[date]['资产负债表']['总负债(元)'] / financial_balance_sheet_data_by_period[date]['资产负债表']['总资产(元)']:.2%}")

        print("\n【关键科目】")
        print(f"货币资金: {financial_balance_sheet_data_by_period[date]['关键科目']['货币资金(元)']:,.2f}")
        print(f"存货: {financial_balance_sheet_data_by_period[date]['关键科目']['存货(元)']:,.2f}")
        print(f"合同负债: {financial_balance_sheet_data_by_period[date]['关键科目']['合同负债(元)']:,.2f}")

        print("\n【同比增长】")
        print(f"总资产增长: {financial_balance_sheet_data_by_period[date]['同比增长']['总资产增长率(%)'] or 0:.2f}%")
        print(f"股东权益增长: {financial_balance_sheet_data_by_period[date]['同比增长']['股东权益增长率(%)'] or 0:.2f}%")





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

def get_financial_balance_data(stock_code, target_date_str):
    """获取财务数据"""
    # 找到最近的报告期
    closest_report_date = find_closest_report_date(target_date_str)

    # 获取前4个报告期
    report_dates = get_previous_report_dates(closest_report_date, 4)

    # 构建API请求URL
    url = (
        "https://datacenter.eastmoney.com/securities/api/data/get?"
        "type=RPT_F10_FINANCE_GBALANCE&"
        "sty=F10_FINANCE_GBALANCE&"
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

    financial_data = get_financial_balance_data(stock_code, target_date)

    parse_financial_balance_data(financial_data)
    print_financial_data()
    print(financial_balance_sheet_data_by_period)


    if financial_data:
        print("获取数据成功:")
        print(financial_data)
    else:
        print("获取数据失败")