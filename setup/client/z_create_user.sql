create user cismon identified by cismon;
grant connect to cismon;

--history
grant select on dba_hist_snapshot to cismon;
grant select on DBA_HIST_SYS_TIME_MODEL to cismon;
grant select on DBA_HIST_PGASTAT to cismon;
grant select on DBA_HIST_SYSSTAT to cismon;
grant select on DBA_HIST_MEM_DYNAMIC_COMP to cismon; 
grant select on DBA_HIST_SGASTAt to cismon;
grant select on dba_hist_seg_stat to cismon;
grant select on dba_hist_sqlstat to cismon;
grant select on dba_hist_system_event to cismon;
grant select on dba_hist_seg_stat_obj to cismon;
grant select on dba_hist_sqltext to cismon; 

--monitor
grant select on dba_tablespace_usage_metrics to cismon;
grant select on v_$asm_diskgroup to cismon;
grant select on gv_$pgastat to cismon;
grant select on gv_$sga_dynamic_components to cismon;
grant select on gv_$sysstat to cismon;
grant select on gv_$system_event to cismon;
grant select on gv_$sys_time_model to cismon;
grant select on v_$sysstat to cismon;
grant select on v_$pgastat to cismon;
grant select on v_$sga_dynamic_components to cismon;
grant select on v_$sys_time_model to cismon;
grant select on v_$system_event to cismon;

--AWR
grant select on dba_hist_parameter to cismon;
grant select on dba_hist_database_instance to cismon;
grant select on v_$instance to cismon;
grant select on v_$database to cismon;
grant select on dba_hist_baseline to cismon;
grant EXECUTE on dbms_workload_repository to cismon;


--ASH
grant select on dba_hist_active_sess_history to cismon;
grant select on dba_hist_ash_snapshot to cismon;
grant select on v_$active_session_history to cismon;
grant select on v_$SESSION to cismon;
grant select on V_$SQL to cismon;
grant select on V_$ACTIVE_SERVICES to cismon;
grant select on V_$EVENT_NAME to cismon;
grant EXECUTE on DBMS_LOB to cismon;
grant EXECUTE on DBMS_SQL to cismon;
grant EXECUTE on DBMS_SWRF_REPORT_INTERNAL to cismon;
grant EXECUTE on DBMS_WORKLOAD_REPOSITORY to cismon;

--sql adviser
grant ADVISOR to cismon;
GRANT CREATE ANY PROCEDURE TO cismon;

--threshold
grant all on sys.dba_outstanding_alerts to cismon;
grant all on sys.dba_alert_history to cismon;

--verify
grant all on sys.v_$database to cismon;
grant all on sys.v_$instance to cismon;

--tbs and asmdg
grant all on sys.dba_data_files to cismon;
grant all on sys.dba_free_space to cismon;
grant all on sys.dba_temp_files to cismon;
grant all on sys.v_$temp_space_header to cismon;
grant all on sys.v_$asm_diskgroup to cismon;
