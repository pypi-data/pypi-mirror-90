import pandas as pd
import numpy as np
import csv
import re
import os

def switch_L_and_D(df, lights_off_zt):
    light = [x for x in df.ZT if int(x.split('-')[1]) <= lights_off_zt]
    dark = [x for x in df.ZT if int(x.split('-')[1]) > lights_off_zt]
    df['ZT'] = dark + light
    df = df.reindex(np.argsort([int(x.split('-')[1]) for x in dark+light])).reset_index(drop=True)
    
    return df

def get_stage_totals(df,
                     num_hours_per_segment_totals,
                     num_total_hours,
                     seconds_per_epoch,
                     lights_off_zt,
                     L_or_D_first):
    
    df_totals = pd.DataFrame()
    for i in np.arange(num_total_hours/num_hours_per_segment_totals):
        imin = int(i*num_hours_per_segment_totals*(3600/seconds_per_epoch))
        imax = int((i+1)*num_hours_per_segment_totals*(3600/seconds_per_epoch))
        z = 'ZT' + str(int(i*num_hours_per_segment_totals)) + '-' + str(int((i+1)*num_hours_per_segment_totals))

        dict_totals = {**{'epoch_min': imin, 'epoch_max': imax, 'ZT':z}, 
                       **(df.iloc[imin:imax].Stage.value_counts()*(seconds_per_epoch/60)).to_dict()}

        df_totals = df_totals.append(pd.DataFrame(dict_totals, index=[0]),ignore_index=True,sort=False)

    df_totals.fillna(0,inplace=True)
    
    if L_or_D_first == 'D':
        df_totals = switch_L_and_D(df_totals, lights_off_zt)
    
    return df_totals

def get_bout_agg(dfb):
    dfg = dfb.groupby('Stage').agg({'count','mean'})
    dfg.columns = ['_'.join(col).strip() for col in dfg.columns.values]
    return dfg.reset_index()

def get_bout_dist(dfb, dist_cutoffs,dist_labels):
    df_dist = pd.cut(dfb[dfb.Stage == 'W']['bout'], bins= dist_cutoffs + [np.inf], labels = dist_labels).value_counts().sort_index().to_frame()
    df_dist = df_dist.reset_index().rename(columns = {'index':'bout_dist_cat'})
    return df_dist

def get_bout_details(df, 
                     num_hours_per_segment_bouts,
                     num_total_hours,
                     seconds_per_epoch,
                     dist_cutoffs,
                     lights_off_zt,
                     L_or_D_first):
    
    df_bout_agg = pd.DataFrame()
    df_bout_dist = pd.DataFrame()
    for i in np.arange(num_total_hours/num_hours_per_segment_bouts):
        imin = int(i*num_hours_per_segment_bouts*(3600/seconds_per_epoch))
        imax = int((i+1)*num_hours_per_segment_bouts*(3600/seconds_per_epoch))
        
        dfb = (df[['Stage','bout_num']].iloc[imin:imax].reset_index().\
               groupby(['Stage','bout_num']).count() * seconds_per_epoch).\
                reset_index().drop("bout_num",axis=1).rename(columns={'EpochNo':'bout'})
        
        dfg = get_bout_agg(dfb)
        dfg['ZT'] = 'ZT' + str(int(i*num_hours_per_segment_bouts)) + '-' + str(int((i+1)*num_hours_per_segment_bouts))
        if L_or_D_first == 'D':
            dfg = switch_L_and_D(dfg,lights_off_zt)
        df_bout_agg = df_bout_agg.append(dfg,ignore_index=True,sort=False)
        
        dist_labels = [str(x) for x in dist_cutoffs[1:] + ['>' + str(dist_cutoffs[-1])]]
        dfd = get_bout_dist(dfb, dist_cutoffs, dist_labels)
        dfd['ZT'] = 'ZT' + str(int(i*num_hours_per_segment_bouts)) + '-' + str(int((i+1)*num_hours_per_segment_bouts))
        if L_or_D_first == 'D':
            dfd = switch_L_and_D(dfd, lights_off_zt)
        df_bout_dist = df_bout_dist.append(dfd,ignore_index=True,sort=False)
    
    if L_or_D_first == 'D':
        df_bout_agg = switch_L_and_D(df_bout_agg)
        df_bout_dist = switch_L_and_D(df_bout_dist)
    
    return df_bout_agg, df_bout_dist

