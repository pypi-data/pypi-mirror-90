import pandas as pd
import numpy as np
import csv
import re
import os
from EEGAnalysis.bout_analysis import *
from EEGAnalysis.spectral import *

def get_empty_frames():
    all_totals = pd.DataFrame()
    all_bouts = pd.DataFrame()
    all_bout_dist = pd.DataFrame()
    all_spectral = pd.DataFrame()
    all_delta_discharge_zt = pd.DataFrame()
    all_delta_discharge_int = pd.DataFrame()
    
    return all_totals, all_bouts, all_bout_dist, all_spectral, all_delta_discharge_zt, all_delta_discharge_int

def read_in_file(config_dict,filename):    
    if config_dict['input_file_type'] == 'csv':
        reader = csv.reader(open(os.path.join(config_dict['file_directory'], filename), "rt"))

        i = 0
        for row in reader:
            if len(row) == 0:
                continue   
            elif row[0] == 'EpochNo':
                break
            i+=1

        df = pd.read_csv(config_dict['file_directory'] + '/' + filename,skiprows = i+2,index_col='EpochNo')
        df = df.iloc[:, :-1]
        df['bout_num'] = (df.Stage.shift(1) != df.Stage).cumsum()

        return df
    elif config_dict['input_file_type'] in ['xlsx','xls','excel']:
        print('Excel file type not supported. Use csv instead')
        return pd.DataFrame()
    else:
        print('Other file type not supported. Use csv instead')
        return pd.DataFrame()

