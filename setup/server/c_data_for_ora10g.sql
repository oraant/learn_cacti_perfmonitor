--Drop the old datas
delete from parameter_oracle10g;
commit;

--DB
insert /*+append*/ into parameter_oracle10g values (1,1,'DB',1,'DB time','aggregate','60000000');
insert /*+append*/ into parameter_oracle10g values (2,1,'DB',2,'logons current','current','1');
insert /*+append*/ into parameter_oracle10g values (3,1,'DB',3,'user rollbacks','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (4,1,'DB',4,'transaction rollbacks','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (5,1,'DB',5,'user calls','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (6,1,'DB',6,'user commits','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (7,1,'DB',7,'db block changes','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (8,1,'DB',8,'execute count','aggregate','600');
commit;

--Parse
insert /*+append*/ into parameter_oracle10g values (9,2,'Parse',1,'parse time elapsed','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (10,2,'Parse',2,'parse time cpu','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (11,2,'Parse',3,'parse count (hard)','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (12,2,'Parse',4,'session cursor cache count','current','600');
insert /*+append*/ into parameter_oracle10g values (13,2,'Parse',5,'session cursor cache hits','current','600');
insert /*+append*/ into parameter_oracle10g values (14,2,'Parse',6,'parse count (failures)','aggregate','600');
commit;

--CPU
insert /*+append*/ into parameter_oracle10g values (15,3,'CPU',1,'CPU used by this session','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (16,3,'CPU',2,'consistent gets','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (17,3,'CPU',3,'session logical reads','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (18,3,'CPU',4,'read by other session','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (19,3,'CPU',5,'db block gets','aggregate','600');
commit;

--IO-reads
insert /*+append*/ into parameter_oracle10g values (20,4,'IO-reads',1,'physical read total IO requests','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (21,4,'IO-reads',2,'physical reads','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (22,4,'IO-reads',3,'physical reads direct','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (23,4,'IO-reads',4,'physical read total multi block requests','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (24,4,'IO-reads',5,'db file scattered read','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (25,4,'IO-reads',6,'physical reads direct temporary tablespace','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (26,4,'IO-reads',7,'physical read total bytes','aggregate','629145600');
insert /*+append*/ into parameter_oracle10g values (27,4,'IO-reads',8,'db file sequential read','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (28,4,'IO-reads',9,'db file parallel read','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (29,4,'IO-reads',10,'index fast full scans (full)','aggregate','600');
commit;

--IO-writes
insert /*+append*/ into parameter_oracle10g values (30,5,'IO-writes',1,'physical writes','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (31,5,'IO-writes',2,'physical writes direct','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (32,5,'IO-writes',3,'physical write total bytes','aggregate','629145600');
insert /*+append*/ into parameter_oracle10g values (33,5,'IO-writes',4,'physical write total IO requests','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (34,5,'IO-writes',5,'physical writes direct temporary tablespace','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (35,5,'IO-writes',6,'physical writes from cache','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (36,5,'IO-writes',7,'physical write total multi block requests','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (37,5,'IO-writes',8,'physical writes direct (lob)','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (38,5,'IO-writes',9,'lob writes','aggregate','600');
commit;

--IO-other
insert /*+append*/ into parameter_oracle10g values (39,6,'IO-others',1,'direct path read temp','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (40,6,'IO-others',2,'Log archive I/O','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (41,6,'IO-others',3,'direct path write temp','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (42,6,'IO-others',4,'Datapump dump file I/O','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (43,6,'IO-others',5,'db file parallel write','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (44,6,'IO-others',6,'lob reads','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (45,6,'IO-others',7,'physical reads direct (lob)','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (46,6,'IO-others',8,'physical reads cache','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (47,6,'IO-others',9,'RMAN backup '||chr(38)||' recovery I/O','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (48,6,'IO-others',10,'direct path read','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (49,6,'IO-others',11,'direct path write','aggregate','600');
commit;

--Sorts
insert /*+append*/ into parameter_oracle10g values (50,7,'Sorts',1,'sorts (disk)','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (51,7,'Sorts',2,'workarea executions - onepass','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (52,7,'Sorts',3,'workarea executions - multipass','aggregate','600');

--Lock
insert /*+append*/ into parameter_oracle10g values (53,8,'Lock',1,'enqueue waits','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (54,8,'Lock',2,'enq: TX - row lock contention','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (55,8,'Lock',3,'concurrency wait time','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (56,8,'Lock',4,'enq: TM - contention','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (57,8,'Lock',5,'enq: TX - allocate ITL entry','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (58,8,'Lock',6,'enqueue deadlocks','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (59,8,'Lock',7,'enq: HW - contention','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (60,8,'Lock',8,'enq: TX - index contention','aggregate','1');
commit;

--WAITTIME
insert /*+append*/ into parameter_oracle10g values (61,9,'WAITTIME',1,'application wait time','aggregate','100');
insert /*+append*/ into parameter_oracle10g values (62,9,'WAITTIME',2,'cluster wait time','aggregate','100');
insert /*+append*/ into parameter_oracle10g values (63,9,'WAITTIME',3,'non-idle wait time','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (64,9,'WAITTIME',4,'user I/O wait time','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (65,9,'WAITTIME',5,'scheduler wait time','aggregate','100');

--Cluster
insert /*+append*/ into parameter_oracle10g values (66,10,'Cluster',1,'gc current blocks received','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (67,10,'Cluster',2,'gc current blocks served','aggregate','10');
insert /*+append*/ into parameter_oracle10g values (68,10,'Cluster',3,'gc read waits','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (69,10,'Cluster',4,'gc current block receive time','aggregate','100');
insert /*+append*/ into parameter_oracle10g values (70,10,'Cluster',5,'gc current block send time','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (71,10,'Cluster',6,'gc read wait time','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (72,10,'Cluster',7,'gc cr blocks received','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (73,10,'Cluster',8,'gc cr blocks served','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (74,10,'Cluster',9,'gc read wait timeouts','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (75,10,'Cluster',10,'gc cr block receive time','aggregate','100');
insert /*+append*/ into parameter_oracle10g values (76,10,'Cluster',11,'gc cr block send time','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (77,10,'Cluster',12,'gc read wait failures','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (78,10,'Cluster',13,'global enqueue get time','aggregate','100');
commit;

--Buffer Cache
insert /*+append*/ into parameter_oracle10g values (79,11,'BufferCache',1,'latch: cache buffers chains','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (80,11,'BufferCache',2,'free buffer requested','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (81,11,'BufferCache',3,'free buffer inspected','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (82,11,'BufferCache',4,'buffer busy waits','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (83,11,'BufferCache',5,'free buffer waits','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (84,11,'BufferCache',6,'dirty buffers inspected','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (85,11,'BufferCache',7,'CR blocks created','aggregate','1');
commit;

--Redo Log
insert /*+append*/ into parameter_oracle10g values (86,12,'REDO',1,'redo size','aggregate','614400');
insert /*+append*/ into parameter_oracle10g values (87,12,'REDO',2,'log file sync','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (88,12,'REDO',3,'latch: redo allocation','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (89,12,'REDO',4,'redo writes','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (90,12,'REDO',5,'redo synch writes','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (91,12,'REDO',6,'log file switch (checkpoint incomplete)','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (92,12,'REDO',7,'redo write time','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (93,12,'REDO',8,'redo synch time','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (94,12,'REDO',9,'log file switch (archiving needed)','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (95,12,'REDO',10,'redo synch time overhead count (<2 msec)','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (96,12,'REDO',11,'redo synch time overhead count (<8 msec)','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (97,12,'REDO',12,'redo synch time overhead count (<32 msec)','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (98,12,'REDO',13,'redo synch time overhead count (<128 msec)','aggregate','1000');
insert /*+append*/ into parameter_oracle10g values (99,12,'REDO',14,'redo synch time overhead count (>=128 msec)','aggregate','1000');

--Undo
insert /*+append*/ into parameter_oracle10g values (100,13,'UNDO',1,'auto extends on undo tablespace','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (101,13,'UNDO',2,'undo segment extension','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (102,13,'UNDO',3,'undo segment tx slot','aggregate','1');

--Table ACCESS
insert /*+append*/ into parameter_oracle10g values (103,14,'TABLE_ACCESS',1,'table scans (short tables)','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (104,14,'TABLE_ACCESS',2,'table scan blocks gotten','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (105,14,'TABLE_ACCESS',3,'table fetch continued row','aggregate','600');
insert /*+append*/ into parameter_oracle10g values (106,14,'TABLE_ACCESS',4,'table scans (long tables)','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (107,14,'TABLE_ACCESS',5,'table scans (rowid ranges)','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (108,14,'TABLE_ACCESS',6,'table scans (direct read)','aggregate','1');
commit;

--Index DML
insert /*+append*/ into parameter_oracle10g values (109,15,'INDEX_DML',1,'leaf node splits','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (110,15,'INDEX_DML',2,'branch node splits','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (111,15,'INDEX_DML',3,'root node splits','aggregate','1');

--Parallel
insert /*+append*/ into parameter_oracle10g values (112,16,'Parallel',1,'queries parallelized','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (113,16,'Parallel',2,'DML statements parallelized','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (114,16,'Parallel',3,'DDL statements parallelized','aggregate','1');

--Net
insert /*+append*/ into parameter_oracle10g values (115,17,'Net',1,'SQL*Net roundtrips to/from client','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (116,17,'Net',2,'SQL*Net roundtrips to/from dblink','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (117,17,'Net',3,'SQL*Net break/reset to dblink','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (118,17,'Net',4,'bytes received via SQL*Net from client','aggregate','1048576');
insert /*+append*/ into parameter_oracle10g values (119,17,'Net',5,'bytes received via SQL*Net from dblink','aggregate','1048576');
insert /*+append*/ into parameter_oracle10g values (120,17,'Net',6,'SQL*Net message from dblink','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (121,17,'Net',7,'bytes sent via SQL*Net to client','aggregate','1048576');
insert /*+append*/ into parameter_oracle10g values (122,17,'Net',8,'bytes sent via SQL*Net to dblink','aggregate','1048576');
insert /*+append*/ into parameter_oracle10g values (123,17,'Net',9,'SQL*Net message to dblink','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (124,17,'Net',10,'SQL*Net more data from client','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (125,17,'Net',11,'SQL*Net more data from dblink','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (126,17,'Net',12,'SQL*Net break/reset to client','aggregate','1');
commit;

--SWAP
insert /*+append*/ into parameter_oracle10g values (127,18,'SWAP',1,'OS Page faults','aggregate','10');
insert /*+append*/ into parameter_oracle10g values (128,18,'SWAP',2,'OS Swaps','aggregate','10');


--SGA-PGA
insert /*+append*/ into parameter_oracle10g values (129,19,'SGA-PGA',1,'buffer_cache','current','1073741824');
insert /*+append*/ into parameter_oracle10g values (130,19,'SGA-PGA',2,'maximum PGA allocated','current','1073741824');
insert /*+append*/ into parameter_oracle10g values (131,19,'SGA-PGA',3,'max processes count','current','1');
insert /*+append*/ into parameter_oracle10g values (132,19,'SGA-PGA',4,'shared pool','current','1073741824');
insert /*+append*/ into parameter_oracle10g values (133,19,'SGA-PGA',5,'total PGA allocated','current','1');
insert /*+append*/ into parameter_oracle10g values (134,19,'SGA-PGA',6,'process count','current','1');
insert /*+append*/ into parameter_oracle10g values (135,19,'SGA-PGA',7,'large pool','current','1');
insert /*+append*/ into parameter_oracle10g values (136,19,'SGA-PGA',8,'extra bytes read/written','current','1');
commit;

--EVENT-GC
insert /*+append*/ into parameter_oracle10g values (137,20,'EVENT-GC',1,'gc current block 2-way','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (138,20,'EVENT-GC',2,'gc cr block 2-way','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (139,20,'EVENT-GC',3,'gc current block congested','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (140,20,'EVENT-GC',4,'gc current block busy','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (141,20,'EVENT-GC',5,'gc cr block busy','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (142,20,'EVENT-GC',6,'gc cr block congested','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (143,20,'EVENT-GC',7,'gc cr multi block request','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (144,20,'EVENT-GC',8,'gc current multi block request','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (145,20,'EVENT-GC',9,'global cache busy','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (146,20,'EVENT-GC',10,'gc buffer busy','aggregate','1');
commit;

--Share Pool
insert /*+append*/ into parameter_oracle10g values (147,21,'SHAREDPOOL',1,'cursor: pin S','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (148,21,'SHAREDPOOL',2,'cursor: pin S wait on X','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (149,21,'SHAREDPOOL',3,'library cache lock','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (150,21,'SHAREDPOOL',4,'cursor: pin X','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (151,21,'SHAREDPOOL',5,'latch: shared pool','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (152,21,'SHAREDPOOL',6,'library cache pin','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (153,21,'SHAREDPOOL',7,'cursor: mutex S','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (154,21,'SHAREDPOOL',8,'latch free','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (155,21,'SHAREDPOOL',9,'library cache: mutex X','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (156,21,'SHAREDPOOL',10,'cursor: mutex X','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (157,21,'SHAREDPOOL',11,'latch: row cache objects','aggregate','1');
insert /*+append*/ into parameter_oracle10g values (158,21,'SHAREDPOOL',12,'library cache: mutex S','aggregate','1');
commit;
