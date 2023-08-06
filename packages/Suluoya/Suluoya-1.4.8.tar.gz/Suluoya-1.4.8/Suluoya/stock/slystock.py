class stock(object):   
    def __init__(self):
        pass
    def correlation(self,x,y):
        import numpy as np
        if type(x)==list:
            x=np.array(x)
        if type(y)==list:
            y=np.array(y)
        return (np.dot([xi - np.mean(x) for xi in x],[yi - np.mean(y) for yi in y])/(len(x)-1))/((x.std())*(y.std()))
    def combine(self,lists=['A','B','C']):
        from itertools import combinations
        from pandas import DataFrame
        results = []
        for j in range(1,len(lists)+1):        
            for i in combinations(lists,j):
                result = []
                result.append(list(i))
                result.append(j)
                results.append(result)
        return DataFrame(results,columns=['group','amount'])
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
        bs.logout()
        return result
    def get_code(self,name='',code='',date=''):
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
        bs.logout()
        return df
    def sharp(self,df,no_risk_rate=0.45/5200):
        import numpy as np
        from pandas import DataFrame
        df=df.astype('float')
        info=df.describe().loc[['mean','std'],]
        columns=df.columns
        lists=[]
        for i in range(0,len(columns)):
            for j in columns[i:]:
                if columns[i] != j:
                    lists.append([columns[i],j])
        for i in lists:
            x=df[i[0]]
            y=df[i[1]]
            a=(np.dot([xi - np.mean(x) for xi in x],[yi - np.mean(y) for yi in y])/(len(x)-1))/((x.std())*(y.std()))
        for i in lists:
            i.append(a)
        weights=np.random.dirichlet(np.ones(len(list(df.columns))),size=1)[0]
        rand={}
        for i in range(0,len(list(df.columns))):
            rand[columns[i]]=weights[i]
        #rate
        rate=0
        for i,j in rand.items():
            rate+=np.array(j*info.loc[['mean'],[i]])[0][0]
        #风险
        risk=0
        for i,j in rand.items():
            risk+=(j**2)*((np.array(info.loc[['std'],[i]])[0][0])**2)
        for i in lists:
            std1=np.array(info.loc[['std'],[i[0]]])[0][0]
            std2=np.array(info.loc[['std'],[i[1]]])[0][0]
            gama=i[2]
            w1=rand[i[0]]
            w2=rand[i[1]]
            risk+=std1*std2*gama*w1*w2
        #夏普
        sharp=(rate-no_risk_rate)/risk
        df=DataFrame([[rate,risk,sharp,rand]],columns=['rate','risk','sharp','weights'])
        df=df.set_index('weights')
        return df
    def Markowit(self,names,number=500,start_date='2018-11-01', end_date='2020-12-31',frequency='w',save=True):
        from pandas import DataFrame
        from tqdm import tqdm
        a=stock()
        zuhe=a.combine(names)
        code=[]
        y=[]
        for i in tqdm(names):
            x=a.get_code(name=i)
            code.append(x[['code','code_name']])
            y.append(x)
        from pandas import concat
        df1=concat(y)
        df=DataFrame()
        for i in tqdm(code):
            name=i['code_name'][0]
            df[name]=a.get_stock(i['code'][0],start_date=start_date, end_date=end_date,
                            frequency=frequency,adjustflag="3",
                            targets='pctChg')['pctChg']
        zuhe=zuhe[zuhe['amount']>1]
        import os 
        from tqdm import trange
        try:
            os.makedirs('./all')
            os.makedirs('./info')
        except:
            pass
        df1=df1.set_index('code_name')
        df1.to_csv(r'info/info.csv',encoding='utf-8')
        df.to_csv(r'info/data.csv',encoding='utf-8',index=False)
        for i,j in zuhe.iterrows():
            result=[]
            for k in trange(number):
                result.append(a.sharp(df[j[0]]))
                from pandas import concat
                all=concat(result)
                all.to_csv(r'all/{}.csv'.format(str(j[0])[1:-1]),encoding='utf8')
        path=r'./all'
        filenames=[]
        for root,dirs,files in os.walk(path):
            for file in files:
                filenames.append(os.path.join(root,file))
        result = []
        from pandas import read_csv
        for i in tqdm(filenames):
            if '.csv' in i :
                df=read_csv(i)
                sharp=df['sharp']
                sharp_max=df['sharp'].max()
                weight=df.loc[df['sharp'].idxmax(),'weights']
                rate=df.loc[df['sharp'].idxmax(),'rate']
                risk=df.loc[df['sharp'].idxmax(),'risk']
                codes=(eval(i[6:-4]))
                code=''
                for i in range(0,len(codes)):
                        code+=codes[i]
                        code+=','
                code=code[:-1]
                result.append([code,sharp_max,weight,rate,risk])
        df=DataFrame(result,columns=['names','sharp','weights','rate','risk'])
        df=df.sort_values(['sharp'], ascending=[False])
        if save==True:
            df.to_csv('result.csv',index=False,encoding='utf8')
        return df
