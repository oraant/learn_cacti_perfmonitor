create or replace function to_file(i_target_name varchar2,
                                   i_param_table varchar2,
                                   i_file_dir    varchar2,
                                   i_file_name   varchar2) return varchar2 is
  v_file_cur  Utl_File.file_type;
  v_timestamp number(20);

  v_param_count number;

  v_class_count number;

  v_param_name varchar2(200);
  v_value_char varchar2(100);

  temp number;

begin

  select (sysdate - TO_DATE('19700101', 'yyyymmdd')) * 86400 -
         TO_NUMBER(SUBSTR(TZ_OFFSET(sessiontimezone), 1, 3)) * 3600
    into v_timestamp
    from dual;

  execute immediate 'select max(class_id) from ' || i_param_table
    into v_class_count;

  for v_temp1 in 1 .. v_class_count loop
  
    execute immediate 'select max(param_id) from ' || i_param_table ||
                      ' where class_id = ' || v_temp1
      into v_param_count;
  
    for v_temp2 in 1 .. v_param_count loop
    
      execute immediate 'select param_name from ' || i_param_table ||
                        ' where class_id = ' || v_temp1 ||
                        ' and param_id = ' || v_temp2
        into v_param_name;
    
      select count(*)
        into temp
        from calvalue_10min
       where target_name = i_target_name
         and param_name = v_param_name;
      if temp = 0 then
        v_value_char := '0';
      else
      
        select case substr(to_char(param_value), 1, 1)
                 when '.' then
                  '0' || to_char(param_value)
                 else
                  to_char(param_value)
               end
          into v_value_char
          from calvalue_10min
         where target_name = i_target_name
           and param_name = v_param_name;
      
        select case instr(v_value_char, '.')
                 when 0 then
                  v_value_char
                 else
                  substr(v_value_char, 0, instr(v_value_char, '.') + 2)
               end
          into v_value_char
          from dual;
      end if;
    
      if v_temp1 = 1 and v_temp2 = 1 then
      
        v_file_cur := utl_file.fopen(i_file_dir, i_file_name, 'w');
      
        Utl_file.putf(v_file_cur, v_timestamp || '  600  ' || '\n');
      
      end if;
    
      Utl_file.putf(v_file_cur, v_value_char || '  ');
      if v_temp2 = v_param_count then
        Utl_file.putf(v_file_cur, '\n');
      end if;
    
    end loop;
  end loop;
  Utl_file.putf(v_file_cur, 'true' || '\n');
  utl_file.fclose(v_file_cur);

  return('true');
end to_file;
/
