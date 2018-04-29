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

IF OBJECT_ID('[A_Chikunov].Chikunov.regions', 'U') IS NOT NULL
  DROP TABLE  [A_Chikunov].Chikunov.regions
GO

CREATE TABLE [A_Chikunov].Chikunov.regions
(
	Number nvarchar(40) NOT NULL, 
	Name nvarchar(40) NULL,  
    CONSTRAINT PK_Number PRIMARY KEY (Number) 
)
GO

IF OBJECT_ID('[A_Chikunov].Chikunov.extRegions', 'U') IS NOT NULL
  DROP TABLE  [A_Chikunov].Chikunov.extRegions
GO

CREATE TABLE [A_Chikunov].Chikunov.extRegions
(
	extNumber nvarchar(40) NOT NULL, 
	curNumber nvarchar(40) NULL,  
    CONSTRAINT PK_extNumber PRIMARY KEY (extNumber),
	CONSTRAINT FK_curNumber FOREIGN KEY (curNumber)
		REFERENCES [A_Chikunov].Chikunov.regions(Number)
)
GO

IF OBJECT_ID('[A_Chikunov].Chikunov.regAuto', 'U') IS NOT NULL
  DROP TABLE  [A_Chikunov].Chikunov.regAuto
GO

CREATE TABLE [A_Chikunov].Chikunov.regAuto
(
	ID int NOT NULL, 
	Model nvarchar(40) NULL,
	Color nvarchar(20) NULL,
	GovNum nvarchar(9) NULL,
	RegNum nvarchar(40) NULL,
	Name nvarchar(40) NULL,
	TimeT Time NULL,
	Direct nvarchar(10) NULL,  
    CONSTRAINT PK_ID PRIMARY KEY (ID), 
	CONSTRAINT FK_RegNumEx FOREIGN KEY (RegNum)
		REFERENCES [A_Chikunov].Chikunov.extRegions(extNumber)
)
GO
 

IF OBJECT_ID('[A_Chikunov].Chikunov.penalty', 'U') IS NOT NULL
  DROP TABLE  [A_Chikunov].Chikunov.penalty
GO

CREATE TABLE [A_Chikunov].Chikunov.penalty
(
	ID_penalty int NOT NULL, 
	Name nvarchar(40) NULL,
	Offense nvarchar(40) NULL,
	Summary int NULL,
	Paid bit NULL,  
    CONSTRAINT PK_ID_penalty PRIMARY KEY (ID_penalty) 
)
GO


INSERT INTO [A_Chikunov].Chikunov.regions VALUES
('01',  '���������� ������'), 
('04',  '���������� �����'),
('02',  '���������� ������������'),
('03',  '���������� �������'),
('05',  '���������� ��������'),
('06',  '���������� ���������'),
('07',  '���������-���������� ����������'),
('08', '���������� ��������'),
('09', '���������� ���������-��������'),
('10', '���������� �������'),
('11', '���������� ����'), 
('82', '���������� ����'),
('12', '���������� ����� ��'),
('13', '���������� ��������'),
('14', '���������� ���� (������)'), 
('15', '���������� �������� ������ � ������'), 
('16', '���������� ���������'),
('17', '���������� ����'),  
('18', '���������� ����������'),
('19', '���������� �������'),  
('95', '��������� ����������'),  
('21', '��������� ����������'),
('22', '��������� ����'),  
('75', '������������� ����'),
('41', '���������� ����'),
('23', '������������� ����') 


INSERT INTO [A_Chikunov].Chikunov.extRegions VALUES
('02','02'),
('102', '02'),
('82', '82'),
('777', '82'),
('13', '13'),
('113',  '13'),
('16','16'),
('116', '16'),
('21','21'),
('121','21'), 
('75','75'),
('80', '75'),
('23', '23'),
('93', '23'),
('123', '23') 

IF OBJECT_ID(N'Chikunov.CheckRegis', N'TR') IS NOT NULL
  DROP Trigger  Chikunov.CheckRegis;
