#!/usr/bin/env python

import pandas as pd
import numpy as np
import PySimpleGUI as sg
from EEGAnalysis.get_config import *
from EEGAnalysis.get_animal_conditions import *
from EEGAnalysis.output_results import *
from EEGAnalysis.run_main_analysis import *
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

def main():  
    layout = [[sg.Text('Create new config.txt'),sg.Button('Click')],
             [sg.Text('Locate config.txt')],
             [sg.Input(), sg.FileBrowse()],
             [sg.Text('___________________________________________________________')],
             [sg.Text('Create new conditions.csv? config.txt required'),sg.Button('Click')],
             [sg.Text('Locate conditions.csv')],
             [sg.Input(), sg.FileBrowse()],
             [sg.Text('___________________________________________________________')],
             [sg.OK(), sg.Button('Close')]]

    # Create the Window
    window = sg.Window('Sleep Behavior Analysis from EEG', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            break

        if event == "Click":
            config_check = sg.popup_yes_no('Are you sure?', keep_on_top=True, title = 'Confirm')
            if config_check == 'Yes':
                create_config() 
                sg.popup('New config.txt created in current directory.', title = 'File created')
        elif event == "Click0":
            conditions_check = sg.popup_yes_no('Are you sure?', keep_on_top=True)
            if conditions_check == 'Yes':
                config_dict = read_config(values['Browse'])
                create_conditions(config_dict['conditions_directory'],config_dict['id_condition_filename'], config_dict['file_naming_convention'])
                sg.popup('New conditions.csv created.', title = 'File created')
        elif event == 'OK':
            config_dict = read_config(values['Browse']) 
            all_conditions = pd.read_csv(os.path.join(config_dict['conditions_directory'], config_dict['id_condition_filename']))
            
            condition_cols = config_dict['organize_output']
            if set(condition_cols).issubset(set(all_conditions.columns)) == False:
                condition_cols = ['raw_filename']

            all_totals, all_bouts, all_bout_dist, all_spectral, all_delta_discharge_zt, all_delta_discharge_int = run_analyses(config_dict, all_conditions, condition_cols)
            all_totals.name = 'all_totals'
            all_bouts.name = 'all_bouts'
            all_bout_dist.name = 'all_bout_dist'
            all_spectral.name = 'all_spectral'
            all_delta_discharge_zt.name = 'all_delta_discharge_zt'
            all_delta_discharge_int.name = 'all_delta_discharge_int'

            for df in (all_totals, all_bouts, all_bout_dist, all_spectral, all_delta_discharge_zt, all_delta_discharge_int):
                write_to_excel(df, config_dict, condition_cols) 

            sg.popup('Analysis completed.', title = 'Complete')

    window.close()

if __name__ == "__main__":
    main()