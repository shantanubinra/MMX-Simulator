import pandas as pd
from gekko import GEKKO
import numpy as np 
import ast 
import os
from datetime import date






def generate_excel(Title , path , constant_vars):
    '''
        AIM : This function will help to generate Excel report
        Inputs : 
            Title : Unique name of file 
            Path : path to store file ..
    
    '''
    
    today = date.today()
    result_dict = {    
                'Channels' :   ['Field calls' , 'DTC Paid Search' , 'HCP Paid Search' , 'HCP Digital' , 'HCP Email' , 'Dtc Display' , 'HCP Display' ,'Speaker Program Person' , 
                                'Speaker Program Virtual' , 'GNA Calls' , 'DTC Social' ] ,         
                'mROI at Current Spend' : [] ,         
                'Current Spend' : [] ,  
                'Allocated Budget' : [x[0] for x in model_2._variables] , 

                'Predicted Revenue' : [y_fild_calls ,y_dp_search , y_hcp_search ,y_hcp_digital , y_hcp_mail ,  y_dtc_display ,y_hcp_display , y_spk_person ,  y_spk_virtual ,y_gna_Calls ,  y_dtc_social ] , 
                'Current Revenue' : [] 
                
            }        

    for i in result_dict['Channels'] : 
        df = pd.read_excel('./data/data_new.xlsx' , sheet_name=i, 
                        dtype={'% Change in Spend':str} )
        # print(np.where(df['% Change in Spend'] == '7.528699885739343e-16'))
        Current_data_ = df[df['% Change in Spend'] == '7.528699885739343e-16']
        result_dict['Current Spend'].append(Current_data_['Total Spend'].values[0])
        result_dict['Current Revenue'].append(Current_data_['Revenue'].values[0])
        result_dict['mROI at Current Spend'].append(Current_data_.iloc[:,-1].values[0]) 
        
    ## Add constant Values 
    result_dict['Channels'].append('HCP WEBSITE')
    result_dict['Current Revenue'].append(constant_vars['hcp_website_revenue_'])
    result_dict['Current Spend'].append(constant_vars['hcp_website_spend_'])
    result_dict['Allocated Budget'].append(constant_vars['hcp_website_spend_'])
    result_dict['Predicted Revenue'].append(constant_vars['hcp_website_revenue_'])
    result_dict['mROI at Current Spend'].append(0)
    
    
    
    result_dict['Channels'].append('DTC WEBSITE')    
    result_dict['Current Spend'].append(constant_vars['dtc_website_spend_'])    
    result_dict['Current Revenue'].append(constant_vars['dtc_website_revenue_'])
    result_dict['Allocated Budget'].append(constant_vars['dtc_website_spend_'])    
    result_dict['Predicted Revenue'].append(constant_vars['dtc_website_revenue_'])
    result_dict['mROI at Current Spend'].append(0)
    
    result_df = pd.DataFrame(result_dict)
    pd.options.display.float_format = "{:.2f}".format
    result_df = result_df.sort_values(by=['mROI at Current Spend'] , ascending=False)
    result_df['% change in revenue'] = ((result_df['Predicted Revenue'] - result_df['Current Revenue'] ) / result_df['Current Revenue'] )* 100
    result_df['% change in Spend'] = ((result_df['Allocated Budget'] - result_df['Current Spend'] ) / result_df['Current Spend'] )* 100

    additional_row = { 'Channels' : 'Total' , 'mROI at Current Spend' : np.nan , 'Current Spend' : result_df['Current Spend'].sum() , 
                    'Allocated Budget' : result_df['Allocated Budget'].sum(), 'Predicted Revenue' :result_df['Predicted Revenue' ].sum() , 'Current Revenue' :result_df['Current Revenue'].sum() ,
                     '% change in revenue' : np.nan, '% change in Spend' : np.nan }

    # arrnaging cols   
    result_df =result_df.append(additional_row , ignore_index=True)
    cols_sequence = ['Channels', 'mROI at Current Spend', 'Current Spend',
        'Allocated Budget', '% change in Spend', 'Current Revenue','Predicted Revenue', 
        '% change in revenue']
    result_df = result_df[cols_sequence]

    result_df.to_excel(f'{path}{Title}_Optimizer_Reports{today.strftime("%d_%m_%Y")}.xlsx')

    return result_df
