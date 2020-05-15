import numpy as np
import pandas as pd

    
Bundle_Performance=pd.read_csv("data/Bundle Performance and Margin.csv")

def BP_Contract_Calculation(Bundle_Payment_Contract,stop_gain,stop_loss,quality_adj_P_max,quality_adj_N_max):   

    
    Bundle_Merge=Bundle_Payment_Contract.merge(Bundle_Performance,left_on='Bundle', right_on='Bundle', suffixes=(False, False))
    
    #calculate performance scenario
    
    Bundle_Merge['PY_best_est_nocontract']=Bundle_Merge['Average Bundle Cost']*(1+Bundle_Merge['Baseline Trend'])
    Bundle_Merge['PY_best_case_nocontract']=Bundle_Merge['PY_best_est_nocontract']*(1-Bundle_Merge['Cost Best Case from BE'])
    Bundle_Merge['PY_worst_case_nocontract']=Bundle_Merge['PY_best_est_nocontract']*(1+Bundle_Merge['Cost Worst Case from BE'])
    
    Bundle_Merge['PY_best_est']=Bundle_Merge['Average Bundle Cost']*(1+Bundle_Merge['Baseline Trend'])*(1-Bundle_Merge['Cost Best Estimate from baseline'])
    Bundle_Merge['PY_best_case']=Bundle_Merge['PY_best_est']*(1-Bundle_Merge['Cost Best Case from BE'])
    Bundle_Merge['PY_worst_case']=Bundle_Merge['PY_best_est']*(1+Bundle_Merge['Cost Worst Case from BE'])
    
    #determine gain/loss & quality adjustment
    
    Bundle_Merge['Recom_PY_best_est_recon_amt']=pd.DataFrame([pd.DataFrame([Bundle_Merge['Recommended']-Bundle_Merge['PY_best_est'],Bundle_Merge['Recommended']*stop_gain]).min(axis=0),Bundle_Merge['Recommended']*(-stop_loss)]).max(axis=0)
    Bundle_Merge['Recom_PY_best_case_recon_amt']=pd.DataFrame([pd.DataFrame([Bundle_Merge['Recommended']-Bundle_Merge['PY_best_case'],Bundle_Merge['Recommended']*stop_gain]).min(axis=0),Bundle_Merge['Recommended']*(-stop_loss)]).max(axis=0)
    Bundle_Merge['Recom_PY_worst_case_recon_amt']=pd.DataFrame([pd.DataFrame([Bundle_Merge['Recommended']-Bundle_Merge['PY_worst_case'],Bundle_Merge['Recommended']*stop_gain]).min(axis=0),Bundle_Merge['Recommended']*(-stop_loss)]).max(axis=0)
    
    Bundle_Merge['Recom_PY_best_est_recon_amt_qual_adj']=np.where(Bundle_Merge['Recom_PY_best_est_recon_amt']>0, Bundle_Merge['Recom_PY_best_est_recon_amt']*(1-(1-Bundle_Merge['Quality Best Est'])*quality_adj_P_max), Bundle_Merge['Recom_PY_best_est_recon_amt']*(1-Bundle_Merge['Quality Best Est']*quality_adj_N_max))
    Bundle_Merge['Recom_PY_best_case_recon_amt_qual_adj']=np.where(Bundle_Merge['Recom_PY_best_case_recon_amt']>0, Bundle_Merge['Recom_PY_best_case_recon_amt']*(1-(1-Bundle_Merge['Quality Best Case'])*quality_adj_P_max), Bundle_Merge['Recom_PY_best_case_recon_amt']*(1-Bundle_Merge['Quality Best Case']*quality_adj_N_max))
    Bundle_Merge['Recom_PY_worst_case_recon_amt_qual_adj']=np.where(Bundle_Merge['Recom_PY_worst_case_recon_amt']>0, Bundle_Merge['Recom_PY_worst_case_recon_amt']*(1-(1-Bundle_Merge['Quality Worst Case'])*quality_adj_P_max), Bundle_Merge['Recom_PY_worst_case_recon_amt']*(1-Bundle_Merge['Quality Worst Case']*quality_adj_N_max))
    
    Bundle_Merge['UD_PY_best_est_recon_amt']=pd.DataFrame([pd.DataFrame([Bundle_Merge['User Defined']-Bundle_Merge['PY_best_est'],Bundle_Merge['User Defined']*stop_gain]).min(axis=0),Bundle_Merge['User Defined']*(-stop_loss)]).max(axis=0)
    Bundle_Merge['UD_PY_best_case_recon_amt']=pd.DataFrame([pd.DataFrame([Bundle_Merge['User Defined']-Bundle_Merge['PY_best_case'],Bundle_Merge['User Defined']*stop_gain]).min(axis=0),Bundle_Merge['User Defined']*(-stop_loss)]).max(axis=0)
    Bundle_Merge['UD_PY_worst_case_recon_amt']=pd.DataFrame([pd.DataFrame([Bundle_Merge['User Defined']-Bundle_Merge['PY_worst_case'],Bundle_Merge['User Defined']*stop_gain]).min(axis=0),Bundle_Merge['User Defined']*(-stop_loss)]).max(axis=0)
    
    Bundle_Merge['UD_PY_best_est_recon_amt_qual_adj']=np.where(Bundle_Merge['UD_PY_best_est_recon_amt']>0, Bundle_Merge['UD_PY_best_est_recon_amt']*(1-(1-Bundle_Merge['Quality Best Est'])*quality_adj_P_max), Bundle_Merge['UD_PY_best_est_recon_amt']*(1-Bundle_Merge['Quality Best Est']*quality_adj_N_max))
    Bundle_Merge['UD_PY_best_case_recon_amt_qual_adj']=np.where(Bundle_Merge['UD_PY_best_case_recon_amt']>0, Bundle_Merge['UD_PY_best_case_recon_amt']*(1-(1-Bundle_Merge['Quality Best Case'])*quality_adj_P_max), Bundle_Merge['UD_PY_best_case_recon_amt']*(1-Bundle_Merge['Quality Best Case']*quality_adj_N_max))
    Bundle_Merge['UD_PY_worst_case_recon_amt_qual_adj']=np.where(Bundle_Merge['UD_PY_worst_case_recon_amt']>0, Bundle_Merge['UD_PY_worst_case_recon_amt']*(1-(1-Bundle_Merge['Quality Worst Case'])*quality_adj_P_max), Bundle_Merge['UD_PY_worst_case_recon_amt']*(1-Bundle_Merge['Quality Worst Case']*quality_adj_N_max))

    #output results
    
    columns=['Best Estimate','Worst Case','Best Case','Contract_type','Bundle','Item']
    bundle_cost_result= pd.DataFrame(columns=columns)
    bundle_cnt=Bundle_Payment_Contract.shape[0]

    for i in range(bundle_cnt):
    
        # output baseline result
        
        data={ 'Scenario':['Best Estimate'],
           'FFS Cost':[Bundle_Merge['PY_best_est_nocontract'][i]],
           'Savings': [0],
           'Losses': [0],
           'Net Cost':[Bundle_Merge['PY_best_est_nocontract'][i]]}
        test_best_est_nocontract=pd.DataFrame(data)
        best_est_nocontract=test_best_est_nocontract.set_index('Scenario').T
    
        data={ 'Scenario':['Worst Case'],
           'FFS Cost':[Bundle_Merge['PY_worst_case_nocontract'][i]],
           'Savings': [0],
           'Losses': [0],
           'Net Cost':[Bundle_Merge['PY_worst_case_nocontract'][i]]}
        test_worst_case_nocontract=pd.DataFrame(data)
        worst_case_nocontract=test_worst_case_nocontract.set_index('Scenario').T
    
        data={ 'Scenario':['Best Case'],
           'FFS Cost':[Bundle_Merge['PY_best_case_nocontract'][i]],
           'Savings': [0],
           'Losses': [0],
           'Net Cost':[Bundle_Merge['PY_best_case_nocontract'][i]]}
        test_best_case_nocontract=pd.DataFrame(data)
        best_case_nocontract=test_best_case_nocontract.set_index('Scenario').T
    
        result_nocontract=pd.concat([best_est_nocontract,worst_case_nocontract, best_case_nocontract], axis=1)
    
        result_nocontract['Contract_type']='FFS Contract'
        result_nocontract['Bundle']=Bundle_Merge['Bundle'][i]
        result_nocontract['Item']=['FFS Cost','Savings Paid to Provider','Losses Owed by Provider','Net Cost']
    
        # output recommended result
        
        data={ 'Scenario':['Best Estimate'],
           'FFS Cost':[Bundle_Merge['PY_best_est'][i]],
           'Savings': [max(0,Bundle_Merge['Recom_PY_best_est_recon_amt_qual_adj'][i])],
           'Losses': [min(0,Bundle_Merge['Recom_PY_best_est_recon_amt_qual_adj'][i])]}
        test_best_est=pd.DataFrame(data)
        test_best_est['Net Cost']=test_best_est['FFS Cost']+test_best_est['Savings']+test_best_est['Losses']
        recom_best_est=test_best_est.set_index('Scenario').T
    
        data={ 'Scenario':['Worst Case'],
           'FFS Cost':[Bundle_Merge['PY_worst_case'][i]],
           'Savings': [max(0,Bundle_Merge['Recom_PY_worst_case_recon_amt_qual_adj'][i])],
           'Losses': [min(0,Bundle_Merge['Recom_PY_worst_case_recon_amt_qual_adj'][i])]}
        test_worst_case=pd.DataFrame(data)
        test_worst_case['Net Cost']=test_worst_case['FFS Cost']+test_worst_case['Savings']+test_worst_case['Losses']
        recom_worst_case=test_worst_case.set_index('Scenario').T
    
        data={ 'Scenario':['Best Case'],
           'FFS Cost':[Bundle_Merge['PY_best_case'][i]],
           'Savings': [max(0,Bundle_Merge['Recom_PY_best_case_recon_amt_qual_adj'][i])],
           'Losses': [min(0,Bundle_Merge['Recom_PY_best_case_recon_amt_qual_adj'][i])]}
        test_best_case=pd.DataFrame(data)
        test_best_case['Net Cost']=test_best_case['FFS Cost']+test_best_case['Savings']+test_best_case['Losses']
        recom_best_case=test_best_case.set_index('Scenario').T
    
        result_recom=pd.concat([recom_best_est,recom_worst_case, recom_best_case], axis=1)
    
        result_recom['Contract_type']='Bundled Payment (Recommended)'
        result_recom['Bundle']=Bundle_Merge['Bundle'][i]
        result_recom['Item']=['FFS Cost','Savings Paid to Provider','Losses Owed by Provider','Net Cost']
    
        # output user defined result
    
        data={ 'Scenario':['Best Estimate'],
           'FFS Cost':[Bundle_Merge['PY_best_est'][i]],
           'Savings': [max(0,Bundle_Merge['UD_PY_best_est_recon_amt_qual_adj'][i])],
           'Losses': [min(0,Bundle_Merge['UD_PY_best_est_recon_amt_qual_adj'][i])]}
        test_best_est=pd.DataFrame(data)
        test_best_est['Net Cost']=test_best_est['FFS Cost']+test_best_est['Savings']+test_best_est['Losses']
        UD_best_est=test_best_est.set_index('Scenario').T
    
        data={ 'Scenario':['Worst Case'],
           'FFS Cost':[Bundle_Merge['PY_worst_case'][i]],
           'Savings': [max(0,Bundle_Merge['UD_PY_worst_case_recon_amt_qual_adj'][i])],
           'Losses': [min(0,Bundle_Merge['UD_PY_worst_case_recon_amt_qual_adj'][i])]}
        test_worst_case=pd.DataFrame(data)
        test_worst_case['Net Cost']=test_worst_case['FFS Cost']+test_worst_case['Savings']+test_worst_case['Losses']
        UD_worst_case=test_worst_case.set_index('Scenario').T
    
        data={ 'Scenario':['Best Case'],
           'FFS Cost':[Bundle_Merge['PY_best_case'][i]],
           'Savings': [max(0,Bundle_Merge['UD_PY_best_case_recon_amt_qual_adj'][i])],
           'Losses': [min(0,Bundle_Merge['UD_PY_best_case_recon_amt_qual_adj'][i])]}
        test_best_case=pd.DataFrame(data)
        test_best_case['Net Cost']=test_best_case['FFS Cost']+test_best_case['Savings']+test_best_case['Losses']
        UD_best_case=test_best_case.set_index('Scenario').T
    
        result_UD=pd.concat([UD_best_est,UD_worst_case, UD_best_case], axis=1)
        result_UD['Contract_type']='Bundled Payment (User Defined)'
        result_UD['Bundle']=Bundle_Merge['Bundle'][i]
        result_UD['Item']=['FFS Cost','Savings Paid to Provider','Losses Owed by Provider','Net Cost']
    
        bundle_cost_result=bundle_cost_result.append([result_nocontract, result_recom,result_UD])
        bundle_cost_result=bundle_cost_result[['Bundle','Contract_type','Item','Best Estimate','Worst Case','Best Case']]
        bundle_cost_result.reset_index()
        
    #Calculate total cost
    
    bundle_cost_result=bundle_cost_result.merge(Bundle_Payment_Contract[['Bundle','Bundle Count']],left_on='Bundle', right_on='Bundle')
    
    bundle_cost_result['Best Estimate Total']=bundle_cost_result['Best Estimate']*bundle_cost_result['Bundle Count']
    bundle_cost_result['Worst Case Total']=bundle_cost_result['Worst Case']*bundle_cost_result['Bundle Count']
    bundle_cost_result['Best Case Total']=bundle_cost_result['Best Case']*bundle_cost_result['Bundle Count']
    
    #Calculate margin
    
    bundle_cost_result=bundle_cost_result.merge(Bundle_Performance[['Bundle','FFS Margin']],left_on='Bundle', right_on='Bundle')
    
    bundle_cost_result.loc[bundle_cost_result['Item'] == 'FFS Cost', 'Best Estimate Margin'] = bundle_cost_result['Best Estimate']*bundle_cost_result['FFS Margin']
    bundle_cost_result.loc[bundle_cost_result['Item'] == 'Savings Paid to Provider', 'Best Estimate Margin'] = bundle_cost_result['Best Estimate']
    bundle_cost_result.loc[bundle_cost_result['Item'] == 'Losses Owed by Provider', 'Best Estimate Margin'] = bundle_cost_result['Best Estimate']
    for i in range(bundle_cnt*3):
        bundle_cost_result.at[3+i*4,'Best Estimate Margin']=bundle_cost_result.at[2+i*4,'Best Estimate Margin']+bundle_cost_result.at[1+i*4,'Best Estimate Margin']+bundle_cost_result.at[0+i*4,'Best Estimate Margin']

    bundle_cost_result.loc[bundle_cost_result['Item'] == 'FFS Cost', 'Worst Case Margin'] = bundle_cost_result['Worst Case']*bundle_cost_result['FFS Margin']
    bundle_cost_result.loc[bundle_cost_result['Item'] == 'Savings Paid to Provider', 'Worst Case Margin'] = bundle_cost_result['Worst Case']
    bundle_cost_result.loc[bundle_cost_result['Item'] == 'Losses Owed by Provider', 'Worst Case Margin'] = bundle_cost_result['Worst Case']
    for i in range(bundle_cnt*3):
        bundle_cost_result.at[3+i*4,'Worst Case Margin']=bundle_cost_result.at[2+i*4,'Worst Case Margin']+bundle_cost_result.at[1+i*4,'Worst Case Margin']+bundle_cost_result.at[0+i*4,'Worst Case Margin']

    bundle_cost_result.loc[bundle_cost_result['Item'] == 'FFS Cost', 'Best Case Margin'] = bundle_cost_result['Best Case']*bundle_cost_result['FFS Margin']
    bundle_cost_result.loc[bundle_cost_result['Item'] == 'Savings Paid to Provider', 'Best Case Margin'] = bundle_cost_result['Best Case']
    bundle_cost_result.loc[bundle_cost_result['Item'] == 'Losses Owed by Provider', 'Best Case Margin'] = bundle_cost_result['Best Case']
    for i in range(bundle_cnt*3):
        bundle_cost_result.at[3+i*4,'Best Case Margin']=bundle_cost_result.at[2+i*4,'Best Case Margin']+bundle_cost_result.at[1+i*4,'Best Case Margin']+bundle_cost_result.at[0+i*4,'Best Case Margin']

    bundle_cost_result['Best Estimate Margin Total']=bundle_cost_result['Best Estimate Margin']*bundle_cost_result['Bundle Count']
    bundle_cost_result['Worst Case Margin Total']=bundle_cost_result['Worst Case Margin']*bundle_cost_result['Bundle Count']
    bundle_cost_result['Best Case Margin Total']=bundle_cost_result['Best Case Margin']*bundle_cost_result['Bundle Count']
    
    #transform to output format
    
    bundle_cost_result_plan=bundle_cost_result[['Bundle','Contract_type','Item','Best Estimate','Worst Case','Best Case','Best Estimate Total','Worst Case Total','Best Case Total']]
    bundle_cost_result_plan['Category']='Plan'
    bundle_cost_result_provider=bundle_cost_result[['Bundle','Contract_type','Item','Best Estimate Margin','Worst Case Margin','Best Case Margin','Best Estimate Margin Total','Worst Case Margin Total','Best Case Margin Total']]
    bundle_cost_result_provider['Category']='Provider'
    
    for i in range(bundle_cnt*3):
        bundle_cost_result_provider.at[0+i*4,'Item']='FFS Margin'
        bundle_cost_result_provider.at[1+i*4,'Item']='Margin (Savings)'
        bundle_cost_result_provider.at[2+i*4,'Item']='Margin (Losses)'
        bundle_cost_result_provider.at[3+i*4,'Item']='Net Margin'

    bundle_cost_result_plan.columns=['Bundle','Contract_type','Item','Best Estimate','Worst Case','Best Case','Best Estimate Total','Worst Case Total','Best Case Total','Category']
    bundle_cost_result_provider.columns=['Bundle','Contract_type','Item','Best Estimate','Worst Case','Best Case','Best Estimate Total','Worst Case Total','Best Case Total','Category']

    bundle_cost_result_transformed= bundle_cost_result_plan.append([bundle_cost_result_provider])
    bundle_cost_result_transformed=bundle_cost_result_transformed[['Category','Bundle','Contract_type','Item','Best Estimate','Worst Case','Best Case','Best Estimate Total','Worst Case Total','Best Case Total']]

    return bundle_cost_result_transformed