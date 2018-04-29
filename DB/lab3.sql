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
   WHERE name = 'Chikunov'
) DROP SCHEMA Chikunov
GO
 
CREATE SCHEMA Chikunov
GO

CREATE TABLE Chikunov.Clubs (
    id int PRIMARY KEY IDENTITY NOT NULL,
    name nvarchar(128)
)

CREATE TABLE Chikunov.Goalkeepers (
    id int PRIMARY KEY IDENTITY NOT NULL,
	club_id int FOREIGN KEY REFERENCES Chikunov.Clubs(id),
	name nvarchar(128),
	family nvarchar(128)    
)

CREATE TABLE Chikunov.Players (
    id int PRIMARY KEY IDENTITY NOT NULL,
	club_id int FOREIGN KEY REFERENCES Chikunov.Clubs(id),
	name nvarchar(128),
	family nvarchar(128)    
)

CREATE TABLE Chikunov.Matches (
    id int PRIMARY KEY IDENTITY NOT NULL,
    match_date date,
	club_home int FOREIGN KEY REFERENCES Chikunov.Clubs(id),
	club_guest int FOREIGN KEY REFERENCES Chikunov.Clubs(id)
)

CREATE TABLE Chikunov.Authors (
    id int PRIMARY KEY IDENTITY NOT NULL,
    match_id int,
	player int FOREIGN KEY REFERENCES Chikunov.Players(id)
)
go

insert into Chikunov.Clubs Values
('�����'),
('������'),
('�������'),
('���������')
go

insert into Chikunov.Goalkeepers values
(1, '����', '�������'),
(1,	'��������', '��������'),
(1,	'������', '��������'),
(2, '�����', '�����'),
(2,'��������', '�������'),
(3, '�����', '���������'),
(3,	'����', '������'),
(4, '����', '���������'),
(4, '����', '�����')
go