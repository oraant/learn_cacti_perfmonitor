
create or replace directory oracle11g as '/cismon/datas/oracle11g';
create or replace directory oracle10g as '/cismon/datas/oracle10g';


CREATE SMALLFILE TABLESPACE "MONITOR" DATAFILE '/oradata/db11g/monitort01.dbf' SIZE 514M AUTOEXTEND ON NEXT 128M MAXSIZE 
UNLIMITED nologging EXTENT MANAGEMENT LOCAL SEGMENT SPACE MANAGEMENT AUTO;


drop table parameter_oracle10g;
CREATE TABLE parameter_oracle10g
  (
    entry_id   NUMBER NOT NULL,
    class_id   NUMBER NOT NULL,
    class_name VARCHAR2(100) NOT NULL,
    param_id   NUMBER NOT NULL,  
    param_name VARCHAR2(100) NOT NULL,
    param_type VARCHAR2(100) NOT NULL,
    divisor    NUMBER NOT NULL,
    CONSTRAINT PK_PARAM_ORA10G PRIMARY KEY (entry_id)
  )
  TABLESPACE MONITOR;


drop table parameter_oracle11g;
CREATE TABLE parameter_oracle11g
  (
    entry_id   NUMBER NOT NULL,
    class_id   NUMBER NOT NULL,
    class_name VARCHAR2(100) NOT NULL,
    param_id   NUMBER NOT NULL,
    param_name VARCHAR2(100) NOT NULL,
    param_type VARCHAR2(100) NOT NULL,
    divisor    NUMBER NOT NULL,
    CONSTRAINT PK_PARAM_ORA11G PRIMARY KEY (entry_id)
  )
  TABLESPACE MONITOR;


drop table rawdata_10min;
CREATE TABLE rawdata_10min
  (
    target_name VARCHAR2(100) NOT NULL,
    param_name  VARCHAR2(100) NOT NULL,
    param_value NUMBER NOT NULL
  )
  TABLESPACE MONITOR;


drop table rawdata_10min_last;
CREATE TABLE rawdata_10min_last
  (
    target_name VARCHAR2(100) NOT NULL,
    param_name  VARCHAR2(100) NOT NULL,
    param_value NUMBER NOT NULL
  )
  TABLESPACE MONITOR;


drop table rawdata_arch;
CREATE TABLE rawdata_arch
  (
    update_time DATE NOT NULL,
    frequence   VARCHAR2(100) NOT NULL,
    target_name VARCHAR2(100) NOT NULL,
    param_name  VARCHAR2(100) NOT NULL,
    param_value NUMBER NOT NULL
  )
  TABLESPACE MONITOR
  PARTITION BY range (update_time) interval(numtoyminterval(1,'MONTH'))
                       (PARTITION p2 VALUES LESS THAN (TO_DATE('2015-06-1', 'YYYY-MM-DD')),
                         PARTITION p3 VALUES LESS THAN (TO_DATE('2015-07-01', 'YYYY-MM-DD')));



drop table calvalue_10min;
CREATE TABLE calvalue_10min
  (
    target_name VARCHAR2(100) NOT NULL,
    param_name  VARCHAR2(100) NOT NULL,
    param_value NUMBER NOT NULL
  )
  TABLESPACE MONITOR;


drop table calvalue_arch;
CREATE TABLE calvalue_arch
  (
    update_time DATE NOT NULL,
    frequence   VARCHAR2(100) NOT NULL,
    target_name VARCHAR2(100) NOT NULL,
    param_name  VARCHAR2(100) NOT NULL,
    param_value NUMBER NOT NULL
  )
  TABLESPACE MONITOR
  PARTITION BY range (update_time) interval(numtoyminterval(1,'MONTH'))
                       (PARTITION p2 VALUES LESS THAN (TO_DATE('2015-06-1', 'YYYY-MM-DD')),
                         PARTITION p3 VALUES LESS THAN (TO_DATE('2015-07-01', 'YYYY-MM-DD')));
