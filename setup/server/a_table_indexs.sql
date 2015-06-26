drop index ind_rawdata_last_tn;
drop index ind_PARAMETER_ORACLE10G_pn;        
drop index ind_PARAMETER_ORACLE11G_pn; 
drop index ind_rawdata_target_name;
drop index ind_calvalue_tn;
drop index ind_alert_tn;
drop index ind_alert_tn_pn;
drop index ind_calvalue_arch_update_time;
create index ind_rawdata_last_tn on rawdata_10min_last(target_name);
create index ind_PARAMETER_ORACLE10G_pn on PARAMETER_ORACLE11G(param_type);             
create index ind_PARAMETER_ORACLE11G_pn on PARAMETER_ORACLE10G(param_type);
create index ind_rawdata_target_name on rawdata_10min(target_name);
create index ind_calvalue_tn on calvalue_10min(target_name);
create index ind_alert_tn on alert_10min(target_name);
create index ind_alert_tn_pn on alert_10min(target_name, param_name);
create index ind_calvalue_arch_update_time on calvalue_arch(update_time);

