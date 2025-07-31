
"""
Tushare ORM Models
==================
SQLAlchemy ORM models for Tushare stock data tables.
Each model matches the official Tushare API schema and uses proper types and relationships.
All `ts_code` fields are foreign keys to `stock_basic`.
"""


from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from .database import Base, create_all_tables

__all__ = [
    "StockBasic", "TradeCal", "NameChange", "StockCompany", "BakBasic",
    "Daily", "AdjFactor", "DailyBasic", "Income", "Balance", "Cashflow", "FinaIndicator",
    "create_all_tables"
]


class StockBasic(Base):
    __tablename__ = 'stock_basic'
    ts_code = Column(String(20), primary_key=True)  # 股票代码
    symbol = Column(String(20))  # 股票代码（无后缀）
    name = Column(String(100))  # 股票名称
    area = Column(String(50))  # 所在地域
    industry = Column(String(50))  # 所属行业
    fullname = Column(String(200))  # 股票全称
    enname = Column(String(200))  # 英文全称
    market = Column(String(20))  # 市场类型（主板/创业板/科创板/北交所）
    exchange = Column(String(20))  # 交易所代码
    curr_type = Column(String(10))  # 交易货币
    list_status = Column(String(2))  # 上市状态 L上市 D退市 P暂停上市
    list_date = Column(Date)  # 上市日期
    delist_date = Column(Date)  # 退市日期
    is_hs = Column(String(2))  # 是否沪深港通标的，N否 H沪股通 S深股通
    cnspell = Column(String(50))  # 拼音缩写
    act_name = Column(String(100))  # 实际控制人
    act_ent_type = Column(String(20))  # 实际控制人类型

    # Relationships
    daily = relationship('Daily', back_populates='stock')
    adj_factors = relationship('AdjFactor', back_populates='stock')
    daily_basics = relationship('DailyBasic', back_populates='stock')
    income = relationship('Income', back_populates='stock')
    balance = relationship('Balance', back_populates='stock')
    cashflow = relationship('Cashflow', back_populates='stock')
    fina_indicator = relationship('FinaIndicator', back_populates='stock')
    namechanges = relationship('NameChange', back_populates='stock')
    stock_company = relationship('StockCompany', back_populates='stock')
    bak_basic = relationship('BakBasic', back_populates='stock')

class TradeCal(Base):
    __tablename__ = 'trade_cal'
    exchange = Column(String(9), primary_key=True)  # 交易所 SSE上交所 SZSE深交所
    cal_date = Column(Date, primary_key=True)  # 日历日期
    is_open = Column(Integer)  # 是否交易 0休市 1交易
    pretrade_date = Column(Date)  # 上一个交易日

class NameChange(Base):
    __tablename__ = 'namechange'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    name = Column(String(100))  # 名称
    start_date = Column(Date)  # 开始日期
    end_date = Column(Date)  # 结束日期
    ann_date = Column(Date)  # 公告日期
    change_reason = Column(String(200))  # 更名原因
    stock = relationship('StockBasic', back_populates='namechanges')

class StockCompany(Base):
    __tablename__ = 'stock_company'
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'), primary_key=True)  # TS股票代码
    exchange = Column(String(9))  # 交易所代码
    chairman = Column(String(50))  # 法人代表
    manager = Column(String(50))  # 总经理
    secretary = Column(String(50))  # 董秘
    reg_capital = Column(Float)  # 注册资本
    setup_date = Column(Date)  # 注册日期
    province = Column(String(50))  # 所在省份
    city = Column(String(50))  # 所在城市
    introduction = Column(String(500))  # 公司介绍
    website = Column(String(100))  # 公司主页
    email = Column(String(100))  # 电子邮件
    office = Column(String(100))  # 办公地址
    employees = Column(Integer)  # 员工人数
    main_business = Column(String(500))  # 主要业务及产品
    business_scope = Column(String(500))  # 经营范围
    stock = relationship('StockBasic', back_populates='stock_company')

