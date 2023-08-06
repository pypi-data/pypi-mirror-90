from .fund_derived_factors import *
from ...data.fund.derived.derived_data_helper import normalize, score_rescale

class ScoreDataPrepare():

    def fund_ablity_prepare(self, factor_list):
        self.factor_list = factor_list
        dt = datetime.date(2012,1,1)
        self.factor_alive = FundAlive().get().loc[dt:]
        result = []
        for fac_name in self.factor_list:
            fac = eval(fac_name)().get()
            fac = fac[fac.index > dt]
            columns = fac.columns.intersection(self.factor_alive.columns).tolist()
            fac = pd.DataFrame(fac[columns].values * self.factor_alive[columns].values, columns=columns, index=self.factor_alive.index)
            fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
            result.append(fac)
            del fac
            del eval(fac_name)._instances[eval(fac_name)]
        self._factor = pd.concat(result, axis=1).stack()
        self._factor = self._factor.reset_index().dropna(subset=self.factor_list, how='all')
        self.fund_info = FundInfo().get()
        self.fund_type = ['stock','bond','index','QDII','mmf']
        self.wind_class_type = self.fund_info.set_index('fund_id')['wind_class_2']
        self._factor = self._factor.rename(columns={'level_1':'fund_id'})
        self._factor.loc[:,'fund_type'] = self._factor.fund_id.map(lambda x : self.WIND_TYPE_DICT[self.wind_class_type[x]])
        self._factor = self._factor.set_index('datetime')

    def manager_score_to_fund_prepare(self):
        self.total_score = MngScoreV1().get().reset_index()
        self.fund_manager_info = FundManagerInfo().get().set_index('fund_id')[['mng_id','start_date','end_date']]
        self.fund_nav = FundNavDaily().get()
        self.fund_info = FundInfo().get()
        type_list = ['stock','bond','index','QDII','mmf']
        self.manager_score = {}
        for type_i in type_list:
            _df = self.total_score[self.total_score['fund_type'] == type_i].reset_index().rename(columns={'index':'datetime'})
            _df = _df.pivot_table(index='datetime',columns='mng_id',values='mng_score')
            self.manager_score[type_i] = _df
        self.date_index = self.manager_score['stock'].index
        self.wind_class_dict = self.fund_info.set_index('fund_id').to_dict()['wind_class_2']

    def manager_score_data_prepare(self):
        dt = datetime.date(2012,1,1)
        self.factor_list = [    'MngAnnualRetDailyHistory', 
                                'MngTotalRetDailyHistory',
                                'MngMddDailyHistory',
                                'MngAnnualVolDailyHistory',
                                'MngDownsideStdDailyHistory',
                                'MngFundTypeTradingDays',
                                'MngFundSize',
                                'MngClAlphaWeeklyHistory',
                                'MngClBetaWeeklyHistory',
                            ]
        result = []
        for fac_name in self.factor_list:
            fac = eval(fac_name)().get()
            fac = fac[fac.index > dt]
            fac.columns = pd.MultiIndex.from_product([[fac_name], fac.columns])
            result.append(fac)
            del fac
            del eval(fac_name)._instances[eval(fac_name)]
        self._factor = pd.concat(result, axis=1).stack()
        self._factor = self._factor.reset_index().dropna(subset=self.factor_list, how='all').rename(columns={'level_1':'mng_id'})
        self._factor.loc[:,'fund_type'] = self._factor.mng_id.map(lambda x: x.split('_')[0])
        self._factor = self._factor.set_index(['datetime','fund_type'])
        self.fund_type = ['stock','bond','index','QDII','mmf']
            
    def score_rescale(self, df):
        return df.rank(pct=True) * 100

    def process_score(self, df):
        df = df.reset_index().set_index('fund_id').drop(columns=['fund_type'])
        return df.rank(pct=True) * 100

    def ability_calc(self):
        date_list = sorted(self._factor.index.unique().tolist())
        res = []
        lens_dt = len(date_list)
        _t0 = time.time()
        for dt in date_list:
            df_dt = self._factor.loc[dt].set_index('fund_type').copy()
            for fund_type in self.fund_type:
                try:
                    df_dt_fund_type = df_dt.loc[fund_type]
                except:
                    continue
                res.append(self.calc_fund(df_dt_fund_type, fund_type, dt))
            dt_idx = date_list.index(dt)
            if dt_idx % 100 == 0:
                _t1 = time.time()
                print(f' dt {dt} idx {dt_idx} total {lens_dt} cost {round(_t1 - _t0)}')
                _t0 = time.time()
        res = [i for i in res if i is not None]
        self._factor = pd.concat(res, axis=0)
        self._factor = self._factor.reset_index().pivot_table(index='datetime',values='fund_score',columns='fund_id')

    def score_fund(self, df, fund_type):
        return pd.DataFrame()

    def calc_fund(self, df, fund_type, dt):
        df = self.process_score(df)
        if df is None:
            return None
        df = self.score_fund(df, fund_type)
        if df is None:
            return None
        df.loc[:,'fund_type'] = fund_type
        df.loc[:,'datetime'] = dt
        return df.dropna(subset=['fund_score'])

