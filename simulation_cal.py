import pandas as pd

def simulation_cal(selected_rows,domian_weight,target_user_pmpm,msr_user,mlr_user,max_user_savepct,max_user_losspct,cap_user_savepct,cap_user_losspct,twosided):
	df_range = pd.read_csv("data/quality_setup.csv")
	domain1=list(range(0,10))
	domain2=list(range(10,13))
	domain3=list(range(13,20))
	domain4=list(range(20,23))


	#selected_rows=[0,1,2,3,4,10,11]
	#domian_weight=[0.5,0.5,0,0]

	member_cnt=10000
	target_recom_pmpm=850
	msr_recom=0.02
	mlr_recom=0.02
	max_recom_savepct=0.4
	max_recom_losspct=0.4
	cap_recom_savepct=0.1
	cap_recom_losspct=0.1

	#target_user_pmpm=800
	#msr_user=0.02
	#mlr_user=0.02
	#max_user_savepct=0.4
	#max_user_losspct=0.4
	#cap_user_savepct=0.1
	#cap_user_losspct=0.1
	quality_score_recom=[0.824583333,0.67375,0.908645833,0.762083333,0.869895833]

	#twosided=False

	pmpy_mean=850*12
	pmpy_rangepct=[1,1.2,0.8,1.1,0.9] # be,worst,best,worse,better
	cost_range=[pmpy_mean*i*member_cnt for i in pmpy_rangepct]

	cost_wo_contract=864*12*member_cnt
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


	sharing_recom=[]
	sharing_user=[]
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
			if net>=0:
				if net>target*msr:
					share_pct=max_savepct*quality_score[i]
					sharing=net*share_pct
					if sharing>target*cap_savepct:
						sharing=target*cap_savepct

				else:
					sharing=0
			else:
				if twosided==True and abs(net)>target*mlr:
					sharing=net*max_losspct
					if abs(sharing)>target*cap_losspct:
						sharing=-(target*cap_losspct)

				else:
					sharing=0
			eval('sharing_'+k).append(sharing)

	df_planview_aco_totcost=pd.DataFrame(['Total Cost(before G/L share)','G/L Sharing Adj','Total Cost(after G/L share)']*3,columns=['Item'])

	df_planview_aco_totcost=df_planview_aco_totcost.reindex(columns=['Scenario','Item','Best Estimate','Worst','Best','Lower End','Higher End','Metrics'])

	df_planview_aco_totcost.iloc[[0,1,2],[2]]=[cost_wo_contract/1000/1000,0,cost_wo_contract/1000/1000]
	df_planview_aco_totcost.iloc[[3,6],2:7]=[(i/1000/1000) for i in cost_range]
	df_planview_aco_totcost.iloc[[4],2:7]=[i/1000/1000 for i in sharing_recom]
	df_planview_aco_totcost.iloc[[5],2:7]=[(cost_range[i]/1000/1000)+(sharing_recom[i]/1000/1000) for i in range(0,5)]
	df_planview_aco_totcost.iloc[[7],2:7]=[(i/1000/1000)for i in sharing_user]
	df_planview_aco_totcost.iloc[[8],2:7]=[(cost_range[i]/1000/1000)+(sharing_user[i]/1000/1000) for i in range(0,5)]
	df_planview_aco_totcost['Metrics']=["ACO's Total Cost"]*9

	df_planview_aco_pmpm=df_planview_aco_totcost.copy()
	df_planview_aco_pmpm.iloc[:,2:7]=df_planview_aco_totcost.iloc[:,2:7]*1000*1000/member_cnt/12
	df_planview_aco_pmpm['Item']=['PMPM(before G/L share)','G/L Sharing Adj','PMPM(after G/L share)']*3
	df_planview_aco_pmpm['Metrics']=["ACO's PMPM"]*9

	df_planview_plan_totcost=df_planview_aco_totcost.copy()
	df_planview_plan_totcost.iloc[[0,2,3,5,6,8],2:7]=df_planview_aco_totcost.iloc[[0,2,3,5,6,8],2:7]+outof_aco_cost/1000/1000
	df_planview_plan_totcost['Metrics']=["Plan's Total Cost"]*9


	df_acoview_totrev=df_planview_aco_totcost.copy()
	df_acoview_totrev['Item']=['Total Revenue(before G/L share)','G/L Sharing Adj','Total Revenue(after G/L share)']*3
	df_acoview_totrev['Metrics']=["ACO's Total Revenue"]*9

	df_acoview_margin=df_acoview_totrev.copy()
	df_acoview_margin.iloc[[0,3,6],2:7]=df_acoview_totrev.iloc[[0,3,6],2:7]*aco_margin
	margin_aft=df_acoview_margin.iloc[[0,3,6],2:7].reset_index(drop=True)+df_acoview_margin.iloc[[1,4,7],2:7].reset_index(drop=True)
	margin_aft['index']=[2,5,8]
	margin_aft=margin_aft.set_index(['index'])
	df_acoview_margin.iloc[[2,5,8],2:7]=margin_aft
	df_acoview_margin['Item']=['Margin(before G/L share)','G/L Sharing Adj','Margin(after G/L share)']*3
	df_acoview_margin['Metrics']=["ACO's Margin"]*9

	df_acoview_margin_pct=df_acoview_margin.copy()
	df_acoview_margin_pct.iloc[[0,1,2],2:7]=df_acoview_margin.iloc[[0,1,2],2:7]/df_acoview_totrev.iloc[[2],2:7].values[0]*100
	df_acoview_margin_pct.iloc[[3,4,5],2:7]=df_acoview_margin.iloc[[3,4,5],2:7]/df_acoview_totrev.iloc[[5],2:7].values[0]*100
	df_acoview_margin_pct.iloc[[6,7,8],2:7]=df_acoview_margin.iloc[[6,7,8],2:7]/df_acoview_totrev.iloc[[8],2:7].values[0]*100
	df_acoview_margin_pct['Item']=['Margin %(before G/L share)','G/L Sharing Adj','Margin %(after G/L share)']*3
	df_acoview_margin_pct['Metrics']=["ACO's Margin %"]*9





	df=pd.concat([df_planview_aco_totcost,df_planview_aco_pmpm,df_planview_plan_totcost,df_acoview_totrev,df_acoview_margin,df_acoview_margin_pct])

	return df
