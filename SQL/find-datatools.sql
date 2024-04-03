-- used to find instances of DataTools databases

declare @sql varchar(max);
DECLARE @dbName varchar(256);
DECLARE dbNameCursor CURSOR FOR
SELECT name FROM sys.databases;
OPEN dbNameCursor;
FETCH NEXT FROM dbNameCursor INTO @dbName;
WHILE @@FETCH_STATUS = 0
BEGIN
	if @sql <> '' -- conditionally add union if not the first select
		set @sql = concat(@sql, ' union ');

	set @sql = concat(@sql, 
        'select 
            '''+@dbName+'''  collate SQL_Latin1_General_CP1_CI_AS as db
            , s.name collate SQL_Latin1_General_CP1_CI_AS as schemaName
        from '+@dbName+'.sys.tables t 
        left join '+@dbName+'.sys.schemas s on t.schema_id = s.schema_id 
        where s.name in (''flo'',''load'', ''etl'')  
        and t.name in (''Workflow'', ''LoadParameters'') group by s.name')

    FETCH NEXT FROM dbNameCursor INTO @dbName;
END;
CLOSE dbNameCursor;
DEALLOCATE dbNameCursor;

print(@sql)
exec(@sql)