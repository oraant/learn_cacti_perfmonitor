CREATE OR REPLACE
  FUNCTION to_file(i_target_name VARCHAR2,
                   i_param_table VARCHAR2,
                   i_file_dir    VARCHAR2,
                   i_file_name   VARCHAR2) RETURN VARCHAR2 IS
    v_file_cur    Utl_File.file_type;
    v_timestamp   NUMBER(20);
    v_param_count NUMBER;
    v_class_count NUMBER;
    v_param_name  VARCHAR2(200);
    v_value_char  VARCHAR2(100);
    temp          NUMBER;
  BEGIN
  
    --get timestamp
    SELECT (sysdate - TO_DATE('19700101', 'yyyymmdd')) * 86400 - TO_NUMBER(SUBSTR(TZ_OFFSET(sessiontimezone), 1, 3)) * 3600
    INTO v_timestamp
    FROM dual;
    

    --get max class id,and loop for all classes.
    --get max parameter id,and loop for all parameters.
    EXECUTE immediate 'select max(class_id) from ' || i_param_table INTO v_class_count;
    FOR v_temp1 IN 1 .. v_class_count LOOP
      EXECUTE immediate 'select max(param_id) from ' || i_param_table || ' where class_id = ' || v_temp1 INTO v_param_count;
      FOR v_temp2 IN 1 .. v_param_count LOOP
      

        --get the specified parameter
        EXECUTE immediate 'select param_name from ' || i_param_table || ' where class_id = ' || v_temp1 || ' and param_id = ' || v_temp2 INTO v_param_name;
        
        --virify if the parameter have value
        SELECT COUNT(*) INTO temp FROM calvalue_10min
        WHERE target_name = i_target_name
        AND param_name    = v_param_name;
        
        --if it don't have parameter value, then make it to '0'
        IF temp = 0 THEN v_value_char   := '0';
        ELSE
        
          --get parameter value,and format it if necessary.
          SELECT CASE SUBSTR(TO_CHAR(param_value), 1, 1)
                   WHEN '.' THEN '0' || TO_CHAR(param_value)
                   ELSE TO_CHAR(param_value)
                 END
          INTO v_value_char
          FROM calvalue_10min
          WHERE target_name = i_target_name
          AND param_name    = v_param_name;
          
          --Adjust the accuracy of the data
          SELECT CASE instr(v_value_char, '.')
                   WHEN 0 THEN v_value_char
                   ELSE SUBSTR(v_value_char, 0, instr(v_value_char, '.') + 2)
                 END
          INTO v_value_char FROM dual;
          
        END IF;
        
        --If it's the first loop,then open and write basic informations into the output file.
        IF v_temp1 = 1 AND v_temp2 = 1 THEN
          v_file_cur := utl_file.fopen(i_file_dir, i_file_name, 'w');
          Utl_file.putf(v_file_cur, v_timestamp || '  600  ' || '\n');
        END IF;
        
        --Write parameter value into the output file,If at the end of class,then ENTER.
        Utl_file.putf(v_file_cur, v_value_char || '  ');
        IF v_temp2 = v_param_count THEN
          Utl_file.putf(v_file_cur, '\n');
        END IF;
        
      END LOOP;
    END LOOP;
    
    --end and close the file.
    Utl_file.putf(v_file_cur, 'true' || '\n');
    utl_file.fclose(v_file_cur);
    RETURN('true');
  END to_file;
