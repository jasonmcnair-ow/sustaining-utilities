-- used to find instances of WorkflowNotification configurations
exec spDropTable '#databases';
CREATE TABLE #databases (db varchar(max), schemaName varchar(max))

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
	else
		set @sql = 'insert into #databases select * from (';


	set @sql = concat(@sql, 
        'select 
            '''+@dbName+'''  collate SQL_Latin1_General_CP1_CI_AS as db
            , s.name collate SQL_Latin1_General_CP1_CI_AS as schemaName
        from '+@dbName+'.sys.tables t 
        left join '+@dbName+'.sys.schemas s on t.schema_id = s.schema_id 
        where s.name in (''flo'')  
        and t.name in (''WorkflowNotification'') group by s.name')

    FETCH NEXT FROM dbNameCursor INTO @dbName;
END;
CLOSE dbNameCursor;
DEALLOCATE dbNameCursor;

set @sql = concat(@sql, ') dbs')

print(@sql)
exec(@sql)

declare @instance varchar(max);

select @instance=name from sys.servers where is_linked = 0

exec spDropTable '#workflowNotifications';
CREATE TABLE #workflowNotifications (
	instance varchar(max)
	, datatoolsDb varchar(max)
	, workflowId int
	, notificationEmailSubject varchar(max)
	, notificationEmailKey varchar(max)
	, failureTicketPriority varchar(32)
	, failureTicketSeverity int
	)

declare @notificationsSql varchar(max);
DECLARE dbNameCursor CURSOR FOR
SELECT db FROM #databases;
OPEN dbNameCursor;
FETCH NEXT FROM dbNameCursor INTO @dbName;
WHILE @@FETCH_STATUS = 0
BEGIN
	set @notificationsSql = 'insert into #workflowNotifications ';
	set @notificationsSql = CONCAT(@notificationsSql, 'select '''+@instance+''', '''+@dbName+''', * from ['+@dbName+'].[flo].[WorkflowNotification]')


	exec(@notificationsSql)

    FETCH NEXT FROM dbNameCursor INTO @dbName;
END;
CLOSE dbNameCursor;
DEALLOCATE dbNameCursor;

select * from #workflowNotifications
