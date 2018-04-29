USE master
GO

IF  EXISTS (
	SELECT name 
		FROM sys.databases 
		WHERE name = N'Auction'
)
ALTER DATABASE [Auction] set single_user with rollback immediate
GO

IF  EXISTS (
	SELECT name 
		FROM sys.databases 
		WHERE name = N'Auction'
)
DROP DATABASE [Auction]
GO

CREATE DATABASE [Auction]
GO

USE [Auction]
GO
 
IF EXISTS(
  SELECT *
    FROM sys.schemas
   WHERE name = 'Auct'
) DROP SCHEMA Auct
GO
 
CREATE SCHEMA Auct
GO

create table clients(
	id int PRIMARY KEY IDENTITY NOT NULL,
	name nvarchar(128)
)
go

create table goods(
	id int PRIMARY KEY IDENTITY NOT NULL,
	name nvarchar(128),
	prop int
)
go

create table book(
	id int PRIMARY KEY IDENTITY NOT NULL,
	d date,
	t time,
	place nvarchar(128),
	theme nvarchar(128)
)
go

create table lots(
	id int PRIMARY KEY IDENTITY NOT NULL,
	auc int,
	num int,
	own int,
	price money
)
go

create table byers(
)
go