def run_analyses(config_dict, all_conditions, condition_cols):
    all_totals, all_bouts, all_bout_dist, all_spectral, all_delta_discharge_zt, all_delta_discharge_int  = get_empty_frames()
    
    if (config_dict['run_SD_spectral'] == 'T') | (config_dict['get_delta_discharge'] == 'T'):
        if 'sleep_condition' in config_dict['file_naming_convention']:
            sd_conditions = all_conditions[all_conditions.sleep_condition == 'SD'].copy()
            non_sleep_cond_cols = list(set(condition_cols) - set(['sleep_condition']))
        else:
            print("If run_SD_spectral or get_delta_discharge = T, sleep_condition must be in file_naming_convention in config.txt file")
                 
    for i in np.arange(all_conditions.shape[0]):
        print("Running analysis for ", all_conditions.iloc[i].raw_filename)
        df = read_in_file(config_dict, all_conditions.iloc[i].raw_filename)
    
        if config_dict['get_stage_totals'] == 'T':
            df_totals = get_stage_totals(df = df,
                         num_hours_per_segment_totals = config_dict['num_hours_per_segment_totals'],
                         num_total_hours = config_dict['num_total_hours'],
                         seconds_per_epoch = config_dict['seconds_per_epoch'],
                         lights_off_zt = config_dict['lights_off_zt'],
                         L_or_D_first = config_dict['L_or_D_first'])
            
            for col in condition_cols:
                df_totals[col] = all_conditions.iloc[i][col]

            all_totals = all_totals.append(df_totals,ignore_index=True,sort=False)
         
        if config_dict['get_bout_details'] == 'T':
            df_bouts, df_bout_dist = get_bout_details(df = df, 
                                        num_hours_per_segment_bouts = config_dict['num_hours_per_segment_bouts'],
                                        num_total_hours = config_dict['num_total_hours'],
                                        seconds_per_epoch = config_dict['seconds_per_epoch'],
                                        dist_cutoffs = config_dict['dist_cutoffs'],
                                        lights_off_zt = config_dict['lights_off_zt'],
                                        L_or_D_first = config_dict['L_or_D_first'])          
                  
            for col in condition_cols:
                df_bouts[col] = all_conditions.iloc[i][col]
                df_bout_dist[col] = all_conditions.iloc[i][col]
       
            all_bouts = all_bouts.append(df_bouts,ignore_index=True,sort=False)
            all_bout_dist = all_bout_dist.append(df_bout_dist,ignore_index=True,sort=False)    
        
        if config_dict['get_spectral'] == 'T':
            if config_dict['run_SD_spectral'] == 'T':
                if 'sleep_condition' in config_dict['file_naming_convention']:                    
                    if all_conditions.iloc[i].sleep_condition == 'BL':
                        sd_file = pd.merge(all_conditions.iloc[i][non_sleep_cond_cols].to_frame().T, sd_conditions, on = non_sleep_cond_cols).raw_filename[0]
                        df_sd = read_in_file(config_dict, sd_file)
                        
                        df_forspec = prep_for_spectral(df, config_dict)
                        df_sd_forspec = prep_for_spectral(df_sd, config_dict)
                        
                        df_bl_spectral, bl_spec_norm, hz_cols = power_spec(df_forspec, config_dict, BL=True)
                        df_bl_spectral[hz_cols] /= bl_spec_norm
                        
                        df_sd_spectral = power_spec(df_sd_forspec, config_dict, BL = False)
                        df_sd_spectral[hz_cols] /= bl_spec_norm
                        
                        for col in condition_cols:
                            df_bl_spectral[col] = all_conditions.iloc[i][col]
                            if col == 'sleep_condition':
                                df_sd_spectral[col] = 'SD'
                            else:
                                df_sd_spectral[col] = all_conditions.iloc[i][col]
                        
                        all_spectral = all_spectral.append(df_bl_spectral,ignore_index=True,sort=False)
                        all_spectral = all_spectral.append(df_sd_spectral,ignore_index=True,sort=False)
                        
                    else:
                        pass                   
                else:
                    print("If run_SD_spectral = 'T', then sleep_condition must be in file_naming_convention")
            else:
                df_forspec = prep_for_spectral(df, config_dict)
                df_bl_spectral, bl_spec_norm, hz_cols = power_spec(df_forspec, config_dict, BL=True)
                df_bl_spectral[hz_cols] /= bl_spec_norm
                
                for col in condition_cols:
                    df_bl_spectral[col] = all_conditions.iloc[i][col]
                
                all_spectral = all_spectral.append(df_bl_spectral,ignore_index=True,sort=False)
                
        if config_dict['get_delta_discharge'] == 'T':
            if 'sleep_condition' in config_dict['file_naming_convention']:
                if all_conditions.iloc[i].sleep_condition == 'BL':
                    sd_file = pd.merge(all_conditions.iloc[i][non_sleep_cond_cols].to_frame().T, sd_conditions, on = non_sleep_cond_cols).raw_filename[0]
                    df_sd = read_in_file(config_dict, sd_file)

                    df_forspec = prep_for_spectral(df, config_dict)
                    df_sd_forspec = prep_for_spectral(df_sd, config_dict)
                        
                    df_bl_ZT, bl_delta_norm = NR_delta_power_zt(df_forspec, config_dict, BL = True)
                    df_bl_int = NR_delta_power_int(df_forspec, config_dict)
                    df_bl_ZT['avg_delta_power'] /= bl_delta_norm
                    df_bl_int['avg_delta_power'] /= bl_delta_norm

                    ## SD
                    df_sd_ZT = NR_delta_power_zt(df_sd_forspec, config_dict, BL = False)
                    df_sd_int = NR_delta_power_int(df_sd_forspec, config_dict)
                    df_sd_ZT['avg_delta_power'] /= bl_delta_norm
                    df_sd_int['avg_delta_power'] /= bl_delta_norm

                    for col in condition_cols:
                        df_bl_ZT[col] = all_conditions.iloc[i][col]
                        df_bl_int[col] = all_conditions.iloc[i][col]
                        if col == 'sleep_condition':
                            df_sd_ZT[col] = 'SD'
                            df_sd_int[col] = 'SD'
                        else:
                            df_sd_ZT[col] = all_conditions.iloc[i][col]
                            df_sd_int[col] = all_conditions.iloc[i][col]

                    all_delta_discharge_zt = all_delta_discharge_zt.append(df_bl_ZT,ignore_index=True,sort=False)
                    all_delta_discharge_zt = all_delta_discharge_zt.append(df_sd_ZT,ignore_index=True,sort=False)

                    all_delta_discharge_int = all_delta_discharge_int.append(df_bl_int,ignore_index=True,sort=False)           
                    all_delta_discharge_int = all_delta_discharge_int.append(df_sd_int,ignore_index=True,sort=False)
                else:
                    pass
            else:
                print("If get_delta_discharge = T, sleep_condition must be in file_naming_convention in config.txt file")         
        
    return all_totals, all_bouts, all_bout_dist, all_spectral, all_delta_discharge_zt, all_delta_discharge_int