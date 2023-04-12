import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def rebalancing(assets_dict, capital):
    
    before_months = [datetime.today()-timedelta(days=1), datetime.today()-timedelta(days=1)-relativedelta(months=12)]
    
    p1 = ['SPY','EFA']
    p2 = ['LQD','HYG']
    p3 = ['VNQ','REM']
    p4 = ['TLT','GLD']
    bil = ['BIL']
    
    raw_data = yf.download(p1+p2+p3+p4+bil, start = before_months[-1].date())
    
    for i in range(len(before_months)):
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

    before_months = [str(before_months[i].date()) for i in range(len(before_months))] 
    bil_rate = raw_data.loc[before_months[0]]['Close']['BIL']/raw_data.loc[before_months[-1]]['Close']['BIL']-1
    p1_rate = raw_data.loc[before_months[0]]['Close'][p1].to_numpy()/raw_data.loc[before_months[-1]]['Close'][p1].to_numpy()-1
    p2_rate = raw_data.loc[before_months[0]]['Close'][p2].to_numpy()/raw_data.loc[before_months[-1]]['Close'][p2].to_numpy()-1
    p3_rate = raw_data.loc[before_months[0]]['Close'][p3].to_numpy()/raw_data.loc[before_months[-1]]['Close'][p3].to_numpy()-1
    p4_rate = raw_data.loc[before_months[0]]['Close'][p4].to_numpy()/raw_data.loc[before_months[-1]]['Close'][p4].to_numpy()-1
    p1_index = np.argmax(p1_rate)
    p2_index = np.argmax(p2_rate)
    p3_index = np.argmax(p3_rate)
    p4_index = np.argmax(p4_rate)
    
    
    assets_value_dict = {asset:value*raw_data.loc[before_months[0]]['Close'][asset] for asset, value in assets_dict.items()}
    asset_tot = sum(assets_value_dict.values())

    portfolio = {}
    res_capital = capital
    if p1_rate[p1_index] > bil_rate:
        if asset_tot == 0:
            price = round(raw_data.loc[before_months[0]]['Close'][p1[p1_index]])
            num_to_buy = round(capital/4/price)
            print(p1[p1_index]+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
            res_capital = res_capital - num_to_buy*price
            portfolio[p1[p1_index]] = [num_to_buy, num_to_buy*price]
        else:
            if p1[p1_index] == p1[0]:
                match_idx = p1[0]
                unmatch_idx = p1[1]
            else:
                match_idx = p1[1]
                unmatch_idx = p1[0]
            
            if unmatch_idx in assets_dict.keys():
                print(unmatch_idx+': '+str(assets_dict[unmatch_idx])+'개 매도 (+'+str(round(assets_value_dict[unmatch_idx]))+'$)')
                res_capital = res_capital + assets_value_dict[unmatch_idx]
    else:
        if asset_tot != 0:
            try:
                print('SPY: '+str(round(assets_dict['SPY']))+'개 매도 (+'+str(round(assets_value_dict['SPY']))+'$)')
                sell_value = assets_dict['SPY']*raw_data.loc[before_months[0]]['Close']['SPY']
            except:
                print('EFA: '+str(round(assets_dict['EFA']))+'개 매도 (+'+str(round(assets_value_dict['EFA']))+'$)')
                sell_value = assets_dict['EFA']*raw_data.loc[before_months[0]]['Close']['EFA']
            res_capital = res_capital + sell_value
    
    if p2_rate[p2_index] > bil_rate:
        if asset_tot == 0:
            price = round(raw_data.loc[before_months[0]]['Close'][p2[p2_index]])
            num_to_buy = round(capital/4/price)
            print(p2[p2_index]+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
            res_capital = res_capital - num_to_buy*price
            portfolio[p2[p2_index]] = [num_to_buy, num_to_buy*price]
        else:
            if p2[p2_index] == p2[0]:
                match_idx = p2[0]
                unmatch_idx = p2[1]
            else:
                match_idx = p2[1]
                unmatch_idx = p2[0]
            
            if unmatch_idx in assets_dict.keys():
                print(unmatch_idx+': '+str(assets_dict[unmatch_idx])+'개 매도 (+'+str(round(assets_value_dict[unmatch_idx]))+'$)')
                res_capital = res_capital + assets_value_dict[unmatch_idx]
    else:
        if asset_tot != 0:
            try:
                print('LQD: '+str(round(assets_dict['LQD']))+'개 매도 (+'+str(round(assets_value_dict['LQD']))+'$)')
                sell_value = assets_dict['LQD']*raw_data.loc[before_months[0]]['Close']['LQD']
            except:
                print('HYG: '+str(round(assets_dict['HYG']))+'개 매도 (+'+str(round(assets_value_dict['HYG']))+'$)')
                sell_value = assets_dict['HYG']*raw_data.loc[before_months[0]]['Close']['HYG']
            res_capital = res_capital + sell_value
            
    if p3_rate[p3_index] > bil_rate:
        if asset_tot == 0:
            price = round(raw_data.loc[before_months[0]]['Close'][p3[p3_index]])
            num_to_buy = round(capital/4/price)
            print(p3[p3_index]+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
            res_capital = res_capital - num_to_buy*price
            portfolio[p3[p3_index]] = [num_to_buy, num_to_buy*price]
        else:
            if p3[p3_index] == p3[0]:
                match_idx = p3[0]
                unmatch_idx = p3[1]
            else:
                match_idx = p3[1]
                unmatch_idx = p3[0]
            
            if unmatch_idx in assets_dict.keys():
                print(unmatch_idx+': '+str(assets_dict[unmatch_idx])+'개 매도 (+'+str(round(assets_value_dict[unmatch_idx]))+'$)')
                res_capital = res_capital + assets_value_dict[unmatch_idx]
    else:
        if asset_tot != 0:
            try:
                print('VNQ: '+str(round(assets_dict['VNQ']))+'개 매도 (+'+str(round(assets_value_dict['VNQ']))+'$)')
                sell_value = assets_dict['VNQ']*raw_data.loc[before_months[0]]['Close']['VNQ']
            except:
                print('REM: '+str(round(assets_dict['REM']))+'개 매도 (+'+str(round(assets_value_dict['REM']))+'$)')
                sell_value = assets_dict['REM']*raw_data.loc[before_months[0]]['Close']['REM']
            res_capital = res_capital + sell_value
            
    if p4_rate[p4_index] > bil_rate:
        if asset_tot == 0:
            price = round(raw_data.loc[before_months[0]]['Close'][p4[p4_index]])
            num_to_buy = round(capital/4/price)
            print(p4[p4_index]+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
            res_capital = res_capital - num_to_buy*price
            portfolio[p4[p4_index]] = [num_to_buy, num_to_buy*price]
        else:
            if p4[p4_index] == p4[0]:
                match_idx = p4[0]
                unmatch_idx = p4[1]
            else:
                match_idx = p4[1]
                unmatch_idx = p4[0]
            
            if unmatch_idx in assets_dict.keys():
                print(unmatch_idx+': '+str(assets_dict[unmatch_idx])+'개 매도 (+'+str(round(assets_value_dict[unmatch_idx]))+'$)')
                res_capital = res_capital + assets_value_dict[unmatch_idx]
    else:
        if asset_tot != 0:
            try:
                print('TLT: '+str(round(assets_dict['TLT']))+'개 매도 (+'+str(round(assets_value_dict['TLT']))+'$)')
                sell_value = assets_dict['TLT']*raw_data.loc[before_months[0]]['Close']['TLT']
            except:
                print('GLD: '+str(round(assets_dict['GLD']))+'개 매도 (+'+str(round(assets_value_dict['GLD']))+'$)')
                sell_value = assets_dict['GLD']*raw_data.loc[before_months[0]]['Close']['GLD']
            res_capital = res_capital + sell_value
    
    res_capital_ref = res_capital
    
    if asset_tot != 0.0:
        if p1_rate[p1_index] > bil_rate:
            if p1[p1_index] == p1[0]:
                match_idx = p1[0]
                unmatch_idx = p1[1]
            else:
                match_idx = p1[1]
                unmatch_idx = p1[0]
            
            if match_idx in assets_dict.keys():
                price = round(raw_data.loc[before_months[0]]['Close'][p1[p1_index]])
                num_to_buy = round((res_capital_ref/4-assets_value_dict[match_idx])/price)
                if num_to_buy > 0:
                    print(match_idx+': '+str(num_to_buy)+'개 추가매입 (-'+str(num_to_buy*price)+'$)')
                else:
                    print(match_idx+': '+str(-num_to_buy)+'개 추가매도 (+'+str(-num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
                num_to_buy = num_to_buy + assets_dict[match_idx]
            else:
                price = round(raw_data.loc[before_months[0]]['Close'][p1[p1_index]])
                num_to_buy = round(res_capital_ref/4/price)
                print(match_idx+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
                
            portfolio[match_idx] = [num_to_buy, num_to_buy*price]
            
        if p2_rate[p2_index] > bil_rate:
            if p2[p2_index] == p2[0]:
                match_idx = p2[0]
                unmatch_idx = p2[1]
            else:
                match_idx = p2[1]
                unmatch_idx = p2[0]
            
            if match_idx in assets_dict.keys():
                price = round(raw_data.loc[before_months[0]]['Close'][p2[p2_index]])
                num_to_buy = round((res_capital_ref/4-assets_value_dict[match_idx])/price)
                if num_to_buy > 0:
                    print(match_idx+': '+str(num_to_buy)+'개 추가매입 (-'+str(num_to_buy*price)+'$)')
                else:
                    print(match_idx+': '+str(-num_to_buy)+'개 추가매도 (+'+str(-num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
                num_to_buy = num_to_buy + assets_dict[match_idx]
            else:
                price = round(raw_data.loc[before_months[0]]['Close'][p2[p2_index]])
                num_to_buy = round(res_capital_ref/4/price)
                print(match_idx+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
            
            portfolio[match_idx] = [num_to_buy, num_to_buy*price]
            
        if p3_rate[p3_index] > bil_rate:
            if p3[p3_index] == p3[0]:
                match_idx = p3[0]
                unmatch_idx = p3[1]
            else:
                match_idx = p3[1]
                unmatch_idx = p3[0]
            
            if match_idx in assets_dict.keys():
                price = round(raw_data.loc[before_months[0]]['Close'][p3[p3_index]])
                num_to_buy = round((res_capital_ref/4-assets_value_dict[match_idx])/price)
                if num_to_buy > 0:
                    print(match_idx+': '+str(num_to_buy)+'개 추가매입 (-'+str(num_to_buy*price)+'$)')
                else:
                    print(match_idx+': '+str(-num_to_buy)+'개 추가매도 (+'+str(-num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
                num_to_buy = num_to_buy + assets_dict[match_idx]
            else:
                price = round(raw_data.loc[before_months[0]]['Close'][p3[p3_index]])
                num_to_buy = round(res_capital_ref/4/price)
                print(match_idx+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
            
            portfolio[match_idx] = [num_to_buy, num_to_buy*price]
            
        if p4_rate[p4_index] > bil_rate:
            if p4[p4_index] == p4[0]:
                match_idx = p4[0]
                unmatch_idx = p4[1]
            else:
                match_idx = p4[1]
                unmatch_idx = p4[0]
            
            if match_idx in assets_dict.keys():
                price = round(raw_data.loc[before_months[0]]['Close'][p4[p4_index]])
                num_to_buy = round((res_capital_ref/4-assets_value_dict[match_idx])/price)
                if num_to_buy > 0:
                    print(match_idx+': '+str(num_to_buy)+'개 추가매입 (-'+str(num_to_buy*price)+'$)')
                else:
                    print(match_idx+': '+str(-num_to_buy)+'개 추가매도 (+'+str(-num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
                num_to_buy = num_to_buy + assets_dict[match_idx]
            else:
                price = round(raw_data.loc[before_months[0]]['Close'][p4[p4_index]])
                num_to_buy = round(res_capital_ref/4/price)
                print(match_idx+': '+str(num_to_buy)+'개 매입 (-'+str(num_to_buy*price)+'$)')
                res_capital = res_capital - num_to_buy*price
                
            portfolio[match_idx] = [num_to_buy, num_to_buy*price]
    
    print('현금: '+str(round(res_capital))+'$ 보유')
    print(portfolio)
    
if __name__ == '__main__':
    assets_dict = {}
    capital = 1000
    rebalancing(assets_dict, capital)
    
    
    