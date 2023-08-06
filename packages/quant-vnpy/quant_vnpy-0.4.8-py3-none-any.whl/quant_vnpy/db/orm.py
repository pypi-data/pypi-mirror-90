"""
@author  : MG
@Time    : 2020/11/24 11:05
@File    : object.py
@contact : mmmaaaggg@163.com
@desc    : 用于创建数据库表结构
"""
import enum
import typing
from collections import defaultdict
from datetime import datetime, date

import pandas as pd
from peewee import (
    CharField,
    SmallIntegerField,
    DateField,
    DateTimeField,
    DoubleField,
    Model,
    CompositeKey,
    fn,
)
# Peewee provides an alternate database implementation
# for using the mysql-connector driver.
# The implementation can be found in playhouse.mysql_ext.
from playhouse.mysql_ext import MySQLConnectorDatabase
from vnpy.trader.constant import Offset
from vnpy.trader.setting import get_settings

from quant_vnpy.config import logging

logger = logging.getLogger()


class StrategyStatusEnum(enum.IntEnum):
    Created = 0
    Initialized = 1
    RunPending = 2
    Running = 3
    StopPending = 4
    Stopped = 5


def init_db():
    settings = get_settings("database.")
    keys = {"database", "user", "password", "host", "port"}
    settings = {k: v for k, v in settings.items() if k in keys}
    db = MySQLConnectorDatabase(**settings)
    return db


_USER_NAME: typing.Optional[str] = None
_BROKER_ID: typing.Optional[str] = None


def get_account() -> typing.Tuple[str, str]:
    global _USER_NAME, _BROKER_ID
    if _USER_NAME is None or _BROKER_ID is None:
        from vnpy.trader.utility import load_json
        filename: str = f"connect_ctp.json"
        connect_dic = load_json(filename)
        if len(connect_dic) == 0:
            _USER_NAME, _BROKER_ID = "test user", "0000"
        else:
            _USER_NAME = connect_dic["用户名"]
            _BROKER_ID = connect_dic["经纪商代码"]

        logger.info(f"user name='{_USER_NAME}', broker_id='{_BROKER_ID}'")

    return _USER_NAME, _BROKER_ID


def set_account(user_name, broker_id):
    global _USER_NAME, _BROKER_ID
    _USER_NAME, _BROKER_ID = user_name, broker_id


def set_account_backtest():
    user_name, broker_id = "test user", "0000"
    set_account(user_name, broker_id)


database = init_db()


