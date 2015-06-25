--the name of base line must be 'perfbl'

select * from dba_hist_snapshot order by snap_id desc;

select snap_id from dba_hist_snapshot where rownum < 10 order by snap_id desc;

begin
 DBMS_WORKLOAD_REPOSITORY.CREATE_BASELINE(start_snap_id => 1822,end_snap_id => 1831,baseline_name => 'perfbl');
end;
/


begin
 dbms_workload_repository.drop_baseline(baseline_name => 'perfbl',cascade => true);
end;
/
