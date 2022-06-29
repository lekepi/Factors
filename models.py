from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, \
    Date, Float, Boolean, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import ConfigDefault
from datetime import datetime
import sys

config_class = ConfigDefault  # get the config file from config.py classes

try:
    my_URI = config_class.SQLALCHEMY_DATABASE_URI
except:
    print("The config file is incorrect")
    sys.exit(1)

Base = declarative_base()
engine = create_engine(my_URI)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Trade(Base):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True)
    order_number = Column(String(length=20), nullable=False)
    trade_date = Column(Date, nullable=False)
    settle_date = Column(Date, nullable=False)
    side = Column(String(length=1), nullable=False)
    is_short = Column(Boolean)
    quantity = Column(Float)
    ticker = Column(String(length=20), nullable=False)
    exec_price = Column(Float, nullable=False)
    broker = Column(String(length=10))
    account = Column(String(length=45))
    cncy = Column(String(length=3))
    sec_name = Column(String(length=45))
    sedol = Column(String(length=7))
    isin = Column(String(length=12))
    cusip = Column(String(length=20))
    bbg_type = Column(String(length=10))
    is_cfd = Column(Boolean)
    origin = Column(String(length=10))
    active = Column(Boolean, default=True)
    created_time = Column(Date, nullable=False, default=datetime.now)
    modified_time = Column(Date)
    created_by = Column(String(length=20), nullable=False)
    modified_by = Column(String(length=20))
    comment = Column(String(length=200))
    file_name = Column(String(length=200))
    product_id = Column(ForeignKey("product.id"))
    product = relationship("Product")
    parent_fund_id = Column(ForeignKey("parent_fund.id"))
    parent_fund = relationship("ParentFund")
    long_future_name = Column(String(length=45))
    allocs = relationship('Allocation', viewonly=True, lazy=True)
    parent_broker_id = Column(ForeignKey("parent_broker.id"))
    parent_broker = relationship("ParentBroker")
    fx_rate = Column(Float)
    pnl_close = Column(Float)
    pnl_1d = Column(Float)
    pnl_2d = Column(Float)
    pnl_3d = Column(Float)
    pnl_4d = Column(Float)
    pnl_5d = Column(Float)
    notional_usd = Column(Float)

    def __repr__(self):
        return f"Trade: {self.trade_date.strftime('%Y-%m-%d')}, id:{self.id}, Account:{self.account} -" \
               f" {self.side} {int(self.quantity)} {self.ticker}"


class Allocation(Base):
    __tablename__ = 'allocation'
    id = Column(Integer, primary_key=True)
    trade_id = Column(ForeignKey("trade.id"))
    trade = relationship("Trade")
    account_id = Column(ForeignKey("account.id"))
    account = relationship("Account")
    quantity = Column(Float)
    active = Column(Boolean, default=True)
    exec_fee = Column(Float)
    sec_fee = Column(Float)
    side = Column(String(length=2))


class ParentBroker(Base):
    __tablename__ = 'parent_broker'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=10), nullable=False)
    long_name = Column(String(length=45), nullable=False)


class OmsBroker(Base):
    __tablename__ = 'oms_broker'
    id = Column(Integer, primary_key=True)
    code = Column(String(length=20), nullable=False)
    parent_broker_id = Column(ForeignKey("parent_broker.id"))
    parent_broker = relationship("ParentBroker")


class FeeRule(Base):
    __tablename__ = 'fee_rule'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=45), nullable=False)
    rate = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)


class ExecFee(Base):
    __tablename__ = 'exec_fee'
    id = Column(Integer, primary_key=True)
    parent_broker_id = Column(ForeignKey("parent_broker.id"))
    parent_broker = relationship("ParentBroker")
    country_id = Column(ForeignKey("country.id"))
    country = relationship("Country")
    rate = Column(Float, nullable=False)
    rate_type = Column(String(length=10), nullable=False)
    min_amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)


class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True)
    bbg_code = Column(String(length=10), nullable=False)
    country_id = Column(ForeignKey("country.id"))
    country = relationship("Country")


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=45), nullable=False)
    continent = Column(String(length=10), nullable=False)
    iso_code = Column(String(length=3), nullable=False)
    settle_day = Column(Integer)
    holidays = relationship('SettlementHoliday', viewonly=True, lazy=True)