class BakBasic(Base):
    __tablename__ = 'bak_basic'
    __table_args__ = (
        Index('idx_bakbasic_ts_code', 'ts_code'),
        Index('idx_bakbasic_trade_date', 'trade_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    trade_date = Column(Date)  # 交易日期
    name = Column(String(100))  # 名称
    industry = Column(String(50))  # 所属行业
    market = Column(String(20))  # 市场类型
    exchange = Column(String(9))  # 交易所代码
    list_status = Column(String(2))  # 上市状态
    list_date = Column(Date)  # 上市日期
    delist_date = Column(Date)  # 退市日期
    stock = relationship('StockBasic', back_populates='bak_basic')

class Daily(Base):
    __tablename__ = 'daily'
    __table_args__ = (
        Index('idx_daily_ts_code', 'ts_code'),
        Index('idx_daily_trade_date', 'trade_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    trade_date = Column(Date)  # 交易日期
    open = Column(Float)  # 开盘价
    high = Column(Float)  # 最高价
    low = Column(Float)  # 最低价
    close = Column(Float)  # 收盘价
    pre_close = Column(Float)  # 昨收价
    change = Column(Float)  # 涨跌额
    pct_chg = Column(Float)  # 涨跌幅
    vol = Column(Float)  # 成交量（手）
    amount = Column(Float)  # 成交额（千元）
    stock = relationship('StockBasic', back_populates='daily')

class AdjFactor(Base):
    __tablename__ = 'adj_factor'
    __table_args__ = (
        Index('idx_adjfactor_ts_code', 'ts_code'),
        Index('idx_adjfactor_trade_date', 'trade_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    trade_date = Column(Date)  # 交易日期
    adj_factor = Column(Float)  # 复权因子
    stock = relationship('StockBasic', back_populates='adj_factors')

class DailyBasic(Base):
    __tablename__ = 'daily_basic'
    __table_args__ = (
        Index('idx_dailybasic_ts_code', 'ts_code'),
        Index('idx_dailybasic_trade_date', 'trade_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    trade_date = Column(Date)  # 交易日期
    close = Column(Float)  # 当日收盘价
    turnover_rate = Column(Float)  # 换手率
    turnover_rate_f = Column(Float)  # 换手率（自由流通股）
    volume_ratio = Column(Float)  # 量比
    pe = Column(Float)  # 市盈率（总市值/净利润， 亏损的PE为空）
    pe_ttm = Column(Float)  # 市盈率（TTM，亏损的PE为空）
    pb = Column(Float)  # 市净率（总市值/净资产）
    ps = Column(Float)  # 市销率
    ps_ttm = Column(Float)  # 市销率（TTM）
    dv_ratio = Column(Float)  # 股息率
    dv_ttm = Column(Float)  # 股息率（TTM）
    total_share = Column(Float)  # 总股本（万股）
    float_share = Column(Float)  # 流通股本（万股）
    free_share = Column(Float)  # 自由流通股本（万股）
    total_mv = Column(Float)  # 总市值（万元）
    circ_mv = Column(Float)  # 流通市值（万元）
    stock = relationship('StockBasic', back_populates='daily_basics')

class Income(Base):
    __tablename__ = 'income'
    __table_args__ = (
        Index('idx_income_ts_code', 'ts_code'),
        Index('idx_income_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    ann_date = Column(Date)  # 公告日期
    f_ann_date = Column(Date)  # 实际公告日期
    end_date = Column(Date)  # 报告期
    report_type = Column(String(8))  # 报告类型
    comp_type = Column(String(8))  # 公司类型
    basic_eps = Column(Float)  # 基本每股收益
    diluted_eps = Column(Float)  # 稀释每股收益
    total_revenue = Column(Float)  # 营业总收入
    revenue = Column(Float)  # 营业收入
    int_income = Column(Float)  # 利息收入
    prem_income = Column(Float)  # 保险业务收入
    comm_income = Column(Float)  # 手续费及佣金收入
    n_commis_income = Column(Float)  # 手续费及佣金净收入
    n_oth_income = Column(Float)  # 其他经营净收益
    n_oth_b_income = Column(Float)  # 加:其他业务净收益
    prem_earned = Column(Float)  # 已赚保费
    n_insur_prem = Column(Float)  # 保险业务净收入
    und_prem = Column(Float)  # 减:分出保费
    reins_income = Column(Float)  # 其中:分保费收入
    n_sec_tb_income = Column(Float)  # 代理买卖证券业务净收入
    n_sec_uw_income = Column(Float)  # 证券承销业务净收入
    n_asset_mg_income = Column(Float)  # 受托客户资产管理业务净收入
    oth_b_income = Column(Float)  # 其他业务收入
    fv_value_chg_gain = Column(Float)  # 加:公允价值变动净收益
    invest_income = Column(Float)  # 加:投资净收益
    ass_invest_income = Column(Float)  # 其中:对联营企业和合营企业的投资收益
    forex_gain = Column(Float)  # 加:汇兑净收益
    total_cogs = Column(Float)  # 营业总成本
    oper_cost = Column(Float)  # 减:营业成本
    int_exp = Column(Float)  # 减:利息支出
    comm_exp = Column(Float)  # 减:手续费及佣金支出
    biz_tax_surchg = Column(Float)  # 减:营业税金及附加
    sell_exp = Column(Float)  # 减:销售费用
    admin_exp = Column(Float)  # 减:管理费用
    fin_exp = Column(Float)  # 减:财务费用
    assets_impair_loss = Column(Float)  # 减:资产减值损失
    prem_refund = Column(Float)  # 退保金
    compens_payout = Column(Float)  # 赔付总支出
    reser_insur_liab = Column(Float)  # 提取保险责任准备金
    div_payt = Column(Float)  # 保户红利支出
    reins_exp = Column(Float)  # 分保费用
    oper_exp = Column(Float)  # 营业支出
    compens_payout_refu = Column(Float)  # 减:摊回赔付支出
    insur_reser_refu = Column(Float)  # 减:摊回保险责任准备金
    reins_cost_refund = Column(Float)  # 减:摊回分保费用
    other_bus_cost = Column(Float)  # 其他业务成本
    operate_profit = Column(Float)  # 营业利润
    non_oper_income = Column(Float)  # 加:营业外收入
    non_oper_exp = Column(Float)  # 减:营业外支出
    nca_disploss = Column(Float)  # 减:非流动资产处置净损失
    total_profit = Column(Float)  # 利润总额
    income_tax = Column(Float)  # 所得税费用
    n_income = Column(Float)  # 净利润(含少数股东损益)
    n_income_attr_p = Column(Float)  # 归属于母公司(股东)的净利润
    minority_gain = Column(Float)  # 少数股东损益
    oth_compr_income = Column(Float)  # 其他综合收益
    compr_income = Column(Float)  # 综合收益总额
    compr_inc_attr_p = Column(Float)  # 归属于母公司(股东)的综合收益总额
    compr_inc_attr_m_s = Column(Float)  # 归属于少数股东的综合收益总额
    earnings_basic = Column(Float)  # 基本每股收益(元)
    stock = relationship('StockBasic', back_populates='income')

class Balance(Base):
    __tablename__ = 'balance'
    __table_args__ = (
        Index('idx_balance_ts_code', 'ts_code'),
        Index('idx_balance_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    ann_date = Column(Date)  # 公告日期
    f_ann_date = Column(Date)  # 实际公告日期
    end_date = Column(Date)  # 报告期
    report_type = Column(String(8))  # 报告类型
    comp_type = Column(String(8))  # 公司类型
    total_share = Column(Float)  # 总股本
    cap_rese = Column(Float)  # 资本公积金
    undistr_porfit = Column(Float)  # 未分配利润
    surplus_rese = Column(Float)  # 盈余公积金
    special_rese = Column(Float)  # 专项储备
    money_cap = Column(Float)  # 货币资金
    trad_asset = Column(Float)  # 交易性金融资产
    notes_receiv = Column(Float)  # 应收票据
    accounts_receiv = Column(Float)  # 应收账款
    oth_receiv = Column(Float)  # 其他应收款
    prepayment = Column(Float)  # 预付款项
    div_receiv = Column(Float)  # 应收股利
    int_receiv = Column(Float)  # 应收利息
    inventories = Column(Float)  # 存货
    amor_exp = Column(Float)  # 待摊费用
    nca_within_1y = Column(Float)  # 一年内到期的非流动资产
    sett_rsrv = Column(Float)  # 结算备付金
    loanto_oth_bank_fi = Column(Float)  # 拆出资金
    premium_receiv = Column(Float)  # 应收保费
    reinsur_receiv = Column(Float)  # 应收分保账款
    reinsu_receiv = Column(Float)  # 应收分保合同准备金
    pur_resale_fa = Column(Float)  # 买入返售金融资产
    oth_cur_assets = Column(Float)  # 其他流动资产
    total_cur_assets = Column(Float)  # 流动资产合计
    fa_avail_for_sale = Column(Float)  # 可供出售金融资产
    htm_invest = Column(Float)  # 持有至到期投资
    lt_eqt_invest = Column(Float)  # 长期股权投资
    invest_real_estate = Column(Float)  # 投资性房地产
    time_deposits = Column(Float)  # 定期存款
    oth_assets = Column(Float)  # 其他资产
    lt_rec = Column(Float)  # 长期应收款
    fix_assets = Column(Float)  # 固定资产
    cip = Column(Float)  # 在建工程
    const_materials = Column(Float)  # 工程物资
    fixed_assets_disp = Column(Float)  # 固定资产清理
    produc_bio_assets = Column(Float)  # 生产性生物资产
    oil_and_gas_assets = Column(Float)  # 油气资产
    intan_assets = Column(Float)  # 无形资产
    r_and_d = Column(Float)  # 研发支出
    goodwill = Column(Float)  # 商誉
    lt_amor_exp = Column(Float)  # 长期待摊费用
    defer_tax_assets = Column(Float)  # 递延所得税资产
    decr_in_disbur = Column(Float)  # 发放贷款及垫款
    oth_nca = Column(Float)  # 其他非流动资产
    total_nca = Column(Float)  # 非流动资产合计
    cash_reser_cb = Column(Float)  # 现金及存放中央银行款项
    depos_in_oth_bfi = Column(Float)  # 存放同业和其它金融机构款项
    prec_metals = Column(Float)  # 贵金属
    deriv_assets = Column(Float)  # 衍生金融资产
    rr_reins_une_prem = Column(Float)  # 应收分保未到期责任准备金
    rr_reins_outstd_cla = Column(Float)  # 应收分保未决赔款准备金
    rr_reins_lins_liab = Column(Float)  # 应收分保寿险责任准备金
    rr_reins_lthins_liab = Column(Float)  # 应收分保长期健康险责任准备金
    refund_depos = Column(Float)  # 存出保证金
    ph_pledge_loans = Column(Float)  # 保户质押贷款
    refund_cap_depos = Column(Float)  # 存出资本保证金
    indep_acct_assets = Column(Float)  # 独立账户资产
    client_depos = Column(Float)  # 其中：客户资金存款
    client_prov = Column(Float)  # 其中：客户备付金
    transac_seat_fee = Column(Float)  # 其中：交易席位费
    invest_as_receiv = Column(Float)  # 应收款项类投资
    total_assets = Column(Float)  # 资产总计
    stock = relationship('StockBasic', back_populates='balance')

class Cashflow(Base):
    __tablename__ = 'cashflow'
    __table_args__ = (
        Index('idx_cashflow_ts_code', 'ts_code'),
        Index('idx_cashflow_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    ann_date = Column(Date)  # 公告日期
    f_ann_date = Column(Date)  # 实际公告日期
    end_date = Column(Date)  # 报告期
    report_type = Column(String(8))  # 报告类型
    comp_type = Column(String(8))  # 公司类型
    net_profit = Column(Float)  # 净利润
    finan_exp = Column(Float)  # 财务费用
    c_fr_sale_sg = Column(Float)  # 销售商品、提供劳务收到的现金
    c_fr_oth_sgs = Column(Float)  # 收到的其他与经营活动有关的现金
    c_payout_biz_act = Column(Float)  # 经营活动现金流出小计
    c_net_cashflow_act = Column(Float)  # 经营活动产生的现金流量净额
    c_fr_sale_fixed_asset = Column(Float)  # 处置固定资产、无形资产和其他长期资产收回的现金净额
    c_fr_oth_invest_act = Column(Float)  # 收到的其他与投资活动有关的现金
    c_payout_invest = Column(Float)  # 投资活动现金流出小计
    c_net_cashflow_inv_act = Column(Float)  # 投资活动产生的现金流量净额
    c_fr_issuing_bonds = Column(Float)  # 发行债券收到的现金
    c_fr_oth_finact = Column(Float)  # 收到的其他与筹资活动有关的现金
    c_payout_bonds = Column(Float)  # 偿还债务支付的现金
    c_payout_div_profit = Column(Float)  # 分配股利、利润或偿付利息支付的现金
    c_net_cashflow_fnc_act = Column(Float)  # 筹资活动产生的现金流量净额
    eff_fx_flu_cash = Column(Float)  # 汇率变动对现金的影响
    n_incr_cash_cash_equ = Column(Float)  # 现金及现金等价物净增加额
    c_cash_equ_beg_period = Column(Float)  # 期初现金及现金等价物余额
    c_cash_equ_end_period = Column(Float)  # 期末现金及现金等价物余额
    c_recp_tax_rends = Column(Float)  # 收到的税费返还
    c_pay_goods_svc = Column(Float)  # 购买商品、接受劳务支付的现金
    c_pay_staff = Column(Float)  # 支付给职工以及为职工支付的现金
    c_pay_tax_surchg = Column(Float)  # 支付的各项税费
    c_pay_oth_biz_act = Column(Float)  # 支付的其他与经营活动有关的现金
    c_recp_interest_income = Column(Float)  # 收到的利息、手续费及佣金
    c_recp_invest_income = Column(Float)  # 收到的投资收益
    c_disp_withdrwl_invest = Column(Float)  # 处置撤回投资收到的现金
    c_recp_borrow = Column(Float)  # 取得借款收到的现金
    c_recp_bonds_iss = Column(Float)  # 发行债券收到的现金
    c_prepay_invest = Column(Float)  # 投资支付的现金
    c_pay_interest_exp = Column(Float)  # 支付的利息
    c_pay_div_profit = Column(Float)  # 支付的股利、利润
    c_recp_oth_finact = Column(Float)  # 收到的其他与筹资活动有关的现金
    c_pay_oth_finact = Column(Float)  # 支付的其他与筹资活动有关的现金
    c_recp_oth_biz_act = Column(Float)  # 收到的其他与经营活动有关的现金
    c_pay_oth_biz_act = Column(Float)  # 支付的其他与经营活动有关的现金
    stock = relationship('StockBasic', back_populates='cashflow')

class FinaIndicator(Base):
    __tablename__ = 'fina_indicator'
    __table_args__ = (
        Index('idx_finaindicator_ts_code', 'ts_code'),
        Index('idx_finaindicator_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), ForeignKey('stock_basic.ts_code'))  # TS股票代码
    ann_date = Column(Date)  # 公告日期
    end_date = Column(Date)  # 报告期
    eps = Column(Float)  # 每股收益
    dt_eps = Column(Float)  # 每股收益（扣除非经常性损益）
    total_revenue_ps = Column(Float)  # 每股营业总收入
    revenue_ps = Column(Float)  # 每股营业收入
    capital_rese_ps = Column(Float)  # 每股资本公积金
    surplus_rese_ps = Column(Float)  # 每股盈余公积金
    undist_profit_ps = Column(Float)  # 每股未分配利润
    extra_item = Column(Float)  # 非经常性损益
    profit_dedt = Column(Float)  # 扣除非经常性损益后的净利润
    gross_margin = Column(Float)  # 销售毛利率
    current_ratio = Column(Float)  # 流动比率
    quick_ratio = Column(Float)  # 速动比率
    cash_ratio = Column(Float)  # 保守速动比率
    ar_turn = Column(Float)  # 应收账款周转率
    ca_turn = Column(Float)  # 流动资产周转率
    fa_turn = Column(Float)  # 固定资产周转率
    assets_turn = Column(Float)  # 总资产周转率
    op_income = Column(Float)  # 经营活动净收益
    valuechange_income = Column(Float)  # 价值变动净收益
    interst_income = Column(Float)  # 利息费用
    daa = Column(Float)  # 折旧与摊销
    ebit = Column(Float)  # 息税前利润
    ebitda = Column(Float)  # 息税折旧摊销前利润
    fcff = Column(Float)  # 企业自由现金流量
    fcfe = Column(Float)  # 股权自由现金流量
    current_exint = Column(Float)  # 无息流动负债
    noncurrent_exint = Column(Float)  # 无息非流动负债
    interestdebt = Column(Float)  # 带息债务
    netdebt = Column(Float)  # 净债务
    tangible_asset = Column(Float)  # 有形资产
    working_capital = Column(Float)  # 营运资金
    networking_capital = Column(Float)  # 营运流动资本
    invest_capital = Column(Float)  # 投资资本
    retained_earnings = Column(Float)  # 留存收益
    diluted2_eps = Column(Float)  # 稀释每股收益（二）
    bps = Column(Float)  # 每股净资产
    ocfps = Column(Float)  # 每股经营活动产生的现金流量净额
    retainedps = Column(Float)  # 每股留存收益
    cfps = Column(Float)  # 每股现金流量净额
    ebit_ps = Column(Float)  # 每股息税前利润
    fcff_ps = Column(Float)  # 每股企业自由现金流量
    fcfe_ps = Column(Float)  # 每股股东自由现金流量
    netprofit_margin = Column(Float)  # 销售净利率
    grossprofit_margin = Column(Float)  # 销售毛利率
    cogs_of_sales = Column(Float)  # 销售成本率
    expense_of_sales = Column(Float)  # 销售期间费用率
    profit_to_gr = Column(Float)  # 净利润/营业总收入
    saleexp_to_gr = Column(Float)  # 销售费用/营业总收入
    adminexp_of_gr = Column(Float)  # 管理费用/营业总收入
    finaexp_of_gr = Column(Float)  # 财务费用/营业总收入
    impai_ttm = Column(Float)  # 资产减值损失/营业总收入
    gc_of_gr = Column(Float)  # 营业总成本/营业总收入
    op_of_gr = Column(Float)  # 营业利润/营业总收入
    ebit_of_gr = Column(Float)  # 息税前利润/营业总收入
    roe = Column(Float)  # 净资产收益率
    roe_waa = Column(Float)  # 加权平均净资产收益率
    roe_dt = Column(Float)  # 净资产收益率(扣除非经常性损益)
    roa = Column(Float)  # 总资产报酬率
    npta = Column(Float)  # 总资产净利润
    debt_to_assets = Column(Float)  # 资产负债率
    assets_to_eqt = Column(Float)  # 权益乘数
    dp_assets_to_eqt = Column(Float)  # 权益乘数(杜邦分析)
    ca_to_assets = Column(Float)  # 流动资产/总资产
    nca_to_assets = Column(Float)  # 非流动资产/总资产
    tbassets_to_totalassets = Column(Float)  # 有形资产/总资产
    int_to_talcap = Column(Float)  # 带息债务/全部投入资本
    eqt_to_talcapital = Column(Float)  # 股东权益/全部投入资本
    currentdebt_to_debt = Column(Float)  # 流动负债/负债合计
    longdeb_to_debt = Column(Float)  # 长期负债/负债合计
    ocf_to_shortdebt = Column(Float)  # 经营活动产生的现金流量净额/流动负债
    debt_to_eqt = Column(Float)  # 产权比率
    eqt_to_debt = Column(Float)  # 归属于母公司的股东权益/负债合计
    eqt_to_interestdebt = Column(Float)  # 归属于母公司的股东权益/带息债务
    tangibleasset_to_debt = Column(Float)  # 有形资产/负债合计
    tangasset_to_intdebt = Column(Float)  # 有形资产/带息债务
    tangibleasset_to_netdebt = Column(Float)  # 有形资产/净债务
    ocf_to_debt = Column(Float)  # 经营活动产生的现金流量净额/负债合计
    ocf_to_interestdebt = Column(Float)  # 经营活动产生的现金流量净额/带息债务
    ocf_to_netdebt = Column(Float)  # 经营活动产生的现金流量净额/净债务
    ebit_to_interest = Column(Float)  # 息税前利润/利息费用
    longdebt_to_workingcapital = Column(Float)  # 长期负债/营运资金
    ebitda_to_debt = Column(Float)  # 息税折旧摊销前利润/负债合计
    turn_days = Column(Float)  # 营业周期
    roa_yearly = Column(Float)  # 年化总资产报酬率
    roa_dp = Column(Float)  # 总资产报酬率(杜邦分析)
    fixed_assets = Column(Float)  # 固定资产合计
    profit_prefin_exp = Column(Float)  # 扣除财务费用前营业利润
    non_op_profit = Column(Float)  # 非营业利润
    op_to_ebt = Column(Float)  # 营业利润/利润总额
    nop_to_ebt = Column(Float)  # 非营业利润/利润总额
    ocf_to_profit = Column(Float)  # 经营活动产生的现金流量净额/营业利润
    cash_to_liqdebt = Column(Float)  # 货币资金/流动负债
    cash_to_liqdebt_withinterest = Column(Float)  # 货币资金/带息流动负债
    op_to_liqdebt = Column(Float)  # 营业利润/流动负债
    op_to_debt = Column(Float)  # 营业利润/负债合计
    roic = Column(Float)  # 投入资本回报率
    roe_yearly = Column(Float)  # 年化净资产收益率
    total_fa_trun = Column(Float)  # 固定资产合计周转率
    profit_to_op = Column(Float)  # 利润总额/营业利润
    q_saleexp_to_gr = Column(Float)  # 销售费用/营业总收入(单季度)
    q_gc_to_gr = Column(Float)  # 营业总成本/营业总收入(单季度)
    q_roe = Column(Float)  # 净资产收益率(单季度)
    q_dt_roe = Column(Float)  # 净资产收益率-扣除非经常性损益(单季度)
    q_npta = Column(Float)  # 总资产净利润(单季度)
    q_netprofit_margin = Column(Float)  # 销售净利率(单季度)
    q_gsprofit_margin = Column(Float)  # 销售毛利率(单季度)
    q_exp_to_sales = Column(Float)  # 销售期间费用率(单季度)
    q_profit_to_gr = Column(Float)  # 净利润/营业总收入(单季度)
    q_saleexp_to_gr_yoy = Column(Float)  # 销售费用同比
    q_gc_to_gr_yoy = Column(Float)  # 营业总成本同比
    q_roe_yoy = Column(Float)  # 净资产收益率(单季度同比)
    q_dt_roe_yoy = Column(Float)  # 净资产收益率-扣除非经常性损益(单季度同比)
    q_npta_yoy = Column(Float)  # 总资产净利润(单季度同比)
    q_netprofit_margin_yoy = Column(Float)  # 销售净利率(单季度同比)
    q_gsprofit_margin_yoy = Column(Float)  # 销售毛利率(单季度同比)
    stock = relationship('StockBasic', back_populates='fina_indicator')
