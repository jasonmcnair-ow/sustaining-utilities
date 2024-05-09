-- Run from a query against another database than the one being targeted
-- to avoid having open connection

-- SET @DatabaseName BELOW BEFORE RUNNING
DECLARE @DatabaseName nvarchar(50)
SET @DatabaseName = N'AHQ_PP_Data_AutoRestore01'

DECLARE @SQL varchar(max)

-- DROP ACTIVE CONNECTIONS
SELECT @SQL = COALESCE(@SQL,'') + 'Kill ' + Convert(varchar, SPId) + ';'
FROM MASTER..SysProcesses
WHERE DBId = DB_ID(@DatabaseName) AND SPId <> @@SPId

--SELECT @SQL 
EXEC(@SQL)

SELECT @SQL = 'DROP DATABASE ' + @DatabaseName + ';'

EXEC(@SQL)