class SettlementHoliday(Base):
    __tablename__ = 'settlement_holiday'
    id = Column(Integer, primary_key=True)
    country_id = Column(ForeignKey("country.id"), nullable=False)
    country = relationship("Country")
    holiday_date = Column(Date, nullable=False)


class IndustrySector(Base):
    __tablename__ = 'industry_sector'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))


class IndustryGroup(Base):
    __tablename__ = 'industry_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    asset_class = Column(String(length=45))
    location = Column(String(length=45))
    broker = Column(String(length=45))
    code = Column(String(length=45))
    name = Column(String(length=45))
    fund_id = Column(ForeignKey("fund.id"))
    fund = relationship("Fund")
    oms_account_id = Column(ForeignKey("oms_account.id"))
    oms_account = relationship("OmsAccount")


class OmsAccount(Base):
    __tablename__ = 'oms_account'
    id = Column(Integer, primary_key=True)
    code = Column(String(length=20))
    still_active = Column(Boolean)
    parent_fund_id = Column(ForeignKey("parent_fund.id"))
    parent_fund = relationship("ParentFund")


class ParentFund(Base):
    __tablename__ = 'parent_fund'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=45))


class Fund(Base):
    __tablename__ = 'fund'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=45))
    parent = Column(String(length=45))


class FundSplit(Base):
    __tablename__ = 'fund_split'
    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    client = Column(String(length=45), nullable=False)
    fund_id = Column(ForeignKey("fund.id"), nullable=False)
    fund = relationship("Fund")
    percentage = Column(Float, nullable=False)


class TaskChecker(Base):
    __tablename__ = 'task_checker'
    id = Column(Integer, primary_key=True)
    date_time = Column(Date, nullable=False, default=datetime.now)
    task_name = Column(String(length=45), nullable=False)
    task_type = Column(String(length=45), nullable=False)
    task_details = Column(String(length=45), nullable=False)
    status = Column(String(length=45), nullable=False)
    comment = Column(String(length=200), nullable=False)
    active = Column(Boolean, default=True)
    def __repr__(self):
        return f"<TaskChecker(date='{self.date_time}', task name='{self.task_name}', status='{self.status}')>"


class LogDb(Base):
    __tablename__ = 'log_db'
    id = Column(Integer, primary_key=True)
    date_time = Column(Date, nullable=False, default=datetime.now)
    project = Column(String(length=45), nullable=False)
    task = Column(String(length=45), nullable=False)
    issue = Column(String(length=45), nullable=False)
    msg_type = Column(String(length=45), nullable=False)
    description = Column(String(length=400), nullable=False)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(length=40), nullable=False)
    name = Column(String(length=60), nullable=False)
    isin = Column(String(length=12))
    sedol = Column(String(length=7))
    expiry = Column(Date)
    expiry2 = Column(Date)
    strike = Column(Float)
    prod_type = Column(String(length=10))
    currency_id = Column(ForeignKey("currency.id"))
    currency = relationship("Currency", foreign_keys=[currency_id])
    security_id = Column(ForeignKey("security.id"))
    security = relationship("Security")
    exchange_id = Column(ForeignKey("exchange.id"))
    exchange = relationship("Exchange")
    industry_sector_id = Column(ForeignKey("industry_sector.id"))
    industry_sector = relationship("IndustrySector")
    industry_group_id = Column(ForeignKey("industry_group.id"))
    industry_group = relationship("IndustryGroup")
    currency2_id = Column(ForeignKey("currency.id"))
    currency2 = relationship("Currency", foreign_keys=[currency2_id])
    is_cent = Column(Boolean)
    multiplier = Column(Float)
    still_active = Column(Boolean, default=True)
    created_date = Column(Date, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Product(ticker='{self.ticker}', name='{self.name}', prod_type='{self.prod_type}')>"


class ProductBeta(Base):
    __tablename__ = 'product_beta'
    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey("product.id"))
    product = relationship("Product")
    entry_date = Column(Date, nullable=False)
    beta = Column(Float)
    alpha = Column(Float)
    return_1d = Column(Float)


