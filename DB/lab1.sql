USE master
GO

IF  EXISTS (
	SELECT name 
		FROM sys.databases 
		WHERE name = N'A_Chikunov'
)
ALTER DATABASE [A_Chikunov] set single_user with rollback immediate
GO

IF  EXISTS (
	SELECT name 
		FROM sys.databases 
		WHERE name = N'A_Chikunov'
)
DROP DATABASE [A_Chikunov]
GO

CREATE DATABASE [A_Chikunov]
GO

USE [A_Chikunov]
GO

IF EXISTS(
  SELECT *
    FROM sys.schemas
   WHERE name = N'Chikunov'
) 
 DROP SCHEMA Chikunov
GO

CREATE SCHEMA Chikunov 
GO

IF OBJECT_ID('[A_Chikunov].Chikunov.ut_typemeasurements', 'U') IS NOT NULL
  DROP TABLE  [A_Chikunov].Chikunov.ut_typemeasurements
GO

CREATE TABLE [A_Chikunov].Chikunov.ut_typemeasurements
(
	ID_type int NOT NULL, 
	Title nvarchar(40) NULL,
	Units nvarchar(20) NULL, 
    CONSTRAINT PK_ID_type PRIMARY KEY (ID_type) 
)
GO

IF OBJECT_ID('[A_Chikunov].Chikunov.ut_stations', 'U') IS NOT NULL
  DROP TABLE  [A_Chikunov].Chikunov.ut_stations
GO

CREATE TABLE [A_Chikunov].Chikunov.ut_stations
(
	ID_station int NOT NULL, 
	Title nvarchar(40) NULL, 
	st_Address nvarchar(40) NULL, 
    CONSTRAINT PK_ID_station PRIMARY KEY (ID_station) 
)
GO

IF OBJECT_ID('[A_Chikunov].Chikunov.ut_measurements', 'U') IS NOT NULL
  DROP TABLE  [A_Chikunov].Chikunov.ut_measurements
GO

CREATE TABLE [A_Chikunov].Chikunov.ut_measurements
(
	ID int NOT NULL IDENTITY(1,1), 
	m_Date Date NULL, 
	ID_type int Null,
	Value float NULL, 
	ID_station int NULL,
    CONSTRAINT PK_ID PRIMARY KEY (ID),
	CONSTRAINT FK_type FOREIGN KEY (ID_type) 
		REFERENCES [A_Chikunov].Chikunov.ut_typemeasurements(ID_type)
		ON DELETE CASCADE 
		ON UPDATE CASCADE,
	CONSTRAINT FK_station FOREIGN KEY (ID_station) 
		REFERENCES [A_Chikunov].Chikunov.ut_stations(ID_station)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
GO

--SELECT * From [A_Chikunov].Chikunov.ut_typemeasurements 
--SELECT * From [A_Chikunov].Chikunov.ut_stations 
--SELECT * From [A_Chikunov].Chikunov.ut_measurements 

INSERT INTO [A_Chikunov].Chikunov.ut_typemeasurements VALUES
(1,'����������� ������� � �����', N'����'),
(2,'��������', N'�� �� �� '),
(3,'��������� �������', N'�������'),
(4,'�������� � ����������� �����', N'����� � �������'),
(5,'������', '��')

--DELETE FROM [A_Chikunov].Chikunov.ut_typemeasurements

INSERT INTO [A_Chikunov].Chikunov.ut_stations VALUES
(1,'������_����', N'79.50 �.�. 76.98 �.�'),
(2,'����������', N'79.55 �.�.  90.62 �.�.'),
(3,'����������', N'78.07 �.�.  14.25 �.�.'),
(4,'�������', N'77.20 �.�.  96.40 �.�.')

INSERT INTO [A_Chikunov].Chikunov.ut_measurements VALUES
('2015/10/10', 1, 15, 1),
('2015/10/11', 2, 180, 2),
('2015/10/12', 3, 100, 3),
('2015/10/13', 4, 10, 4),
('2015/10/10', 5, 30, 1),
('2015/10/11', 1, 20, 2),
('2015/10/12', 2, 160, 3),
('2015/10/13', 3, 130, 4),
('2015/10/10', 4, 15, 1),
('2015/10/11', 5, 33, 2),
('2015/10/12', 1, 15, 3),
('2015/10/13', 2, 150, 4),
('2015/10/10', 3, 10, 1),
('2015/10/11', 4, 5, 2),
('2015/10/12', 5, 4, 3),
('2015/10/13', 1, 2, 4),
('2015/10/10', 1, 15, 4),
('2015/10/11', 2, 180, 3),
('2015/10/12', 3, 100, 3),
('2015/10/13', 4, 10, 4),
('2015/10/10', 5, 25, 1),
('2015/10/11', 1, 20, 2),
('2015/10/12', 2, 160, 2),
('2015/10/13', 3, 130, 1),
('2015/10/10', 4, 15, 4),
('2015/10/11', 5, 33, 3),
('2015/10/12', 1, 15, 3),
('2015/10/13', 2, 150, 4),
('2015/10/10', 3, 20, 1),
('2015/10/11', 4, 5, 2),
('2015/10/12', 5, 4, 2),
('2015/10/13', 1, 2, 1)

--SET DATEFORMAT dmy;
--GO
SELECT ID_type as ID, Title as [��� ���������], Units as [��.] From [A_Chikunov].Chikunov.ut_typemeasurements 
SELECT ID_station as ID, Title as [�������� �������], st_Address as ����� From [A_Chikunov].Chikunov.ut_stations 
SELECT ID, CONVERT(varchar,m_Date, 104) as ����, ID_type as ���, Value as ��������, ID_station as �������  From [A_Chikunov].Chikunov.ut_measurements 

SELECT CONVERT(varchar,M.m_Date, 104) as ����, T.Title as ���, AVG(Value) as ��������, S.Title as �������
From [A_Chikunov].Chikunov.ut_measurements as M, [A_Chikunov].Chikunov.ut_typemeasurements as T, [A_Chikunov].Chikunov.ut_stations as S
WHERE m_Date = '2015/10/10' AND T.ID_type = m.ID_type AND S.ID_station=m.ID_station
GROUP BY M.m_Date, T.Title, S.Title;