GO

Create Trigger Chikunov.CheckRegis
on [A_Chikunov].Chikunov.regAuto
instead of insert
as
begin
	DECLARE @num bit
	Declare @Number nvarchar(9)
	Declare @Reg nvarchar(40)
	Declare @Direct nvarchar(10)

	Declare @ID int 
	Declare @Model nvarchar(40)
	Declare @Color nvarchar(20)
	Declare @Name nvarchar(40)
	Declare @TimeT Time 

	Select @ID = (Select i.ID from INSERTED i)
	Select @Model = (Select i.Model from inserted i )
	Select @Color = (Select i.Color from inserted i )
	Select @Name = (Select i.Name from inserted i )
	Select @TimeT = (Select i.TimeT from inserted i )
	Select @Number = (Select GovNum from INSERTED)	
	Select @Reg = (Select RegNum from INSERTED)	
	Select @Direct = (Select Direct from INSERTED)	
	
	IF(@Number Like '[ABEKMHOPCTYX������������][0-9][0-9][0-9][ABEKMHOPCTYX������������][ABEKMHOPCTYX������������]')
		Set @num = 1;
	Else
		begin
		Set @num = 0;
		RAISERROR('�������� ���. �����',16,2);
        ROLLBACK TRANSACTION;
        RETURN
		end
	
	Declare @regi bit
	if (@Reg Like '[127][0-9][0-9]' OR @Reg LIKE '[0-9][0-9]')
		set @regi = 1;
	Else
		begin
		Set @regi = 0;
		RAISERROR('�������� ������',16,2);
        ROLLBACK TRANSACTION;
        RETURN
		end
	
	Declare @dir bit
	Declare @in int
	Select @in = Count(*) from [A_Chikunov].Chikunov.regAuto
					where [A_Chikunov].Chikunov.regAuto.GovNum = @Number
						and
						  [A_Chikunov].Chikunov.regAuto.Direct = 'IN'
	Declare @out int
	Select @out = Count(*) from [A_Chikunov].Chikunov.regAuto
					where [A_Chikunov].Chikunov.regAuto.GovNum = @Number
						and
						  [A_Chikunov].Chikunov.regAuto.Direct = 'OUT'
	if (@in = @out)
		set @dir =1;
	else if (@in > @out and @Direct = 'IN')
		set @dir = 0;
	else if (@in > @out and @Direct = 'OUT')
		set @dir = 1;
	else if (@in < @out and @Direct = 'OUT')
		set @dir = 0;
	else if (@in < @out and @Direct = 'INT')
		set @dir = 1;

	if @dir = 0
	begin
		RAISERROR('������ ��� �������� ��� �������',16,2);
        ROLLBACK TRANSACTION;
        RETURN
	end

	if (@num >0 and @dir >0 and @regi >0)
		insert into [A_Chikunov].Chikunov.regAuto
		values(@ID, @Model,@Color, @Number, @Reg, @Name, @TimeT, @Direct );
		
end
go

SELECT * From [A_Chikunov].Chikunov.regAuto 
SELECT * From [A_Chikunov].Chikunov.regions 
SELECT * From [A_Chikunov].Chikunov.extRegions 
SELECT * From [A_Chikunov].Chikunov.penalty 
go

INSERT INTO [A_Chikunov].Chikunov.regAuto VALUES
(2,'BMW','RED','A754EK','102','IVAN','10:11:12','IN')
go 
INSERT INTO [A_Chikunov].Chikunov.regAuto VALUES
(6,'Honda','RED','A754E�','102','IVAN','10:11:12','OUT')
go 
INSERT INTO [A_Chikunov].Chikunov.regAuto VALUES
(8,'Mazda','RED','A754E�','102','IVAN','10:11:12','IN')
go 
INSERT INTO [A_Chikunov].Chikunov.regAuto VALUES
(9,'Mazda','RED','A754E�','102','IVAN','10:11:12','IN') 
go

SELECT * From [A_Chikunov].Chikunov.regAuto 
