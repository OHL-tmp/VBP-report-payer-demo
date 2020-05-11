import pandas as pd

def simulation_cal(selected_rows,domian_weight,df_json,target_user_pmpm,msr_user,mlr_user,max_user_savepct,max_user_losspct,cap_user_savepct,cap_user_losspct,twosided):
	df_range = pd.read_csv("data/quality_setup.csv")
	domain1=list(range(0,10))
	domain2=list(range(10,14))
	domain3=list(range(14,20))
	domain4=list(range(20,23))

	member_cnt=int(df_json['medical cost target']['member count']) #10000
	target_recom_pmpm=int(df_json['medical cost target']['recom target'].replace('$',''))#850
	msr_recom=int(df_json['savings/losses sharing arrangement']['recom msr'].replace('%',''))/100#0.02
	mlr_recom=int(df_json['savings/losses sharing arrangement']['recom mlr'].replace('%',''))/100#0.02
	max_recom_savepct=int(df_json['savings/losses sharing arrangement']['recom savings sharing'].replace('%',''))/100#0.4
	max_recom_losspct=int(df_json['savings/losses sharing arrangement']['recom losses sharing'].replace('%',''))/100#0.4
	
	cap_recom_savepct_position=df_json['savings/losses sharing arrangement']['recom savings share cap'].find('%')
	cap_recom_savepct=int(df_json['savings/losses sharing arrangement']['recom savings share cap'][0:cap_recom_savepct_position])/100#0.1
	
	cap_recom_losspct_position=df_json['savings/losses sharing arrangement']['recom losses share cap'].find('%')
	cap_recom_losspct=int(df_json['savings/losses sharing arrangement']['recom losses share cap'][0:cap_recom_losspct_position])/100#0.1

	quality_score_recom=[0.824583333,0.67375,0.908645833,0.762083333,0.869895833]

	pmpy_mean=850*12
	pmpy_rangepct=[1,1.2,0.8,1.1,0.9] # be,worst,best,worse,better
	cost_range=[pmpy_mean*i*member_cnt for i in pmpy_rangepct]

	cost_wo_contract=864*12
	cost_wo_contract_range=[cost_wo_contract*i*member_cnt for i in pmpy_rangepct]

	outof_aco_cost=cost_wo_contract*6
	aco_margin=0.05

	target_recom=target_recom_pmpm*12*member_cnt
	target_user=target_user_pmpm*12*member_cnt

	k=0
	for i in range(1,5):
		domain=eval('domain'+str(i))
		selected_indomain=[ j in domain for j in  selected_rows]
		if True in selected_indomain:
			k=k+1
			selected_index=[j for j, e in enumerate(selected_indomain) if e == True]
			selected_eachdomain=[selected_rows[j] for j in selected_index]
			df_filtered=df_range[df_range['id'].isin (selected_eachdomain)][df_range.columns[11:]]
			if k==1:
				quality_score_user=df_filtered.sum()/(len(df_filtered)*2)*domian_weight[i-1]
			else:
				quality_score_user=quality_score_user+df_filtered.sum()/(len(df_filtered)*2)*domian_weight[i-1]

	sharing_gain_recom=[]
	sharing_loss_recom=[]
	sharing_gain_user=[]
	sharing_loss_user=[]
	for k in ['recom','user']:
		target=eval('target_'+k)
		msr=eval('msr_'+k)
		mlr=eval('mlr_'+k)
		max_savepct=eval('max_'+k+'_savepct')
		max_losspct=eval('max_'+k+'_losspct')
		cap_savepct=eval('cap_'+k+'_savepct')
		cap_losspct=eval('cap_'+k+'_losspct')
		quality_score=eval('quality_score_'+k)
		for i in range(0,5):
			net=target-cost_range[i]

			eval('sharing_gain_'+k).append(0)
			eval('sharing_loss_'+k).append(0)

			if net>=0:
				if net>target*msr:
					share_pct=max_savepct*quality_score[i]
					sharing=net*share_pct
					if sharing>target*cap_savepct:
						sharing=target*cap_savepct

				else:
					sharing=0

				eval('sharing_gain_'+k)[i]=sharing


			else:
				if twosided==True and abs(net)>target*mlr:
					sharing=net*max_losspct
					if abs(sharing)>target*cap_losspct:
						sharing=-(target*cap_losspct)

				else:
					sharing=0

				eval('sharing_loss_'+k)[i]=sharing
			

	df_planview_aco_totcost=pd.DataFrame(['Total Cost(before G/L share)','Gain Sharing','Loss Sharing','Total Cost(after G/L share)']*3,columns=['Item'])

	df_planview_aco_totcost=df_planview_aco_totcost.reindex(columns=['Scenario','Item','Best Estimate','Worst','Best','Lower End','Higher End','Metrics'])

	df_planview_aco_totcost.iloc[[0,3],2:7]=[(i/1000/1000) for i in cost_wo_contract_range]
	df_planview_aco_totcost.iloc[[4,8],2:7]=[(i/1000/1000) for i in cost_range]
	df_planview_aco_totcost.iloc[[5],2:7]=[i/1000/1000 for i in sharing_gain_recom]
	df_planview_aco_totcost.iloc[[9],2:7]=[(i/1000/1000)for i in sharing_gain_user]
	if twosided:
		df_planview_aco_totcost.iloc[[6],2:7]=[i/1000/1000 for i in sharing_loss_recom]
		df_planview_aco_totcost.iloc[[7],2:7]=[(cost_range[i]/1000/1000)+(sharing_gain_recom[i]/1000/1000)+(sharing_loss_recom[i]/1000/1000) for i in range(0,5)]
		df_planview_aco_totcost.iloc[[10],2:7]=[i/1000/1000 for i in sharing_loss_user]
		df_planview_aco_totcost.iloc[[11],2:7]=[(cost_range[i]/1000/1000)+(sharing_gain_user[i]/1000/1000)+(sharing_loss_user[i]/1000/1000) for i in range(0,5)]

	else:
		df_planview_aco_totcost.iloc[[7],2:7]=[(cost_range[i]/1000/1000)+(sharing_gain_recom[i]/1000/1000) for i in range(0,5)]
		df_planview_aco_totcost.iloc[[11],2:7]=[(cost_range[i]/1000/1000)+(sharing_gain_user[i]/1000/1000) for i in range(0,5)]
	
	
	df_planview_aco_totcost['Metrics']=["ACO's Total Cost"]*12

	df_planview_aco_pmpm=df_planview_aco_totcost.copy()
	df_planview_aco_pmpm.iloc[:,2:7]=df_planview_aco_totcost.iloc[:,2:7]*1000*1000/member_cnt/12
	df_planview_aco_pmpm['Item']=['PMPM(before G/L share)','Gain Sharing','Loss Sharing','PMPM(after G/L share)']*3
	df_planview_aco_pmpm['Metrics']=["ACO's PMPM"]*12

	df_planview_plan_totcost=df_planview_aco_totcost.copy()
	df_planview_plan_totcost.iloc[[0,3,4,7,8,11],2:7]=df_planview_aco_totcost.iloc[[0,3,4,7,8,11],2:7]+outof_aco_cost/1000/1000
	df_planview_plan_totcost['Metrics']=["Plan's Total Cost"]*12


	df_acoview_totrev=df_planview_aco_totcost.copy()
	df_acoview_totrev['Item']=['Total Revenue(before G/L share)','Gain Sharing','Loss Sharing','Total Revenue(after G/L share)']*3
	df_acoview_totrev['Metrics']=["ACO's Total Revenue"]*12

	df_acoview_margin=df_acoview_totrev.copy()
	df_acoview_margin.iloc[[0,4,8],2:7]=df_acoview_totrev.iloc[[0,4,8],2:7]*aco_margin
	if twosided:
		margin_aft=df_acoview_margin.iloc[[0,4,8],2:7].reset_index(drop=True)+df_acoview_margin.iloc[[1,5,9],2:7].fillna(0).reset_index(drop=True)+df_acoview_margin.iloc[[2,6,10],2:7].fillna(0).reset_index(drop=True)
	else:
		margin_aft=df_acoview_margin.iloc[[0,4,8],2:7].reset_index(drop=True)+df_acoview_margin.iloc[[1,5,9],2:7].fillna(0).reset_index(drop=True)
	margin_aft['index']=[3,7,11]
	margin_aft=margin_aft.set_index(['index'])
	df_acoview_margin.iloc[[3,7,11],2:7]=margin_aft
	df_acoview_margin['Item']=['Margin(before G/L share)','Gain Sharing','Loss Sharing','Margin(after G/L share)']*3
	df_acoview_margin['Metrics']=["ACO's Margin"]*12

	df_acoview_margin_pct=df_acoview_margin.copy()
	df_acoview_margin_pct.iloc[[0,1,2,3],2:7]=df_acoview_margin.iloc[[0,1,2,3],2:7]/df_acoview_totrev.iloc[[3],2:7].values[0]*100
	df_acoview_margin_pct.iloc[[4,5,6,7],2:7]=df_acoview_margin.iloc[[4,5,6,7],2:7]/df_acoview_totrev.iloc[[7],2:7].values[0]*100
	df_acoview_margin_pct.iloc[[8,9,10,11],2:7]=df_acoview_margin.iloc[[8,9,10,11],2:7]/df_acoview_totrev.iloc[[11],2:7].values[0]*100
	df_acoview_margin_pct['Item']=['Margin %(before G/L share)','Gain Sharing','Loss Sharing','Margin %(after G/L share)']*3
	df_acoview_margin_pct['Metrics']=["ACO's Margin %"]*12

	df=pd.concat([df_planview_aco_totcost,df_planview_aco_pmpm,df_planview_plan_totcost,df_acoview_totrev,df_acoview_margin,df_acoview_margin_pct])

	return df
