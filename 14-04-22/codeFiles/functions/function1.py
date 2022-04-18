from gekko import GEKKO
import pandas as pd
from datetime import date
import logging




def function_1(Total_Budget , datafilePath='input_polynomial.xlsx'  ,coef_sheet_name='Sheet1'):
    # Total_Budget = 50000000
    # datafilePath= 'input_polynomial.xlsx' 
    # coef_sheet_name = 'Sheet1'
    dF_ = pd.read_excel(datafilePath, sheet_name = coef_sheet_name)
    channelNames = dF_.channel_name.values
    Variables_dict = {} 
    equations_list = []

    model_ = GEKKO()
    for _ , row_ in dF_.iterrows():
        # print(row_)
        if 'hcp display' in row_['channel_name'].lower():
            Variables_dict[row_['channel_name']] = model_.Var(value= row_['current_spend'], lb=row_['lower bound'],ub=row_['Upper bound'] , name= row_['channel_name'] )
            # var__ = model_.log(model_._variables[_])
            var__ = model_.log(Variables_dict[row_['channel_name']])

            model_.Maximize((var__*row_['term_1 (a)'] + var__*row_['term_2 (b)'] + var__*row_['term_2 (c)'] + var__*row_['term_3 (e)'] + var__*row_['term_3 (f)'] + var__*row_['term_3 (g)'] + row_['term_3 (intercept)']))
        else:
            # Variable initialization
            Variables_dict[row_['channel_name']] = model_.Var(value= row_['current_spend'], lb=row_['lower bound'],ub=row_['Upper bound'] , name= row_['channel_name'] )
            # var_ = (model_._variables[_])**0.5
            var_ = (Variables_dict[row_['channel_name']])**0.5

            # print(var_)
            model_.Maximize( (var_*row_['term_1 (a)'] + (var_**2)*row_['term_2 (b)'] + (var_**3)*row_['term_2 (c)'] + (var_**4)*row_['term_3 (e)'] + (var_**5)*row_['term_3 (f)'] + (var_**6)*row_['term_3 (g)'] + row_['term_3 (intercept)']))

    model_.Equation(sum(model_._variables) <= Total_Budget) # constrains
    model_.solve(disp=False)
    return model_ , dF_
    
