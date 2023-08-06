import pandas as pd
import numpy as np
import csv
import xlsxwriter
import re
from openpyxl import load_workbook
import os
import itertools

def sort_by_ZT(df, other_factors = [], for_spectral = False):
    if for_spectral == False:
        df['int_vals'] = df.ZT.apply(lambda s: int(re.search('ZT(.*)-',s).group(1)))
        df.sort_values(['int_vals'] + other_factors,inplace=True)
        return df.iloc[:,:-1].set_index(['ZT'] + other_factors)
    else:
        df['sort_order'] = df.ZT.apply(lambda x: int(x[2:]))
        df = df.sort_values('sort_order')
        df = df.drop('sort_order',axis=1)
        return df

def write_to_excel(df, config_dict, condition_cols):
    custom_sort = {'W':0,'NR':1,'R':2}
    if df.empty is False:
        if df.name == 'all_totals':
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_all_totals.xlsx'
            book = pd.ExcelWriter(fileout, engine='openpyxl')
            for z in zip(['W','NR','R'],['Wake_totals','NREM_totals','REM_totals']):
                dft = pd.pivot_table(data = df, index = 'ZT',columns = condition_cols,values = z[0]).reset_index()
                dft = sort_by_ZT(dft)
                dft.to_excel(book,sheet_name = z[1],index=True)      
            book.save()
            book.close()
        elif df.name in ['all_bouts']:
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_bout_details.xlsx'
            book = pd.ExcelWriter(fileout, engine='openpyxl')
            for b in ['bout_count','bout_mean']:
                dft = pd.pivot_table(data = df, index = ['Stage','ZT'],columns = condition_cols,values = b).reset_index()
                dft['stage_sort_val'] = dft.Stage.map(custom_sort)
                dft = sort_by_ZT(dft,['stage_sort_val'])
                dft = dft.reset_index().set_index('ZT').iloc[:,1:]
                
                if b == 'bout_count':
                    b_name = 'bout_count_number'
                elif b == 'bout_mean':
                    b_name = 'bout_mean_length'
                    
                dft.to_excel(book,sheet_name = b_name,index=True)     
            book.save()
            book.close()
        elif df.name == 'all_bout_dist':
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_bout_details.xlsx'
            dft = pd.pivot_table(data = df, index = ['ZT','bout_dist_cat'],columns = condition_cols,values = 'bout').reset_index()
            dft = sort_by_ZT(dft,['bout_dist_cat'])
            
            with pd.ExcelWriter(fileout, engine = 'openpyxl', mode='a') as book:
                dft.to_excel(book, 'wake_bout_distrib', index=True)
            book.save()
            book.close()
            
        elif df.name == 'all_spectral':
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_spectogram.xlsx'
            book = pd.ExcelWriter(fileout, engine='openpyxl')
            
            for i in itertools.product(['Light','Dark'],['W','NR','R']):
                dft = df[(df.Period == i[0]) & (df.Stage == i[1])].copy()
                dft = dft.drop(['Period','Stage'],axis=1).set_index(condition_cols).T
                               
                dft.to_excel(book, i[0] + '_' + i[1], index=True)
                
            book.save()
            book.close()
            
        elif df.name == 'all_delta_discharge_zt':  
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_DeltaPower_byZT.xlsx'
            book = pd.ExcelWriter(fileout, engine='openpyxl')
            for i in ['BL','SD']: 
                dft = df[df.sleep_condition == i].copy()
                dfp = pd.pivot_table(data = dft.fillna(-1), index = 'ZT', columns = condition_cols, values = 'avg_delta_power').reset_index()
                dfp = sort_by_ZT(dfp, for_spectral = True)  
                dfp.set_index('ZT',inplace=True)
                dfp.replace({-1:np.nan},inplace=True)
                dfp.to_excel(book,sheet_name = i + '_deltaPower_byZT',index=True)

                dfp = pd.pivot_table(data = dft, index = 'ZT', columns = condition_cols, values = 'num_epochs').reset_index()
                dfp = sort_by_ZT(dfp, for_spectral = True) 
                dfp.set_index('ZT',inplace=True)
                dfp.to_excel(book,sheet_name = i + '_numEpochs_byZT',index=True)
                
            book.save()
            book.close()

        elif df.name == 'all_delta_discharge_int':
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_DeltaPower_byInterval.xlsx'
            book = pd.ExcelWriter(fileout, engine='openpyxl')
            
            for i in ['BL','SD']: 
                dft = df[df.sleep_condition == i].copy()
                dfp = pd.pivot_table(data = dft, index = 'interval_num', columns = condition_cols, values = 'avg_delta_power')
                dfp.to_excel(book,sheet_name = i + '_deltaPower_byInterval',index=True)
            
            book.save()
            book.close()
            
            