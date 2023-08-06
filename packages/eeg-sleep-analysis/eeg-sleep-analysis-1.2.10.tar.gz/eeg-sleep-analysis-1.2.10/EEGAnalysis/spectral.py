import pandas as pd
import numpy as np

def rename_cols_for_spectral(df):
    new_cols = []
    for col in df.columns:
        try:
            new_cols.append(np.int(col.split('.')[0]))
        except:
            new_cols.append(col)
    
    col_max = np.max([x for x in new_cols if isinstance(x,int) == True])
    return new_cols, col_max

def prep_for_spectral(df, config_dict):
    freq_bins = config_dict['freq_bins']
    
    new_cols, col_max = rename_cols_for_spectral(df)
    df.columns = new_cols
    if 'bout_num' in df.columns:
        df.drop('bout_num',axis=1,inplace=True)

    for x in freq_bins.keys():
        bin_range = [freq_bins[x][0], np.min([freq_bins[x][1], col_max])]
        df[x] = df.iloc[:,2+bin_range[0]:3+bin_range[1]].sum(axis=1)

    if config_dict['L_or_D_first'] == 'D':
        idx_nm = df.index.name
        df.reset_index(inplace=True)
        df[idx_nm] = np.where(df[idx_nm] >= 10800, df[idx_nm] - 10800, 10800+ df[idx_nm])
        df.sort_values(idx_nm,inplace=True)
        df.set_index(idx_nm, inplace=True)
    
    return df

def NR_delta_power_int(df, config_dict):
    df['NR_running_count'] = np.where(df.Stage == 'NR',1,0).cumsum()
    
    delta_int = []
    num_epochs_per_sec = config_dict['num_epochs_per_segment']
    for i in np.arange(int(np.floor(df.NR_running_count.max())/num_epochs_per_sec)):
        i_min = num_epochs_per_sec*(i) + 1
        i_max = num_epochs_per_sec*(i+1)
        delta_int.append(df[(df.Stage == 'NR') & (df.NR_running_count >= i_min) & (df.NR_running_count <= i_max)].delta.mean())

    df_NR_delta_INT = pd.DataFrame({'interval_num':np.arange(1,len(delta_int) + 1),'avg_delta_power':delta_int})
    
    return df_NR_delta_INT 

def NR_delta_power_zt(df, config_dict, BL):
    nr_delta_zt = []
    nr_count_zt = []
    num_hours = config_dict['num_total_hours']
    num_epochs = int(np.round(3600/config_dict['seconds_per_epoch'],0))
    
    for i in np.arange(num_hours):
        i_min = num_epochs*(i)
        i_max = num_epochs*(i+1) - 1
        nr_delta_zt.append(df[(df.Stage == 'NR')].loc[i_min:i_max].delta.mean())
        nr_count_zt.append(df[(df.Stage == 'NR')].loc[i_min:i_max].delta.count())

    df_NR_delta_ZT = pd.DataFrame({'avg_delta_power':nr_delta_zt,'num_epochs':nr_count_zt})
    df_NR_delta_ZT['ZT'] = ['ZT' + str(x) for x in df_NR_delta_ZT.index]
    df_NR_delta_ZT = df_NR_delta_ZT[['ZT','avg_delta_power','num_epochs']].copy()
    
    if BL == True:
        df_bl_norm = df_NR_delta_ZT[df_NR_delta_ZT.ZT.isin(['ZT8','ZT9','ZT10','ZT11'])]
        BL_normal = (df_bl_norm.avg_delta_power * df_bl_norm.num_epochs).sum()/df_bl_norm.num_epochs.sum()
        return df_NR_delta_ZT, BL_normal
    else:
        return df_NR_delta_ZT
    
def power_spec(df, config_dict, BL):
    hz_cols = pd.to_numeric(df.columns, errors = 'coerce').dropna().astype(int)
    df_spec_out = pd.DataFrame()
    for n,z in enumerate(zip([0,config_dict['lights_off_zt']], [config_dict['lights_off_zt'],config_dict['num_total_hours']])):
        i_min = z[0]*900
        i_max = z[1]*900-1

        df_out = df.loc[i_min:i_max].groupby('Stage')[hz_cols].mean()
        df_out = df_out.merge(df.loc[i_min:i_max].groupby('Stage').Time.count().to_frame().rename(columns = {'Time':'Count'}),\
                          left_index=True, right_index=True)
        
        if n == 0:
            df_out['Period'] = 'Light'
        else:
            df_out['Period'] = 'Dark'

        df_spec_out = df_spec_out.append(df_out.reset_index(),ignore_index=True, sort = False)
    if BL == True:
        df_spec_out['avg_power'] = df_spec_out[hz_cols].mean(axis=1)
        BL_spec_normal = (df_spec_out.Count * df_spec_out.avg_power).sum()/df_spec_out.Count.sum()
        
        return df_spec_out[['Period','Stage','Count'] + list(hz_cols)], BL_spec_normal, hz_cols
    else:
        return df_spec_out[['Period','Stage','Count'] + list(hz_cols)]