class Security(Base):
    __tablename__ = 'security'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=60), nullable=False)
    ticker = Column(String(length=40))
    isin = Column(String(length=12))
    asset_type = Column(String(length=20))
    generic_future = Column(String(length=20))
    expiry_type = Column(String(length=20))
    expi_country_id = Column(Integer)
    roll_reminder = Column(Integer)
    expi_months = Column(String(length=20))

    def __repr__(self):
        return f"<Product(name='{self.name}', asset_type='{self.asset_type}')>"


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=45))
    code = Column(String(length=45), nullable=False, unique=True)
    symbol = Column(String(length=45))

    def __repr__(self):
        return f"<Currency(name='{self.name}', code='{self.code}', symbol='{self.symbol}')>"


class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    entry_date = Column(Date, nullable=False)
    parent_fund_id = Column(ForeignKey("parent_fund.id"), nullable=False)
    parent_fund = relationship("ParentFund")
    product_id = Column(ForeignKey("product.id"), nullable=False)
    product = relationship("Product")
    quantity = Column(Float, nullable=False)
    ticker = Column(String(length=20))
    mkt_price = Column(Float)
    mkt_value_usd = Column(Float)
    perf_1d = Column(Float)
    beta = Column(Float)
    pnl_usd = Column(Float)
    alpha_usd = Column(Float)
    perf_1m = Column(Float)
    perf_3m = Column(Float)
    perf_6m = Column(Float)
    perf_1y = Column(Float)
    perf_2y = Column(Float)
    perf_3y = Column(Float)
    qty_gs = Column(Float)
    qty_ms = Column(Float)
    qty_ubs = Column(Float)


class IndexReturn(Base):
    __tablename__ = 'index_return'
    id = Column(Integer, primary_key=True)
    entry_date = Column(Date, nullable=False)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    product = relationship("Product")
    perf_1d = Column(Float)
    perf_1m = Column(Float)
    perf_3m = Column(Float)
    perf_6m = Column(Float)
    perf_1y = Column(Float)
    perf_2y = Column(Float)
    perf_3y = Column(Float)


class AnalystPerf(Base):
    __tablename__ = 'analyst_perf'
    id = Column(Integer, primary_key=True)
    last_date = Column(Date, nullable=False)
    entry_date = Column(Date, nullable=False)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    product = relationship("Product")
    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User")
    alpha_point = Column(Float)
    relative_point = Column(Float)
    last_perf = Column(Float)
    current_size = Column(Float)
    daily_size = Column(Float)
    target_size = Column(Float)
    is_historic = Column(Boolean)
    is_top_pick = Column(Boolean)


class AnalystSelection(Base):
    __tablename__ = 'analyst_selection'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User")
    ananda_sector_id = Column(Integer, ForeignKey("ananda_sector.id"), nullable=False)
    size = Column(Integer)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    side = Column(String(1), nullable=False)
    conviction = Column(Integer)
    reason = Column(String(500), nullable=False)
    is_historic = Column(Boolean, default=False)
    previous = Column(String(100))
    is_top_pick = Column(Boolean, default=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), unique=True, nullable=False)
    last_name = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)


class ProductBetaOverride(Base):
    __tablename__ = 'product_beta_override'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    beta = Column(Float)


class ProductAlphaTiming(Base):
    __tablename__ = 'product_alpha_timing'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product")
    entry_date = Column(Date, nullable=False)
    timing_type = Column(String(20))
    alpha_usd = Column(Float)


class TradeFx(Base):
    __tablename__ = 'trade_fx'
    id = Column(Integer, primary_key=True)
    trade_date = Column(Date)
    product_name = Column(String(20))
    asset_type = Column(String(20))
    side = Column(String(20))
    quantity1 = Column(Float)
    cncy_id1 = Column(ForeignKey("currency.id"))
    currency1 = relationship("Currency", foreign_keys=[cncy_id1])
    quantity2 = Column(Float)
    cncy_id2 = Column(ForeignKey("currency.id"))
    currency2 = relationship("Currency", foreign_keys=[cncy_id2])
    rate = Column(String(45))
    settlement = Column(String(45))
    expiration = Column(String(45))


