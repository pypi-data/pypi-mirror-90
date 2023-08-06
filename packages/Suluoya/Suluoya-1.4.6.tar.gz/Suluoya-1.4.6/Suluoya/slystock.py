class stock(object):   
    def __init__(self):
        pass
    def combine(self,lists=['A','B','C']):
        from itertools import combinations
        results = []
        for j in range(1,len(lists)+1):        
            for i in combinations(lists,j):
                result = []
                result.append(list(i))
                result.append(j)
                results.append(result)
        return pd.DataFrame(results,columns=['group','amout'])
    def get_stock(self,code="sh.600000",start_date='2020-07-01', end_date='2020-12-31',
                    frequency='d',adjustflag="3",
                    targets='date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST'):
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        import baostock as bs
        from pandas import DataFrame
        lg = bs.login()
        rs = bs.query_history_k_data_plus(code,targets,
            start_date=start_date, end_date=end_date,
            frequency=frequency, adjustflag=adjustflag)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = DataFrame(data_list, columns=rs.fields)
        return result
    def get_code(self,code='',name='',date=''):
        import baostock as bs
        from pandas import DataFrame
        from pandas import merge
        lg = bs.login()
        rs = bs.query_stock_basic(code_name=name,code=code)
        industry_list = []
        while (rs.error_code == '0') & rs.next():
            industry_list.append(rs.get_row_data())
        basic_info = DataFrame(industry_list, columns=rs.fields)
        if name!='' and code=='':
            code=basic_info['code'][0]
        rs = bs.query_stock_industry(code=code,date=date)
        industry_list = []
        while (rs.error_code == '0') & rs.next():
            industry_list.append(rs.get_row_data())
        industry_info = DataFrame(industry_list, columns=rs.fields)
        df=merge(basic_info,industry_info,how='outer')
        return df
        bs.logout()

