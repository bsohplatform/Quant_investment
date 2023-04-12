import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def rebalancing(assets_dict, capital):
    weight = [12, 4, 2, 1]
    now = datetime.today()-timedelta(days=1)

    before_months = [now - relativedelta(months=i) for i in range(13)]

    canary_list = ['SPY','VWO','VEA','BND']
    offense_list = ['SPY','QQQ','IWM','VGK','EWJ','VWO','VNQ','DBC','GLD','TLT','HYG','LQD']
    defense_list = ['TIP','DBC','BIL','IEF','TLT','LQD','BND']

    raw_data = yf.download(canary_list+offense_list+defense_list, start = before_months[-1].date())
    

    for i in range(13):
        days = 0
        while 1:
            try:
                dtime = timedelta(days=days)
                dtime = -dtime if i == 0 else dtime
                before_months[i] = before_months[i] + dtime
                raw_data.loc[str(before_months[i].date())]
                break
            except:
                days = days+1

    before_months = [str(before_months[i].date()) for i in range(13)] 
    mom_list = [before_months[1],before_months[3], before_months[6], before_months[12]]

    scores = []
    for canary in canary_list:
        canary_element = raw_data.loc[mom_list]['Close'][canary].to_numpy()
        canary_element = [(raw_data.loc[before_months[0]]['Close'][canary]/canary_element[i]-1)*weight[i] for i in range(4)]
        scores.append(sum(canary_element))
    
    assets_value_dict = {asset:value*raw_data.loc[before_months[0]]['Close'][asset] for asset, value in assets_dict.items()}
    asset_tot = sum(assets_value_dict.values())
    
    portfolio = {}
    
    SMA_list = []
    res_capital = capital
    if scores[0] > 0 and scores[1] > 0 and scores[2] > 0 and scores[3] > 0:
        for offense in offense_list:
            offense_element = raw_data.loc[before_months]['Close'][offense].to_numpy()
            SMA_list.append(offense_element[0]/np.mean(offense_element))

        sort_index = np.argsort(SMA_list)[::-1]
        list_sort = np.array(offense_list)[sort_index[:6]]
        if asset_tot == 0:
            for i in range(len(list_sort)):
                price = round(raw_data.loc[before_months[0]]['Close'][list_sort[i]])
                num_to_buy = round(capital/len(list_sort)/price)
                print(list_sort[i]+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                portfolio[list_sort[i]] = [num_to_buy, num_to_buy*price]
                res_capital = res_capital - num_to_buy*price
        else:
            assets_list = assets_dict.keys()
            to_sell_list = set(assets_list) - set(list_sort)
            to_buy_list = set(list_sort) - set(assets_list)
            to_add_list = set(assets_list) - set(to_sell_list)
                   
            if to_sell_list:
                for sell in to_sell_list:
                    print(sell+': '+str(assets_dict[sell])+'개 매도 (+'+str(round(assets_value_dict[sell]))+'$)')
                    res_capital = res_capital + assets_value_dict[sell]   
    else:
        for defense in defense_list:
            defense_element = raw_data.loc[before_months]['Close'][defense].to_numpy()
            SMA_list.append(defense_element[0]/np.mean(defense_element))

        sort_index = np.argsort(SMA_list)[::-1]
        list_sort = np.array(defense_list)[sort_index[:3]]
        bil_index = np.where(np.array(defense_list) == 'BIL')
        bil = np.array(SMA_list)[bil_index]
        
        if SMA_list[sort_index[0]] == bil:
            list_sort = np.array(defense_list)[sort_index[0]]
            bil_case = 2
        elif SMA_list[sort_index[1]] == bil:
            list_sort = np.array(defense_list)[sort_index[:2]]
            bil_case = 1
        else:
            bil_case = 0
        
        if asset_tot == 0:
            if bil_case == 1:
                price = round(raw_data.loc[before_months[0]]['Close'][list_sort[0]])
                price_bil = round(raw_data.loc[before_months[0]]['Close'][list_sort[1]])
                num_to_buy = round(capital/3/price)
                print(list_sort[0]+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                num_to_buy_bil = round(2*capital/3/price_bil)
                print(list_sort[1]+': '+str(num_to_buy_bil)+'개 매입 (-'+str(num_to_buy*price_bil)+'$)')
                portfolio[list_sort[0]] = [num_to_buy, num_to_buy*price]
                portfolio[list_sort[1]] = [num_to_buy_bil, num_to_buy_bil*price_bil]
                res_capital = res_capital - num_to_buy*price - num_to_buy_bil*price_bil
            else:    
                for buy in list_sort:
                    price = round(raw_data.loc[before_months[0]]['Close'][buy])
                    num_to_buy = round(capital/len(list_sort)/price)
                    print(buy+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                    portfolio[buy] = [num_to_buy, num_to_buy*price]
                    res_capital = res_capital - num_to_buy*price
        else:
            # BIL 보다 작은 경우 고려해서 작성 필요
            assets_list = assets_dict.keys()
            to_sell_list = set(assets_list) - set(list_sort)
            to_buy_list = set(list_sort) - set(assets_list)
            to_add_list = set(assets_list) - set(to_sell_list)
            
            if to_sell_list:
                for sell in to_sell_list:
                    print(sell+': '+str(assets_dict[sell])+'개 매도 (+'+str(round(assets_value_dict[sell]))+'$)')
                    res_capital = res_capital + assets_value_dict[sell]              
    
    res_capital_ref = res_capital
    
    if asset_tot != 0:
        if scores[0] > 0 and scores[1] > 0 and scores[2] > 0 and scores[3] > 0:
            if to_add_list:
                for add in to_add_list:
                    price = round(raw_data.loc[before_months[0]]['Close'][add])
                    num_to_add = round((res_capital_ref/len(to_add_list)-assets_value_dict[add])/price)
                    if num_to_add < 0:
                        print(add+': '+str(-num_to_add)+'개 추가 매도 (+'+str(-num_to_add*price)+'$)')
                    else:
                        print(add+': '+str(num_to_add)+'개 추가 매입 (-'+str(num_to_add*price)+'$)') 
                    
                    assets_dict[add] = assets_dict[add] + num_to_add
                    res_capital = res_capital - num_to_add*price
                    portfolio[add] = [assets_dict[add], assets_dict[add]*price]
                    
            if to_buy_list:
                for buy in to_buy_list:
                    price = round(raw_data.loc[before_months[0]]['Close'][buy])
                    num_to_buy = round(res_capital_ref/len(to_buy_list)/price)
                    print(buy+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                    
                    res_capital = res_capital - num_to_buy*price
                    portfolio[buy] = [num_to_buy, num_to_buy*price]
        else:
            if to_add_list:
                for add in to_add_list:
                    if bil_case == 1:
                        price = round(raw_data.loc[before_months[0]]['Close'][add])
                        if add == 'BIL':
                            num_to_add = round((2*res_capital_ref/3-assets_value_dict[add])/price)
                        else:    
                            num_to_add = round((res_capital_ref/3-assets_value_dict[add])/price)
                    else:    
                        num_to_add = round((res_capital_ref-assets_value_dict[add])/price)
                    
                    if num_to_add < 0:
                        print(add+': '+str(-num_to_add)+'개 추가 매도 (+'+str(-num_to_add*price)+'$)')
                    else:
                        print(add+': '+str(num_to_add)+'개 추가 매입 (-'+str(num_to_add*price)+'$)')  
                    
                    assets_dict[add] = assets_dict[add] + num_to_add
                    res_capital = res_capital - num_to_add*price
                    portfolio[add] = [assets_dict[add], assets_dict[add]*price]
                    
                if to_buy_list:
                    for buy in to_buy_list:
                        if bil_case == 1:
                            price = round(raw_data.loc[before_months[0]]['Close'][buy])
                            if buy == 'BIL':
                                num_to_buy = round(2*res_capital_ref/3/price)
                            else:    
                                num_to_buy = round(res_capital_ref/3/price)
                        else:    
                            num_to_buy = round(res_capital_ref/price)
                        print(buy+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                        
                        res_capital = res_capital - num_to_buy*price
                        portfolio[buy] = [num_to_buy, num_to_buy*price]
    
    print('현금: '+str(round(res_capital))+'$ 보유')
    print(portfolio)
if __name__ == '__main__':
    #assets_dict = {'SPY':1,'QQQ':1,'IWM':2,'VGK':10,'EWJ':10,'VWO':10}
    assets_dict = {}
    capital = 1000
    rebalancing(assets_dict, capital)