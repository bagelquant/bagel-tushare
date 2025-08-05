"""
Database connection and query execution module.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from sqlalchemy import Column, String, Integer, Float, Date, Index
from sqlalchemy.orm import relationship, declarative_base, Session
from sqlalchemy import TIMESTAMP


Base = declarative_base()

def create_all_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def get_engine(host: str,
               port: int,
               user: str,
               password: str,
               database: str) -> Engine:
    return create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')


class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    update_table = Column(String(20), nullable=False)
    message = Column(String(200), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))


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


class TradeCal(Base):
    __tablename__ = 'trade_cal'
    exchange = Column(String(9), primary_key=True)  # 交易所 SSE上交所 SZSE深交所
    cal_date = Column(Date, primary_key=True)  # 日历日期
    is_open = Column(Integer)  # 是否交易 0休市 1交易
    pretrade_date = Column(Date)  # 上一个交易日

class Daily(Base):
    __tablename__ = 'daily'
    __table_args__ = (
        Index('idx_daily_ts_code', 'ts_code'),
        Index('idx_daily_trade_date', 'trade_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20))  # TS股票代码
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

class AdjFactor(Base):
    __tablename__ = 'adj_factor'
    __table_args__ = (
        Index('idx_adjfactor_ts_code', 'ts_code'),
        Index('idx_adjfactor_trade_date', 'trade_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20))  # TS股票代码
    trade_date = Column(Date)  # 交易日期
    adj_factor = Column(Float)  # 复权因子

class DailyBasic(Base):
    __tablename__ = 'daily_basic'
    __table_args__ = (
        Index('idx_dailybasic_ts_code', 'ts_code'),
        Index('idx_dailybasic_trade_date', 'trade_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20))  # TS股票代码
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

class Income(Base):
    __tablename__ = 'income'
    __table_args__ = (
        Index('idx_income_ts_code', 'ts_code'),
        Index('idx_income_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20))
    ann_date = Column(Date)
    f_ann_date = Column(Date)
    end_date = Column(Date)
    report_type = Column(String(8))
    comp_type = Column(String(8))
    end_type = Column(String(8))
    basic_eps = Column(Float)
    diluted_eps = Column(Float)
    total_revenue = Column(Float)
    revenue = Column(Float)
    int_income = Column(Float)
    prem_earned = Column(Float)
    comm_income = Column(Float)
    n_commis_income = Column(Float)
    n_oth_income = Column(Float)
    n_oth_b_income = Column(Float)
    prem_income = Column(Float)
    out_prem = Column(Float)
    une_prem_reser = Column(Float)
    reins_income = Column(Float)
    n_sec_tb_income = Column(Float)
    n_sec_uw_income = Column(Float)
    n_asset_mg_income = Column(Float)
    oth_b_income = Column(Float)
    fv_value_chg_gain = Column(Float)
    invest_income = Column(Float)
    ass_invest_income = Column(Float)
    forex_gain = Column(Float)
    total_cogs = Column(Float)
    oper_cost = Column(Float)
    int_exp = Column(Float)
    comm_exp = Column(Float)
    biz_tax_surchg = Column(Float)
    sell_exp = Column(Float)
    admin_exp = Column(Float)
    fin_exp = Column(Float)
    assets_impair_loss = Column(Float)
    prem_refund = Column(Float)
    compens_payout = Column(Float)
    reser_insur_liab = Column(Float)
    div_payt = Column(Float)
    reins_exp = Column(Float)
    oper_exp = Column(Float)
    compens_payout_refu = Column(Float)
    insur_reser_refu = Column(Float)
    reins_cost_refund = Column(Float)
    other_bus_cost = Column(Float)
    operate_profit = Column(Float)
    non_oper_income = Column(Float)
    non_oper_exp = Column(Float)
    nca_disploss = Column(Float)
    total_profit = Column(Float)
    income_tax = Column(Float)
    n_income = Column(Float)
    n_income_attr_p = Column(Float)
    minority_gain = Column(Float)
    oth_compr_income = Column(Float)
    t_compr_income = Column(Float)
    compr_inc_attr_p = Column(Float)
    compr_inc_attr_m_s = Column(Float)
    ebit = Column(Float)
    ebitda = Column(Float)
    insurance_exp = Column(Float)
    undist_profit = Column(Float)
    distable_profit = Column(Float)
    rd_exp = Column(Float)
    fin_exp_int_exp = Column(Float)
    fin_exp_int_inc = Column(Float)
    transfer_surplus_rese = Column(Float)
    transfer_housing_imprest = Column(Float)
    transfer_oth = Column(Float)
    adj_lossgain = Column(Float)
    withdra_legal_surplus = Column(Float)
    withdra_legal_pubfund = Column(Float)
    withdra_biz_devfund = Column(Float)
    withdra_rese_fund = Column(Float)
    withdra_oth_ersu = Column(Float)
    workers_welfare = Column(Float)
    distr_profit_shrhder = Column(Float)
    prfshare_payable_dvd = Column(Float)
    comshare_payable_dvd = Column(Float)
    capit_comstock_div = Column(Float)
    net_after_nr_lp_correct = Column(Float)
    credit_impa_loss = Column(Float)
    net_expo_hedging_benefits = Column(Float)
    oth_impair_loss_assets = Column(Float)
    total_opcost = Column(Float)
    amodcost_fin_assets = Column(Float)
    oth_income = Column(Float)
    asset_disp_income = Column(Float)
    continued_net_profit = Column(Float)
    end_net_profit = Column(Float)
    update_flag = Column(String(8))

class BalanceSheet(Base):
    __tablename__ = 'balancesheet'
    __table_args__ = (
        Index('idx_balancesheet_ts_code', 'ts_code'),
        Index('idx_balancesheet_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20))
    ann_date = Column(Date)
    f_ann_date = Column(Date)
    end_date = Column(Date)
    report_type = Column(String(8))
    comp_type = Column(String(8))
    end_type = Column(String(8))
    total_share = Column(Float)
    cap_rese = Column(Float)
    undistr_porfit = Column(Float)
    surplus_rese = Column(Float)
    special_rese = Column(Float)
    money_cap = Column(Float)
    trad_asset = Column(Float)
    notes_receiv = Column(Float)
    accounts_receiv = Column(Float)
    oth_receiv = Column(Float)
    prepayment = Column(Float)
    div_receiv = Column(Float)
    int_receiv = Column(Float)
    inventories = Column(Float)
    amor_exp = Column(Float)
    nca_within_1y = Column(Float)
    sett_rsrv = Column(Float)
    loanto_oth_bank_fi = Column(Float)
    premium_receiv = Column(Float)
    reinsur_receiv = Column(Float)
    reinsur_res_receiv = Column(Float)
    pur_resale_fa = Column(Float)
    oth_cur_assets = Column(Float)
    total_cur_assets = Column(Float)
    fa_avail_for_sale = Column(Float)
    htm_invest = Column(Float)
    lt_eqt_invest = Column(Float)
    invest_real_estate = Column(Float)
    time_deposits = Column(Float)
    oth_assets = Column(Float)
    lt_rec = Column(Float)
    fix_assets = Column(Float)
    cip = Column(Float)
    const_materials = Column(Float)
    fixed_assets_disp = Column(Float)
    produc_bio_assets = Column(Float)
    oil_and_gas_assets = Column(Float)
    intan_assets = Column(Float)
    r_and_d = Column(Float)
    goodwill = Column(Float)
    lt_amor_exp = Column(Float)
    defer_tax_assets = Column(Float)
    decr_in_disbur = Column(Float)
    oth_nca = Column(Float)
    total_nca = Column(Float)
    cash_reser_cb = Column(Float)
    depos_in_oth_bfi = Column(Float)
    prec_metals = Column(Float)
    deriv_assets = Column(Float)
    rr_reins_une_prem = Column(Float)
    rr_reins_outstd_cla = Column(Float)
    rr_reins_lins_liab = Column(Float)
    rr_reins_lthins_liab = Column(Float)
    refund_depos = Column(Float)
    ph_pledge_loans = Column(Float)
    refund_cap_depos = Column(Float)
    indep_acct_assets = Column(Float)
    client_depos = Column(Float)
    client_prov = Column(Float)
    transac_seat_fee = Column(Float)
    invest_as_receiv = Column(Float)
    total_assets = Column(Float)
    lt_borr = Column(Float)
    st_borr = Column(Float)
    cb_borr = Column(Float)
    depos_ib_deposits = Column(Float)
    loan_oth_bank = Column(Float)
    trading_fl = Column(Float)
    notes_payable = Column(Float)
    acct_payable = Column(Float)
    adv_receipts = Column(Float)
    sold_for_repur_fa = Column(Float)
    comm_payable = Column(Float)
    payroll_payable = Column(Float)
    taxes_payable = Column(Float)
    int_payable = Column(Float)
    div_payable = Column(Float)
    oth_payable = Column(Float)
    acc_exp = Column(Float)
    deferred_inc = Column(Float)
    st_bonds_payable = Column(Float)
    payable_to_reinsurer = Column(Float)
    rsrv_insur_cont = Column(Float)
    acting_trading_sec = Column(Float)
    acting_uw_sec = Column(Float)
    non_cur_liab_due_1y = Column(Float)
    oth_cur_liab = Column(Float)
    total_cur_liab = Column(Float)
    bond_payable = Column(Float)
    lt_payable = Column(Float)
    specific_payables = Column(Float)
    estimated_liab = Column(Float)
    defer_tax_liab = Column(Float)
    defer_inc_non_cur_liab = Column(Float)
    oth_ncl = Column(Float)
    total_ncl = Column(Float)
    depos_oth_bfi = Column(Float)
    deriv_liab = Column(Float)
    depos = Column(Float)
    agency_bus_liab = Column(Float)
    oth_liab = Column(Float)
    prem_receiv_adva = Column(Float)
    depos_received = Column(Float)
    ph_invest = Column(Float)
    reser_une_prem = Column(Float)
    reser_outstd_claims = Column(Float)
    reser_lins_liab = Column(Float)
    reser_lthins_liab = Column(Float)
    indept_acc_liab = Column(Float)
    pledge_borr = Column(Float)
    indem_payable = Column(Float)
    policy_div_payable = Column(Float)
    total_liab = Column(Float)
    treasury_share = Column(Float)
    ordin_risk_reser = Column(Float)
    forex_differ = Column(Float)
    invest_loss_unconf = Column(Float)
    minority_int = Column(Float)
    total_hldr_eqy_exc_min_int = Column(Float)
    total_hldr_eqy_inc_min_int = Column(Float)
    total_liab_hldr_eqy = Column(Float)
    lt_payroll_payable = Column(Float)
    oth_comp_income = Column(Float)
    oth_eqt_tools = Column(Float)
    oth_eqt_tools_p_shr = Column(Float)
    lending_funds = Column(Float)
    acc_receivable = Column(Float)
    st_fin_payable = Column(Float)
    payables = Column(Float)
    hfs_assets = Column(Float)
    hfs_sales = Column(Float)
    cost_fin_assets = Column(Float)
    fair_value_fin_assets = Column(Float)
    cip_total = Column(Float)
    oth_pay_total = Column(Float)
    long_pay_total = Column(Float)
    debt_invest = Column(Float)
    oth_debt_invest = Column(Float)
    oth_eq_invest = Column(Float)
    oth_illiq_fin_assets = Column(Float)
    oth_eq_ppbond = Column(Float)
    receiv_financing = Column(Float)
    use_right_assets = Column(Float)
    lease_liab = Column(Float)
    contract_assets = Column(Float)
    contract_liab = Column(Float)
    accounts_receiv_bill = Column(Float)
    accounts_pay = Column(Float)
    oth_rcv_total = Column(Float)
    fix_assets_total = Column(Float)
    update_flag = Column(String(8))


class Cashflow(Base):
    __tablename__ = 'cashflow'
    __table_args__ = (
        Index('idx_cashflow_ts_code', 'ts_code'),
        Index('idx_cashflow_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20))
    ann_date = Column(Date)
    f_ann_date = Column(Date)
    end_date = Column(Date)
    comp_type = Column(String(8))
    report_type = Column(String(8))
    end_type = Column(String(8))
    net_profit = Column(Float)
    finan_exp = Column(Float)
    c_fr_sale_sg = Column(Float)
    recp_tax_rends = Column(Float)
    n_depos_incr_fi = Column(Float)
    n_incr_loans_cb = Column(Float)
    n_inc_borr_oth_fi = Column(Float)
    prem_fr_orig_contr = Column(Float)
    n_incr_insured_dep = Column(Float)
    n_reinsur_prem = Column(Float)
    n_incr_disp_tfa = Column(Float)
    ifc_cash_incr = Column(Float)
    n_incr_disp_faas = Column(Float)
    n_incr_loans_oth_bank = Column(Float)
    n_cap_incr_repur = Column(Float)
    c_fr_oth_operate_a = Column(Float)
    c_inf_fr_operate_a = Column(Float)
    c_paid_goods_s = Column(Float)
    c_paid_to_for_empl = Column(Float)
    c_paid_for_taxes = Column(Float)
    n_incr_clt_loan_adv = Column(Float)
    n_incr_dep_cbob = Column(Float)
    c_pay_claims_orig_inco = Column(Float)
    pay_handling_chrg = Column(Float)
    pay_comm_insur_plcy = Column(Float)
    oth_cash_pay_oper_act = Column(Float)
    st_cash_out_act = Column(Float)
    n_cashflow_act = Column(Float)
    oth_recp_ral_inv_act = Column(Float)
    c_disp_withdrwl_invest = Column(Float)
    c_recp_return_invest = Column(Float)
    n_recp_disp_fiolta = Column(Float)
    n_recp_disp_sobu = Column(Float)
    stot_inflows_inv_act = Column(Float)
    c_pay_acq_const_fiolta = Column(Float)
    c_paid_invest = Column(Float)
    n_disp_subs_oth_biz = Column(Float)
    oth_pay_ral_inv_act = Column(Float)
    n_incr_pledge_loan = Column(Float)
    stot_out_inv_act = Column(Float)
    n_cashflow_inv_act = Column(Float)
    c_recp_borrow = Column(Float)
    proc_issue_bonds = Column(Float)
    oth_cash_recp_ral_fnc_act = Column(Float)
    stot_cash_in_fnc_act = Column(Float)
    free_cashflow = Column(Float)
    c_prepay_amt_borr = Column(Float)
    c_pay_dist_dpcp_int_exp = Column(Float)
    incl_dvd_profit_paid_sc_ms = Column(Float)
    oth_cashpay_ral_fnc_act = Column(Float)
    stot_cashout_fnc_act = Column(Float)
    n_cash_flows_fnc_act = Column(Float)
    eff_fx_flu_cash = Column(Float)
    n_incr_cash_cash_equ = Column(Float)
    c_cash_equ_beg_period = Column(Float)
    c_cash_equ_end_period = Column(Float)
    c_recp_cap_contrib = Column(Float)
    incl_cash_rec_saims = Column(Float)
    uncon_invest_loss = Column(Float)
    prov_depr_assets = Column(Float)
    depr_fa_coga_dpba = Column(Float)
    amort_intang_assets = Column(Float)
    lt_amort_deferred_exp = Column(Float)
    decr_deferred_exp = Column(Float)
    incr_acc_exp = Column(Float)
    loss_disp_fiolta = Column(Float)
    loss_scr_fa = Column(Float)
    loss_fv_chg = Column(Float)
    invest_loss = Column(Float)
    decr_def_inc_tax_assets = Column(Float)
    incr_def_inc_tax_liab = Column(Float)
    decr_inventories = Column(Float)
    decr_oper_payable = Column(Float)
    incr_oper_payable = Column(Float)
    others = Column(Float)
    im_net_cashflow_oper_act = Column(Float)
    conv_debt_into_cap = Column(Float)
    conv_copbonds_due_within_1y = Column(Float)
    fa_fnc_leases = Column(Float)
    im_n_incr_cash_equ = Column(Float)
    net_dism_capital_add = Column(Float)
    net_cash_rece_sec = Column(Float)
    credit_impa_loss = Column(Float)
    use_right_asset_dep = Column(Float)
    oth_loss_asset = Column(Float)
    end_bal_cash = Column(Float)
    beg_bal_cash = Column(Float)
    end_bal_cash_equ = Column(Float)
    beg_bal_cash_equ = Column(Float)
    update_flag = Column(String(8))
    

class FinaIndicator(Base):
    __tablename__ = 'fina_indicator'
    __table_args__ = (
        Index('idx_finaindicator_ts_code', 'ts_code'),
        Index('idx_finaindicator_end_date', 'end_date'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20))
    ann_date = Column(Date)
    end_date = Column(Date)
    eps = Column(Float)
    dt_eps = Column(Float)
    total_revenue_ps = Column(Float)
    revenue_ps = Column(Float)
    capital_rese_ps = Column(Float)
    surplus_rese_ps = Column(Float)
    undist_profit_ps = Column(Float)
    extra_item = Column(Float)
    profit_dedt = Column(Float)
    gross_margin = Column(Float)
    current_ratio = Column(Float)
    quick_ratio = Column(Float)
    cash_ratio = Column(Float)
    invturn_days = Column(Float)
    arturn_days = Column(Float)
    inv_turn = Column(Float)
    ar_turn = Column(Float)
    ca_turn = Column(Float)
    fa_turn = Column(Float)
    assets_turn = Column(Float)
    op_income = Column(Float)
    valuechange_income = Column(Float)
    interst_income = Column(Float)
    daa = Column(Float)
    ebit = Column(Float)
    ebitda = Column(Float)
    fcff = Column(Float)
    fcfe = Column(Float)
    current_exint = Column(Float)
    noncurrent_exint = Column(Float)
    interestdebt = Column(Float)
    netdebt = Column(Float)
    tangible_asset = Column(Float)
    working_capital = Column(Float)
    networking_capital = Column(Float)
    invest_capital = Column(Float)
    retained_earnings = Column(Float)
    diluted2_eps = Column(Float)
    bps = Column(Float)
    ocfps = Column(Float)
    retainedps = Column(Float)
    cfps = Column(Float)
    ebit_ps = Column(Float)
    fcff_ps = Column(Float)
    fcfe_ps = Column(Float)
    netprofit_margin = Column(Float)
    grossprofit_margin = Column(Float)
    cogs_of_sales = Column(Float)
    expense_of_sales = Column(Float)
    profit_to_gr = Column(Float)
    saleexp_to_gr = Column(Float)
    adminexp_of_gr = Column(Float)
    finaexp_of_gr = Column(Float)
    impai_ttm = Column(Float)
    gc_of_gr = Column(Float)
    op_of_gr = Column(Float)
    ebit_of_gr = Column(Float)
    roe = Column(Float)
    roe_waa = Column(Float)
    roe_dt = Column(Float)
    roa = Column(Float)
    npta = Column(Float)
    roic = Column(Float)
    roe_yearly = Column(Float)
    roa2_yearly = Column(Float)
    roe_avg = Column(Float)
    opincome_of_ebt = Column(Float)
    investincome_of_ebt = Column(Float)
    n_op_profit_of_ebt = Column(Float)
    tax_to_ebt = Column(Float)
    dtprofit_to_profit = Column(Float)
    salescash_to_or = Column(Float)
    ocf_to_or = Column(Float)
    ocf_to_opincome = Column(Float)
    capitalized_to_da = Column(Float)
    debt_to_assets = Column(Float)
    assets_to_eqt = Column(Float)
    dp_assets_to_eqt = Column(Float)
    ca_to_assets = Column(Float)
    nca_to_assets = Column(Float)
    tbassets_to_totalassets = Column(Float)
    int_to_talcap = Column(Float)
    eqt_to_talcapital = Column(Float)
    currentdebt_to_debt = Column(Float)
    longdeb_to_debt = Column(Float)
    ocf_to_shortdebt = Column(Float)
    debt_to_eqt = Column(Float)
    eqt_to_debt = Column(Float)
    eqt_to_interestdebt = Column(Float)
    tangibleasset_to_debt = Column(Float)
    tangasset_to_intdebt = Column(Float)
    tangibleasset_to_netdebt = Column(Float)
    ocf_to_debt = Column(Float)
    ocf_to_interestdebt = Column(Float)
    ocf_to_netdebt = Column(Float)
    ebit_to_interest = Column(Float)
    longdebt_to_workingcapital = Column(Float)
    ebitda_to_debt = Column(Float)
    turn_days = Column(Float)
    roa_yearly = Column(Float)
    roa_dp = Column(Float)
    fixed_assets = Column(Float)
    profit_prefin_exp = Column(Float)
    non_op_profit = Column(Float)
    op_to_ebt = Column(Float)
    nop_to_ebt = Column(Float)
    ocf_to_profit = Column(Float)
    cash_to_liqdebt = Column(Float)
    cash_to_liqdebt_withinterest = Column(Float)
    op_to_liqdebt = Column(Float)
    op_to_debt = Column(Float)
    roic_yearly = Column(Float)
    total_fa_trun = Column(Float)
    profit_to_op = Column(Float)
    q_opincome = Column(Float)
    q_investincome = Column(Float)
    q_dtprofit = Column(Float)
    q_eps = Column(Float)
    q_netprofit_margin = Column(Float)
    q_gsprofit_margin = Column(Float)
    q_exp_to_sales = Column(Float)
    q_profit_to_gr = Column(Float)
    q_saleexp_to_gr = Column(Float)
    q_adminexp_to_gr = Column(Float)
    q_finaexp_to_gr = Column(Float)
    q_impair_to_gr_ttm = Column(Float)
    q_gc_to_gr = Column(Float)
    q_op_to_gr = Column(Float)
    q_roe = Column(Float)
    q_dt_roe = Column(Float)
    q_npta = Column(Float)
    q_opincome_to_ebt = Column(Float)
    q_investincome_to_ebt = Column(Float)
    q_dtprofit_to_profit = Column(Float)
    q_salescash_to_or = Column(Float)
    q_ocf_to_sales = Column(Float)
    q_ocf_to_or = Column(Float)
    basic_eps_yoy = Column(Float)
    dt_eps_yoy = Column(Float)
    cfps_yoy = Column(Float)
    op_yoy = Column(Float)
    ebt_yoy = Column(Float)
    netprofit_yoy = Column(Float)
    dt_netprofit_yoy = Column(Float)
    ocf_yoy = Column(Float)
    roe_yoy = Column(Float)
    bps_yoy = Column(Float)
    assets_yoy = Column(Float)
    eqt_yoy = Column(Float)
    tr_yoy = Column(Float)
    or_yoy = Column(Float)
    q_gr_yoy = Column(Float)
    q_gr_qoq = Column(Float)
    q_sales_yoy = Column(Float)
    q_sales_qoq = Column(Float)
    q_op_yoy = Column(Float)
    q_op_qoq = Column(Float)
    q_profit_yoy = Column(Float)
    q_profit_qoq = Column(Float)
    q_netprofit_yoy = Column(Float)
    q_netprofit_qoq = Column(Float)
    equity_yoy = Column(Float)
    rd_exp = Column(Float)
    update_flag = Column(String(8))


def insert_log(engine: Engine,
               table_name: str, 
            message: str) -> None:
    """
    Inserts a log entry into the `log` table using SQLAlchemy ORM.
    """
    with Session(engine) as session:
        log_entry = Log(update_table=table_name, message=message)
        session.add(log_entry)
        session.commit()


def create_index(engine: Engine,
                 table_name: str) -> None:
    """
    Creates an index on the specified table in the database.

    The function generates a SQL query to create an index on the table's
    columns listed in the `index_list`. The query is executed using the
    provided database engine within a transaction, ensuring changes only
    take effect if the execution succeeds.

    :param engine: A SQLAlchemy Engine object that connects to the database.
    :param table_name: The name of the table on which the index will be created.
    :return: None
    """
    index_list = ['trade_date', 'f_ann_date', 'end_date', 'ts_code']
    # get columns
    query_columns = f"""
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = '{table_name}'
    """

    # get existing indexes
    query_existing = f"""
    SHOW INDEX FROM {table_name}
    """

    # No need to check ORM indexes; only check DB indexes

    with engine.begin() as conn:
        columns = conn.execute(text(query_columns)).fetchall()
        columns = [_[0] for _ in columns]

        existing_indexes = conn.execute(text(query_existing)).fetchall()
        existing_indexes = [_[2] for _ in existing_indexes]

        # Only create indexes if the table has no existing indexes at all
        if not existing_indexes:
            for index in index_list:
                idx_name = f"idx_{table_name}_{index}"
                if index in columns:
                    if index == 'ts_code':
                        # ts_code is TEXT not specify length
                        query_create_index = f"""
                        ALTER TABLE {table_name}
                        MODIFY COLUMN ts_code VARCHAR(20),
                        ADD INDEX {idx_name} (ts_code);
                        """
                    else:
                        query_create_index = f"""
                        CREATE INDEX {idx_name} ON {table_name} ({index});
                        """
                    conn.execute(text(query_create_index))
