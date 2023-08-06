import talib

from pyalgotrading.constants import *
from pyalgotrading.strategy.strategy_base import StrategyBase


class StrategyStochasticCrossoverCoverOrder(StrategyBase):
    class ActionConstants:
        NO_ACTION = 0
        ENTRY_BUY_OR_EXIT_SELL = 1
        ENTRY_SELL_OR_EXIT_BUY = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fastk_period = self.strategy_parameters['FASTK_PERIOD']
        self.slowk_period = self.strategy_parameters['SLOWK_PERIOD']
        self.slowd_period = self.strategy_parameters['SLOWD_PERIOD']
        self.stoploss = self.strategy_parameters['STOPLOSS_TRIGGER']

        assert (0 < self.fastk_period == int(self.fastk_period)), f"Strategy parameter FASTK_PERIOD should be a positive integer. Received: {self.fastk_period}"
        assert (0 < self.slowk_period == int(self.slowk_period)), f"Strategy parameter SLOWK_PERIOD should be a positive integer. Received: {self.slowk_period}"
        assert (0 < self.slowd_period == int(self.slowd_period)), f"Strategy parameter SLOWD_PERIOD should be a positive integer. Received: {self.slowd_period}"
        assert (0 < self.stoploss < 1), f"Strategy parameter STOPLOSS_TRIGGER should be a positive fraction between 0 and 1. Received: {self.stoploss}"

        self.main_order = None

    def initialize(self):
        self.main_order = {}

    @staticmethod
    def name():
        return 'Stochastic Crossover Cover Order Strategy'

    @staticmethod
    def versions_supported():
        return [AlgoBullsEngineVersion.VERSION_3_2_0, AlgoBullsEngineVersion.VERSION_3_3_0]

    def get_decision(self, instrument):
        hist_data = self.get_historical_data(instrument)
        slowk, slowd = talib.STOCH(hist_data['high'], hist_data['low'], hist_data['close'], fastk_period=self.fastk_period,
                                   slowk_period=self.slowk_period, slowk_matype=0, slowd_period=self.slowd_period, slowd_matype=0)
        stochastic_crossover_value = self.utils.crossover(slowk, slowd)
        if stochastic_crossover_value == 1:
            action = self.ActionConstants.ENTRY_BUY_OR_EXIT_SELL
        elif stochastic_crossover_value == -1:
            action = self.ActionConstants.ENTRY_SELL_OR_EXIT_BUY
        else:
            action = self.ActionConstants.NO_ACTION
        return action

    def strategy_select_instruments_for_entry(self, candle, instruments_bucket):

        selected_instruments_bucket = []
        sideband_info_bucket = []

        for instrument in instruments_bucket:
            action = self.get_decision(instrument)
            if self.main_order.get(instrument) is None:
                if action is self.ActionConstants.ENTRY_BUY_OR_EXIT_SELL:
                    selected_instruments_bucket.append(instrument)
                    sideband_info_bucket.append({'action': 'BUY'})
                elif action is self.ActionConstants.ENTRY_SELL_OR_EXIT_BUY:
                    if self.strategy_mode is StrategyMode.INTRADAY:
                        selected_instruments_bucket.append(instrument)
                        sideband_info_bucket.append({'action': 'SELL'})

        return selected_instruments_bucket, sideband_info_bucket

    def strategy_enter_position(self, candle, instrument, sideband_info):
        if sideband_info['action'] == 'BUY':
            qty = self.number_of_lots * instrument.lot_size
            ltp = self.broker.get_ltp(instrument)
            self.main_order[instrument] = self.broker.BuyOrderCover(instrument=instrument,
                                                                    order_code=BrokerOrderCodeConstants.INTRADAY,
                                                                    order_variety=BrokerOrderVarietyConstants.MARKET,
                                                                    quantity=qty,
                                                                    price=ltp,
                                                                    trigger_price=ltp - (ltp * self.stoploss))
        elif sideband_info['action'] == 'SELL':
            qty = self.number_of_lots * instrument.lot_size
            ltp = self.broker.get_ltp(instrument)
            self.main_order[instrument] = self.broker.SellOrderCover(instrument=instrument,
                                                                     order_code=BrokerOrderCodeConstants.INTRADAY,
                                                                     order_variety=BrokerOrderVarietyConstants.MARKET,
                                                                     quantity=qty,
                                                                     price=ltp,
                                                                     trigger_price=ltp + (ltp * self.stoploss))
        else:
            raise SystemExit(f'Invalid sideband info value {sideband_info}')

        return self.main_order[instrument]

    def strategy_select_instruments_for_exit(self, candle, instruments_bucket):
        selected_instruments_bucket = []
        sideband_info_bucket = []

        for instrument in instruments_bucket:
            if self.main_order.get(instrument) is not None:
                action = self.get_decision(instrument)
                if ((self.main_order[instrument].order_transaction_type is BrokerOrderTransactionTypeConstants.BUY and
                     action is self.ActionConstants.ENTRY_SELL_OR_EXIT_BUY) or
                        (self.main_order[instrument].order_transaction_type is BrokerOrderTransactionTypeConstants.SELL and
                         action is self.ActionConstants.ENTRY_BUY_OR_EXIT_SELL)):
                    selected_instruments_bucket.append(instrument)
                    sideband_info_bucket.append({'action': 'EXIT'})
        return selected_instruments_bucket, sideband_info_bucket

    def strategy_exit_position(self, candle, instrument, sideband_info):
        if sideband_info['action'] == 'EXIT':
            self.main_order[instrument].exit_position()
            self.main_order[instrument] = None
            return True
        return False
