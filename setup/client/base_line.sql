--the name of base line must be 'perfbl'

select * from dba_hist_snapshot order by snap_id desc;

select * from (select snap_id from dba_hist_snapshot  order by snap_id desc) where rownum < 10;

begin
 DBMS_WORKLOAD_REPOSITORY.CREATE_BASELINE(start_snap_id => 1822,end_snap_id => 1831,baseline_name => 'perfbl');
end;
/


begin
 dbms_workload_repository.drop_baseline(baseline_name => 'perfbl',cascade => false);
end;
/
