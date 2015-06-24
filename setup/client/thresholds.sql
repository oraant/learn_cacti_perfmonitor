BEGIN
DBMS_SERVER_ALERT.SET_THRESHOLD (
metrics_id =>dbms_server_alert.HARD_PARSES_SEC,
warning_operator => DBMS_SERVER_ALERT.OPERATOR_GE,
warning_value => 10,
critical_operator => dbms_server_alert.OPERATOR_GE,
critical_value => 30,
observation_period => 1,
consecutive_occurrences => 1,
instance_name => NULL,
object_type => dbms_server_alert.OBJECT_TYPE_SYSTEM,
object_name => null);
end;
/

begin
dbms_server_alert.set_threshold(
metrics_id => dbms_server_alert.BLOCKED_USERS,
warning_operator => dbms_server_alert.OPERATOR_GE,
warning_value => 1,
critical_operator => dbms_server_alert.OPERATOR_GE,
critical_value => 2,
observation_period => 1,
consecutive_occurrences => 1,
instance_name => null,
object_type => dbms_server_alert.OBJECT_TYPE_SESSION,
object_name => null);
end;
/

begin
dbms_server_alert.set_threshold(
metrics_id => dbms_server_alert.LOGONS_CURRENT,
warning_operator => dbms_server_alert.OPERATOR_GT,
warning_value => 200,
critical_operator => dbms_server_alert.OPERATOR_GT,
critical_value => 400,
observation_period => 1,
consecutive_occurrences => 1,
instance_name => NULL,
object_type => dbms_server_alert.OBJECT_TYPE_SYSTEM,
object_name => NULL);
end;
/

BEGIN
DBMS_SERVER_ALERT.SET_THRESHOLD (
metrics_id=>DBMS_SERVER_ALERT.TABLESPACE_PCT_FULL,
warning_operator=>DBMS_SERVER_ALERT.OPERATOR_GE,
warning_value=>60,
critical_operator=>DBMS_SERVER_ALERT.OPERATOR_GE,
critical_value=>80,
observation_period=>1,
consecutive_occurrences=>1,
INSTANCE_NAME=>null,
object_type=>DBMS_SERVER_ALERT.OBJECT_TYPE_TABLESPACE,
object_name=>'SYSTEM');
END;
/

begin
dbms_server_alert.set_threshold(
metrics_id => dbms_server_alert.ENQUEUE_DEADLOCKS_SEC,
warning_operator => dbms_server_alert.OPERATOR_GT,
warning_value => 0,
critical_operator => dbms_server_alert.OPERATOR_GT,
critical_value => 0,
observation_period => 1,
consecutive_occurrences => 1,
instance_name => null,
object_type => dbms_server_alert.OBJECT_TYPE_SYSTEM,
object_name => null);
end;
/

begin
dbms_server_alert.set_threshold(
metrics_id => dbms_server_alert.PHYSICAL_READS_SEC,
warning_operator => dbms_server_alert.OPERATOR_GE,
warning_value => 30,
critical_operator => dbms_server_alert.OPERATOR_GE,
critical_value => 80,
observation_period => 1,
consecutive_occurrences => 1,
instance_name => null,
object_type => dbms_server_alert.OBJECT_TYPE_SYSTEM,
object_name => null);
end;
/