class PositionNew(Base):
    __tablename__ = 'position_new'
    id = Column(Integer, primary_key=True)
    entry_date = Column(Date)
    product_id = Column(ForeignKey("product.id"))
    product = relationship(Product)
    alpha_bp_1d = Column(Float)
    alpha_bp_3d = Column(Float)
    alpha_bp_1w = Column(Float)
    alpha_bp_4w = Column(Float)
    alpha_bp_3m = Column(Float)
    alpha_bp_6m = Column(Float)
    alpha_usd_1d = Column(Float)
    alpha_usd_3d = Column(Float)
    alpha_usd_1w = Column(Float)
    alpha_usd_4w = Column(Float)
    alpha_usd_3m = Column(Float)
    alpha_usd_6m = Column(Float)
    first_time = Column(Boolean)
    notional_usd = Column(Float)

class AlphaSummary(Base):
    __tablename__ = 'alpha_summary'
    id = Column(Integer, primary_key=True)
    entry_date = Column(Date)
    parent_fund_id = Column(ForeignKey("parent_fund.id"))
    parent_fund = relationship("ParentFund")
    long_usd = Column(Float)
    long_amer_usd = Column(Float)
    long_emea_usd = Column(Float)
    alpha_bp = Column(Float)
    alpha_amer_bp = Column(Float)
    alpha_emea_bp = Column(Float)
    alpha_long_bp = Column(Float)
    alpha_short_bp = Column(Float)


class AnalystAlert(Base):
    __tablename__ = 'analyst_alert'
    id = Column(Integer, primary_key=True)
    product_id1 = Column(ForeignKey("product.id"), nullable=False)
    product1 = relationship("Product", foreign_keys=[product_id1])
    product_id2 = Column(ForeignKey("product.id"), nullable=False)
    product2 = relationship("Product", foreign_keys=[product_id2])
    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User")
    entry_date = Column(DateTime, default=datetime.now)
    limit1 = Column(Float)
    limit2 = Column(Float)
    start_date = Column(Date)
    final_date = Column(Date)
    final_perf = Column(Float)


class NameValue(Base):
    __tablename__ = 'name_value'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    my_value = Column(String(45))


class Factor(Base):
    __tablename__ = 'factor'
    id = Column(Integer, primary_key=True)
    long_name = Column(String(45))
    short_name = Column(String(45))
    style = Column(String(45))
    source = Column(String(45))
    description = Column(String(45))
    norm_calculation = Column(String(45))
    min_value = Column(Float)
    max_value = Column(Float)


class FactorMarketData(Base):
    __tablename__ = 'factor_market_data'
    id = Column(Integer, primary_key=True)
    entry_date = Column(Date)
    ticker = Column(String(45))
    factor_id = Column(Integer, ForeignKey("factor.id"), nullable=False)
    factor = relationship("Factor")
    index = Column(String(45))
    raw_value = Column(Float)
    linear_value = Column(Float)
    norm_value = Column(Float)
    quintile = Column(Integer)


class FactorPosition(Base):
    __tablename__ = 'factor_position'
    id = Column(Integer, primary_key=True)
    entry_date = Column(Date)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product")
    factor_id = Column(Integer, ForeignKey("factor.id"), nullable=False)
    factor = relationship("Factor")
    notional_usd = Column(Float)
    raw_value = Column(Float)
    linear_value = Column(Float)
    norm_value = Column(Float)
    quintile = Column(Integer)
    parent_fund_id = Column(ForeignKey("parent_fund.id"))
    parent_fund = relationship("ParentFund")


def copy_trade(trade):
    amended_trade = Trade(
        order_number=trade.order_number,
        trade_date=trade.trade_date,
        settle_date=trade.settle_date,
        side=trade.side,
        is_short=trade.is_short,
        quantity=trade.quantity,
        ticker=trade.ticker,
        exec_price=trade.exec_price,
        broker=trade.broker,
        account=trade.account,
        cncy=trade.cncy,
        sec_name=trade.sec_name,
        sedol=trade.sedol,
        isin=trade.isin,
        cusip=trade.cusip,
        bbg_type=trade.bbg_type,
        is_cfd=trade.is_cfd,
        origin=trade.origin,
        created_by=trade.created_by,
        product_id=trade.product_id,
        long_future_name=trade.long_future_name,
        parent_fund_id=trade.parent_fund_id,
        parent_broker_id=trade.parent_broker_id,
        fx_rate=trade.fx_rate
    )
    return amended_trade