class MngScoreV1(Factor, ScoreDataPrepare):
    # 雷达图基金评价 历史业绩为重

    def __init__(self):
        super().__init__(f_name='MngScoreV1', f_type=FundFactorType.DERIVED, f_level='score')

    def calc_mng(self, df, fund_type):
        if fund_type == 'stock':
            return self.score_mng_stock(df)
        if fund_type == 'bond':
            return self.score_mng_bond(df)
        if fund_type == 'index':
            return self.score_mng_index(df)
        if fund_type == 'QDII':
            return self.score_mng_qdii(df)
        if fund_type == 'mmf':
            return self.score_mng_mmf(df)
        
    def score_mng_stock(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale(0.4*score_rescale(df['MngAnnualRetDailyHistory']) +0.6*score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.3 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.3 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_select_time'] =  score_rescale(normalize(df['MngClAlphaWeeklyHistory']))
        df.loc[:,'mng_select_stock'] = score_rescale(normalize(df['MngClBetaWeeklyHistory']) )
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_risk_ability'] + df.loc[:,'mng_select_time'] + df.loc[:,'mng_select_stock'] + 1.5 * df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_select_time','mng_select_stock','mng_experience','mng_score']]

    def score_mng_bond(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale( 0.8 * score_rescale(df['MngAnnualRetDailyHistory']) + 0.2 * score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.1 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.5 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_select_time'] =  score_rescale(normalize(df['MngClAlphaWeeklyHistory']))
        df.loc[:,'mng_select_stock'] = score_rescale(normalize(df['MngClBetaWeeklyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(1.2 * df.loc[:,'mng_ret_ability'] +  df.loc[:,'mng_risk_ability'] + df.loc[:,'mng_select_time'] + df.loc[:,'mng_select_stock'] + 1.5 * df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_select_time','mng_select_stock','mng_experience','mng_score']]

    def score_mng_index(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale( 0.4 * score_rescale(df['MngAnnualRetDailyHistory']) + 0.6 * score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.3 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.3 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.4 *  score_rescale(df['MngFundTypeTradingDays']) + 0.6 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_risk_ability'] + 2 * df.loc[:,'mng_experience'] )
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_experience','mng_score']]

    def score_mng_qdii(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale( 0.4 * score_rescale(df['MngAnnualRetDailyHistory']) + 0.6 * score_rescale(df['MngTotalRetDailyHistory']))
        df.loc[:,'mng_risk_ability'] = score_rescale(0.3 * score_rescale(-df['MngMddDailyHistory']) + 0.4 * score_rescale(-df['MngAnnualVolDailyHistory']) + 0.3 * score_rescale(-df['MngDownsideStdDailyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_risk_ability'] + 1.5 * df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_risk_ability','mng_experience','mng_score']]

    def score_mng_mmf(self, df):
        df.loc[:,'mng_ret_ability'] = score_rescale(normalize(df['MngAnnualRetDailyHistory']))
        df.loc[:,'mng_experience'] = score_rescale( 0.8 *  score_rescale(df['MngFundTypeTradingDays']) + 0.2 * score_rescale(df['MngFundSize']))
        df.loc[:,'mng_score'] = score_rescale(df.loc[:,'mng_ret_ability'] + df.loc[:,'mng_experience'])
        return df[['mng_id','mng_ret_ability','mng_experience','mng_score']]

    def calc(self):
        self.manager_score_data_prepare()
        date_list = sorted(self._factor.index.get_level_values(0).unique().tolist())
        result = []
        _t0 = time.time()
        for dt in date_list:
            #df_dt = self._factor.loc[dt]
            for fund_type in self.fund_type:
                df_i = self._factor.loc[dt,fund_type].copy()
                df_i = self.calc_mng(df_i, fund_type)
                result.append(df_i)
            dt_idx = date_list.index(dt)
            if dt_idx % 100 == 0:
                print(f'dt {dt} idx {dt_idx}')

        _t1 = time.time()
        print(_t1 - _t0)
        self._factor = pd.concat(result).dropna(subset=['mng_score'])
        self._factor = self._factor.reset_index()

    def append_update(self):
        self._exsited_factor = self.get()
        last_date = pd.to_datetime(self._exsited_factor.index[-1]).date()
        self.manager_score_data_prepare()
        date_list = sorted(self._factor.index.get_level_values(0).unique().tolist())
        date_list = [pd.to_datetime(i).date() for i in date_list]
        date_list = [i for i in date_list if i > last_date]
        result = []
        if len(date_list)  == 0:
            return True
        for dt in date_list:
            for fund_type in self.fund_type:
                df_i = self._factor.loc[dt,fund_type].copy()
                df_i = self.calc_mng(df_i, fund_type)
                result.append(df_i)
            dt_idx = date_list.index(dt)
        if len(result) == 0:
            return True
        self._factor = pd.concat(result).dropna(subset=['mng_score'])
        self._factor = self._factor.reset_index().set_index('datetime')
        self._factor = self._exsited_factor.append(self._factor)
        td = self._factor.index.tolist()
        td = pd.to_datetime(td)
        td = [i.date() for i in td] 
        self._factor.index = td
        return self.save()

class FundMngScoreV1(Factor, ScoreDataPrepare):

    def __init__(self):
        super().__init__(f_name='FundMngScoreV1', f_type=FundFactorType.DERIVED, f_level='score')

    def loop_item(self, fund_id):
        wind_type = self.wind_class_dict.get(fund_id)
        fund_type = self.WIND_TYPE_DICT.get(wind_type, 'stock')
        if fund_id not in self.fund_manager_info.index:
            return None
        single_fund_info = self.fund_manager_info.loc[[fund_id]]
        result = []
        for row in single_fund_info.itertuples(index=False):
            if row.mng_id not in self.manager_score[fund_type]:
                continue
            manager_score = pd.Series((self.date_index >= row.start_date) & (self.date_index <= row.end_date), index=self.date_index,name=row.mng_id) * 1
            manager_score = manager_score * self.manager_score[fund_type][row.mng_id]
            result.append(manager_score)
        if result  == []:
            return None
        fund_manager_score_i = pd.concat(result,axis=1).max(axis=1)
        fund_manager_score_i.name = fund_id
        return fund_manager_score_i

    def calc(self):
        self.manager_score_to_fund_prepare() 
        score_result_total = []
        fund_list = self.fund_nav.columns.tolist()
        _t0 = time.time()
        for fund_id in fund_list:
            res_i = self.loop_item(fund_id)
            if res_i is not None:
                score_result_total.append(res_i)
            idx = fund_list.index(fund_id)
            if idx % 1000 == 0:
                _t1 = time.time()
                #print(f'fund_id {fund_id} {idx} {len(fund_list)} cost { round(_t1 - _t0,2)}')
                _t0 = time.time()
        self._factor = pd.concat(score_result_total, axis=1)
        self.data = None

class RetAbilityFundScore(Factor, ScoreDataPrepare):

    def __init__(self):
        super().__init__(f_name='RetAbilityFundScore', f_type=FundFactorType.DERIVED, f_level='score')

    def score_fund(self, df, fund_type):
        if fund_type in ['stock','index','QDII']:
            df.loc[:,'fund_score'] = self.score_rescale(0.4 * df.AnnualRetDailyHistory + 0.6 * df.TotalRetDailyHistory)
        elif fund_type in ['bond']:
            df.loc[:,'fund_score'] = self.score_rescale(0.8 * df.AnnualRetDailyHistory + 0.2 * df.TotalRetDailyHistory)
        elif fund_type in ['mmf']:
            df.loc[:,'fund_score'] = self.score_rescale(df.RecentMonthRet)
        return df[['fund_score']]

    def calc(self):
        fund_list = ['AnnualRetDailyHistory', 
                     'TotalRetDailyHistory',
                     'RecentMonthRet']
        
        self.fund_ablity_prepare(fund_list)
        self.ability_calc()

class RiskAbilityFundScore(Factor, ScoreDataPrepare):

    def __init__(self):
        super().__init__(f_name='RiskAbilityFundScore', f_type=FundFactorType.DERIVED, f_level='score')

    def score_fund(self, df, fund_type):
        if fund_type in ['stock','index','QDII','bond']:
            df.loc[:,'fund_score'] = self.score_rescale(0.3 * df.MddDailyHistory + 0.4 * df.AnnualVolDailyHistory + 0.3 * df.DownsideStdDailyHistory)
        elif fund_type in ['mmf']:
            df.loc[:,'fund_score'] = self.score_rescale(0.5 * df.FundPersonalHold + 0.5 * df.FundSizeCombine)
        return df[['fund_score']]

    def calc(self):
        fund_list = ['MddDailyHistory', 
                     'AnnualVolDailyHistory',
                     'DownsideStdDailyHistory',
                     'FundPersonalHold',
                     'FundSizeCombine']
        self.fund_ablity_prepare(fund_list)
        self.ability_calc()

class StableAbility(Factor, ScoreDataPrepare):

    def __init__(self):
        super().__init__(f_name='StableAbility', f_type=FundFactorType.DERIVED, f_level='score')

    def score_fund(self, df, fund_type):
        if fund_type in ['stock','index','QDII','bond']:
            df.loc[:,'fund_score'] = self.score_rescale(0.4 * df.TradeYear + 0.4 * df.ContinueRegValue + 0.2 * df.FundSizeCombine)
        else:
            return None
        return df[['fund_score']]

    def calc(self):
        fund_list = ['TradeYear', 
                     'ContinueRegValue',
                     'FundSizeCombine']
        
        self.fund_ablity_prepare(fund_list)
        self.ability_calc()

class SelectTimeAbility(Factor, ScoreDataPrepare):

    def __init__(self):
        super().__init__(f_name='SelectTimeAbility', f_type=FundFactorType.DERIVED, f_level='score')

    def score_fund(self, df, fund_type):
        if fund_type in ['stock','QDII']:
            df.loc[:,'fund_score'] = self.score_rescale(df.FundClBetaHistoryWeekly)
        else:
            return None
        return df[['fund_score']]

    def calc(self):
        fund_list = ['FundClBetaHistoryWeekly']
        self.fund_ablity_prepare(fund_list)
        self.ability_calc()

class SelectStockAbility(Factor, ScoreDataPrepare):

    def __init__(self):
        super().__init__(f_name='SelectStockAbility', f_type=FundFactorType.DERIVED, f_level='score')

    def score_fund(self, df, fund_type):
        if fund_type in ['stock','QDII']:
            df.loc[:,'fund_score'] = self.score_rescale(df.FundClAlphaHistoryWeekly)
        else:
            return None
        return df[['fund_score']]

    def calc(self):
        fund_list = ['FundClAlphaHistoryWeekly']
        self.fund_ablity_prepare(fund_list)
        self.ability_calc()

class UpdateDerivedScoreStart:
    pass
