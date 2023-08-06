import pandas as pd
from ...stock.factor.fund_derived_factors import *
from ...stock.factor.fund_derived_score import *

BK_BACKTEST = [FundMngScoreV1,RetAbilityFundScore,RiskAbilityFundScore,StableAbility,SelectTimeAbility,
                SelectStockAbility,WinRateMonthlyTop50,WinRateMonthlyTop75]

def combine_factor():
    result = []
    factor_list = BK_BACKTEST
    fac_name_list = [i().name for i in BK_BACKTEST]
    for fac_i in factor_list:
        fac_class = fac_i()
        fac = fac_class.get()
        fac_name = fac_class.name
        fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
        result.append(fac)
        fac_class.clear(recursive=True)
    df = pd.concat(result, axis=1).stack()
    df = df.reset_index().dropna(subset=fac_name_list, how='any')
    df = df.rename(columns={'level_0':'datetime','level_1':'fund_id'})
    return df