class StrategyStatus(Model):
    """
    策略状态信息
    * strategy_name 策略名称
    * status 策略状态
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    status: int = SmallIntegerField()
    symbols: str = CharField(max_length=20)
    update_dt = DateTimeField()
    description: str = CharField()

    @staticmethod
    def is_table_exists():
        try:
            is_exists = StrategyStatus.table_exists()
            return is_exists
        except:
            return False
        finally:
            StrategyStatus._meta.database.close()

    @staticmethod
    def set_status(strategy_name, status: int):
        try:
            user_name, broker_id = get_account()
            ret_data = StrategyStatus.update(
                status=status, update_dt=datetime.now()
            ).where(
                StrategyStatus.user_name == user_name,
                StrategyStatus.broker_id == broker_id,
                StrategyStatus.strategy_name == strategy_name,
            ).execute()
            logger.debug("%s[%s] %s status=%d", user_name, broker_id, strategy_name, status)
        finally:
            StrategyStatus._meta.database.close()
        return ret_data

    @staticmethod
    def query_status(strategy_name) -> int:
        try:
            user_name, broker_id = get_account()
            ss: StrategyStatus = StrategyStatus.get_or_none(
                StrategyStatus.user_name == user_name,
                StrategyStatus.broker_id == broker_id,
                StrategyStatus.strategy_name == strategy_name,
            )
            if ss is None:
                status = -1
            else:
                status = ss.status

            logger.debug("%s[%s] %s status=%d", user_name, broker_id, strategy_name, status)
            return status
        finally:
            StrategyStatus._meta.database.close()

    @staticmethod
    def register_strategy(strategy_name, status: int, symbols: str):
        try:
            user_name, broker_id = get_account()
            ret_data = StrategyStatus.insert(
                user_name=user_name, broker_id=broker_id,
                strategy_name=strategy_name, status=status,
                symbols=symbols, update_dt=datetime.now()).on_conflict(
                preserve=[StrategyStatus.user_name, StrategyStatus.broker_id, StrategyStatus.strategy_name],
                update={StrategyStatus.status: status, StrategyStatus.update_dt: datetime.now()}
            ).execute()
            logger.debug("%s[%s] %s status=%d", user_name, broker_id, strategy_name, status)
            return ret_data
        finally:
            StrategyStatus._meta.database.close()

    @staticmethod
    def query_all():
        user_name, broker_id = get_account()
        try:
            ret_data = [_ for _ in StrategyStatus.select().where(
                StrategyStatus.user_name == user_name,
                StrategyStatus.broker_id == broker_id,
            ).execute()]
        finally:
            StrategyStatus._meta.database.close()

        return ret_data

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name')
        table_settings = "ENGINE = MEMORY"


class OrderDataModel(Model):
    """
    策略状态信息
    实际生产环境中 orderid 可以唯一确定
    但是，回测环境下，需要与策略名称，品种进行配合才行
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    orderid: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    order_type: str = CharField(max_length=20)
    direction: str = CharField(max_length=8)
    offset: str = CharField(max_length=8)
    price = DoubleField()
    volume = DoubleField()
    status: str = CharField(max_length=20)
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name', 'orderid', 'symbol')
        # indexes = ((("strategy_name", "symbol"), True),)

    @staticmethod
    def bulk_replace(data_dic_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in data_dic_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    OrderDataModel.replace(**data_dic).execute()

        finally:
            OrderDataModel._meta.database.close()


class TradeDataModel(Model):
    """
    策略状态信息
    实际生产环境中 tradeid 可以唯一确定
    但是，回测环境下，需要与策略名称，品种进行配合才行
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    tradeid: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    orderid: str = CharField()
    direction: str = CharField(max_length=8)
    offset: str = CharField(max_length=8)
    price = DoubleField()
    volume = DoubleField()
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name', 'tradeid', 'symbol')
        # indexes = ((("strategy_name", "symbol"), True),)

    @staticmethod
    def get_latest_open_trade_data():
        """
        获取各个策略最近的一笔开仓交易单
        """
        user_name, broker_id = get_account()
        sql_str = """select trades.* from trade_data_model trades inner join (
            select strategy_name, max(`datetime`) dt from trade_data_model 
            where user_name=%s and broker_id=%s and offset=%s
            group by strategy_name) latest
            on trades.strategy_name = latest.strategy_name
            and trades.`datetime` = latest.dt
            where user_name=%s and broker_id=%s and offset=%s
            """
        strategy_symbol_latest_open_trade_data_dic = defaultdict(dict)
        try:
            for trade_data in TradeDataModel.raw(
                    sql_str, user_name, broker_id, Offset.OPEN.value,
                    user_name, broker_id, Offset.OPEN.value, ).execute():
                strategy_symbol_latest_open_trade_data_dic[trade_data.strategy_name][trade_data.symbol] = trade_data
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_latest_open_trade_data_dic

    @staticmethod
    def query_latest_n_trade_date_list(latest_n) -> typing.List[date]:
        user_name, broker_id = get_account()
        sql_str = f"select distinct Date(`datetime`) from trade_data_model" \
                  f" where user_name=%s and broker_id=%s" \
                  f" order by Date(`datetime`) desc limit {latest_n}"
        trade_date_list = []
        try:
            for trade_date in database.execute_sql(sql_str, [user_name, broker_id]):
                trade_date_list.append(trade_date[0])
        finally:
            database.close()

        return trade_date_list

    @staticmethod
    def query_trade_data_by_strategy_since(
            strategy_name: str = None, trade_dt: datetime = None
    ) -> typing.Dict[str, list]:
        """
        :param strategy_name
        :param trade_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        user_name, broker_id = get_account()
        strategy_symbol_trade_data_list_dic = defaultdict(list)
        try:
            if trade_dt is None:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.symbol].append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name,
                        TradeDataModel.datetime > trade_dt
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.symbol].append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list_dic

    @staticmethod
    def query_trade_data_by_strategy_symbol_since(
            strategy_name: str, symbol: str, trade_dt: datetime = None
    ) -> list:
        """
        :param strategy_name
        :param trade_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        user_name, broker_id = get_account()
        strategy_symbol_trade_data_list = []
        try:
            if trade_dt is None:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name,
                        TradeDataModel.symbol == symbol,
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list.append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name,
                        TradeDataModel.symbol == symbol,
                        TradeDataModel.datetime > trade_dt
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list.append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list

    @staticmethod
    def query_trade_data_since(
            update_dt: datetime = None
    ) -> typing.Dict[str, typing.Dict[str, list]]:
        """
        :param update_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        user_name, broker_id = get_account()
        strategy_symbol_trade_data_list_dic = defaultdict(lambda: defaultdict(list))
        try:
            if update_dt is None:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.strategy_name][_.symbol].append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.datetime > update_dt
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.strategy_name][_.symbol].append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list_dic

    @staticmethod
    def bulk_replace(data_dic_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in data_dic_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    TradeDataModel.replace(**data_dic).execute()

        finally:
            TradeDataModel._meta.database.close()

    @staticmethod
    def clear_by_strategy_name(strategy_name):
        try:
            user_name, broker_id = get_account()
            TradeDataModel.delete().where(
                TradeDataModel.user_name == user_name,
                TradeDataModel.broker_id == broker_id,
                TradeDataModel.strategy_name == strategy_name).execute()
        finally:
            TradeDataModel._meta.database.close()


class LatestTickPriceModel(Model):
    """
    策略状态信息
    * symbol 产品名称
    """
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    price = DoubleField()
    volume = DoubleField()
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('symbol')
        table_settings = "ENGINE = MEMORY"

    @staticmethod
    def query_latest_price(symbol):
        """
        获取各个策略最近的一笔开仓交易单
        """
        try:
            data: LatestTickPriceModel = LatestTickPriceModel.get_or_none(LatestTickPriceModel.symbol == symbol)
        finally:
            LatestTickPriceModel._meta.database.close()

        return data

    @staticmethod
    def query_all_latest_price() -> dict:
        """
        获取各个策略最近的一笔开仓交易单
        """
        try:
            symbol_tick_dic: typing.Dict[str, LatestTickPriceModel] = {
                _.symbol: _ for _ in LatestTickPriceModel.select()}
        finally:
            LatestTickPriceModel._meta.database.close()

        return symbol_tick_dic


class PositionStatusModel(Model):
    """
    策略持仓信息
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    tradeid: str = CharField()
    strategy_name: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    trade_date = DateField()
    trade_dt = DateTimeField()
    direction: str = CharField(max_length=8)
    avg_price = DoubleField()  # 平均持仓成本
    latest_price = DoubleField()  # 最新价格
    volume = DoubleField()
    holding_gl = DoubleField()  # holding gain and loss 持仓盈亏
    offset_gl = DoubleField()  # offset gain and loss 平仓盈亏
    offset_daily_gl = DoubleField()  # daily offset gain and loss 平仓盈亏
    offset_acc_gl = DoubleField()  # accumulate offset gain and loss 平仓盈亏
    update_dt = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'tradeid', 'strategy_name', 'symbol')

    @staticmethod
    def query_latest_position_status() -> typing.Dict[str, dict]:
        """
        获取各个策略最近的一笔开仓交易单
        """
        user_name, broker_id = get_account()
        sql_str = """select pos.* from position_status_model pos inner join (
            select strategy_name, max(trade_dt) trade_dt from position_status_model 
            where user_name=%s and broker_id=%s
            group by strategy_name, symbol) latest
            on pos.strategy_name = latest.strategy_name
            and pos.trade_dt = latest.trade_dt
            where user_name=%s and broker_id=%s"""
        strategy_symbol_pos_status_dic = defaultdict(dict)
        try:
            for pos_status in PositionStatusModel.raw(
                    sql_str, user_name, broker_id, user_name, broker_id).execute():
                strategy_symbol_pos_status_dic[pos_status.strategy_name][pos_status.symbol] = pos_status
        finally:
            PositionStatusModel._meta.database.close()

        return strategy_symbol_pos_status_dic

    @staticmethod
    def bulk_replace(pos_status_new_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in pos_status_new_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    PositionStatusModel.replace(**data_dic).execute()

        finally:
            PositionStatusModel._meta.database.close()


class PositionDailyModel(Model):
    """
    策略持仓信息
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    trade_date = DateField()
    trade_dt = DateTimeField()
    direction: str = CharField(max_length=8)
    avg_price = DoubleField()  # 平均持仓成本
    latest_price = DoubleField()  # 最新价格
    volume = DoubleField()
    holding_gl = DoubleField()  # holding gain and loss 持仓盈亏
    offset_gl = DoubleField()  # offset gain and loss 平仓盈亏
    offset_daily_gl = DoubleField()  # daily offset gain and loss 平仓盈亏
    offset_acc_gl = DoubleField()  # accumulate offset gain and loss 平仓盈亏
    update_dt = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name', 'symbol', 'trade_date')

    @staticmethod
    def bulk_replace(position_daily_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in position_daily_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    PositionDailyModel.replace(**data_dic).execute()

        finally:
            PositionDailyModel._meta.database.close()

    @staticmethod
    def query_latest_position_daily() -> typing.Dict[str, dict]:
        """
        获取各个策略最近的一笔开仓交易单
        """
        user_name, broker_id = get_account()
        sql_str = """select pos.* from position_daily_model pos inner join (
            select strategy_name, max(trade_date) trade_date from position_daily_model 
            where user_name=%s and broker_id=%s
            group by strategy_name, symbol) latest
            on pos.strategy_name = latest.strategy_name
            and pos.trade_date = latest.trade_date
            where user_name=%s and broker_id=%s"""
        strategy_symbol_pos_daily_dic = defaultdict(dict)
        try:
            for pos_status in PositionDailyModel.raw(
                    sql_str, user_name, broker_id, user_name, broker_id).execute():
                strategy_symbol_pos_daily_dic[pos_status.strategy_name][pos_status.symbol] = pos_status
        finally:
            PositionDailyModel._meta.database.close()

        return strategy_symbol_pos_daily_dic


class TradeDateModel(Model):
    """
    策略状态信息
    * strategy_name 策略名称
    * status 策略状态
    """
    trade_date = DateField(primary_key=True)

    class Meta:
        database = database
        legacy_table_names = False
        table_settings = "ENGINE = MYISAM"

    @staticmethod
    def get_latest_trade_date():
        try:
            obj: TradeDateModel = TradeDateModel.select(fn.MAX(TradeDateModel.trade_date)).first()
        finally:
            TradeDateModel._meta.database.close()

        return None if obj.trade_date is None else obj.trade_date

    @staticmethod
    def bulk_replace(data_dic_list: typing.List[dict]):
        try:
            with database.atomic():
                for data_dic in data_dic_list:
                    TradeDateModel.replace(**data_dic).execute()

        finally:
            TradeDateModel._meta.database.close()

    @staticmethod
    def get_next_trade_date_dic() -> typing.Dict[date, date]:
        trade_date_df = pd.read_sql("SELECT * FROM trade_date_model order by trade_date", database)
        trade_date_df['trade_date_next'] = trade_date_df['trade_date'].shift(-1)
        next_trade_date_dic = trade_date_df.set_index('trade_date')['trade_date_next'].to_dict()
        return next_trade_date_dic


def init_models():
    # try:
    #     StrategyStatus.create_table()  # 创建表  # engine='MEMORY'
    # except peewee.OperationalError:
    #     logger.warning("StrategyStatus table already exists!")
    #
    # try:
    #     TradeDataModel.create_table()  # 创建表  # engine='MEMORY'
    # except peewee.OperationalError:
    #     logger.warning("TradeDataModel table already exists!")

    database.connect()
    database.create_tables([
        StrategyStatus, OrderDataModel, TradeDataModel,
        LatestTickPriceModel, PositionStatusModel, PositionDailyModel,
        TradeDateModel,
    ])


def _test_record_strategy_status():
    strategy_name = 'asdf11'
    user_name, broker_id = get_account()
    status = StrategyStatusEnum.Running
    StrategyStatus.register_strategy(strategy_name=strategy_name, status=status.value, symbols='rb2101.SHFE')
    ss: StrategyStatus = StrategyStatus.get_or_none(
        StrategyStatus.user_name == user_name, StrategyStatus.broker_id == broker_id,
        StrategyStatus.strategy_name == strategy_name)
    assert ss.status == status.value
    assert ss.description == ''
    StrategyStatus.set_status(strategy_name=strategy_name, status=status.value)
    ss: StrategyStatus = StrategyStatus.get_or_none(
        StrategyStatus.user_name == user_name, StrategyStatus.broker_id == broker_id,
        StrategyStatus.strategy_name == strategy_name)
    print(ss, ss.status)
    ss.status = StrategyStatusEnum.Stopped.value
    ss.update()
    ss._meta.database.close()
    print(ss, ss.status)


if __name__ == "__main__":
    init_models()
    # _test_record_strategy_status()
