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
 
IF OBJECT_ID('Chikunov.Records') IS NOT NULL
    DROP TABLE Chikunov.Records
IF OBJECT_ID('Chikunov.Posts') IS NOT NULL
    DROP TABLE Chikunov.Posts
IF OBJECT_ID('Chikunov.Cars') IS NOT NULL
    DROP TABLE Chikunov.Cars
IF OBJECT_ID('Chikunov.RegionCodes') IS NOT NULL
    DROP TABLE Chikunov.RegionCodes
IF OBJECT_ID('Chikunov.Regions') IS NOT NULL
    DROP TABLE Chikunov.Regions
IF OBJECT_ID('Chikunov.Persons') IS NOT NULL
    DROP TABLE Chikunov.Persons
IF OBJECT_ID('Chikunov.lastAction') IS NOT NULL
	DROP FUNCTION Chikunov.lastAction
IF EXISTS(
  SELECT *
    FROM sys.schemas
   WHERE name = 'Chikunov'
) DROP SCHEMA Chikunov
GO
 
CREATE SCHEMA Chikunov
GO
 
-- Создание таблицы
CREATE TABLE Chikunov.Regions (
    id int PRIMARY KEY NOT NULL,
    name nvarchar(128) NOT NULL
)
CREATE TABLE Chikunov.RegionCodes (
    code int PRIMARY KEY NOT NULL,
    region_id int FOREIGN KEY REFERENCES Chikunov.Regions(id)
)
CREATE TABLE Chikunov.Persons (
    id int PRIMARY KEY IDENTITY NOT NULL,
    name nvarchar(128),
    family nvarchar(128)
)
CREATE TABLE Chikunov.Cars (
    id int PRIMARY KEY IDENTITY NOT NULL,
    mark nvarchar(128),
    color nvarchar(64),
    number nvarchar(64),
    region_code int FOREIGN KEY REFERENCES Chikunov.RegionCodes(code),
    owner int FOREIGN KEY REFERENCES Chikunov.Persons(id),
)
GO
CREATE TRIGGER Chikunov.CarsTrigger ON Chikunov.Cars FOR INSERT AS
	IF EXISTS (SELECT * FROM inserted WHERE number NOT LIKE '[АВЕКМНОРСТУХABEKMHOPCTYX][0-9][0-9][0-9][АВЕКМНОРСТУХABEKMHOPCTYX][АВЕКМНОРСТУХABEKMHOPCTYX]') OR
		EXISTS (SELECT * FROM inserted WHERE NOT (region_code < 100 OR region_code BETWEEN 100 AND 199 OR region_code BETWEEN 200 AND 299 OR region_code BETWEEN 700 AND 799))
	BEGIN
		RAISERROR ('Неверный номер автомобиля или код региона', 16, 1);
		ROLLBACK TRANSACTION;
		RETURN 
	END
GO 

CREATE TABLE Chikunov.Posts (
    id int PRIMARY KEY IDENTITY NOT NULL,
    name nvarchar(128)
)
CREATE TABLE Chikunov.Records (
    id int PRIMARY KEY IDENTITY NOT NULL,
    post_id int FOREIGN KEY REFERENCES Chikunov.Posts(id),
    car_id int FOREIGN KEY REFERENCES Chikunov.Cars(id),
    incoming bit,
    record_time datetime
)
GO
CREATE FUNCTION Chikunov.lastAction (@car_id int, @rec_id int, @time datetime)
RETURNS int
AS
BEGIN
    DECLARE @result bit = (SELECT TOP(1) incoming FROM Chikunov.Records WHERE car_id = @car_id AND id != @rec_id AND record_time <= @time ORDER BY record_time DESC)
	IF @result IS NULL RETURN -1
	RETURN CAST(@result AS int)
END
GO
CREATE TRIGGER Chikunov.RecordsTrigger ON Chikunov.Records FOR INSERT AS
	IF EXISTS (SELECT * FROM inserted WHERE incoming=Chikunov.lastAction(car_id, id, record_time))
	BEGIN
		RAISERROR ('Неверное действие для машины', 16, 1);
		ROLLBACK TRANSACTION;
		RETURN 
	END
GO

 
INSERT INTO Chikunov.Regions VALUES
    (13, 'Республика Мордовия'),
	(23, 'Краснодарский край'),       
    (50, 'Московская область'),
	(66, 'Свердловская область'),    
    (74, 'Челябинская область'),
	(77, 'город Москва')   
go
   
INSERT INTO Chikunov.RegionCodes VALUES
    (66, 66),
    (96, 66),
    (196, 66),

	(77, 77),
    (97, 77),
    (99, 77),
    (177, 77),
    (197, 77),
    (199, 77),
    (777, 77),
    
    (23, 23),
    (93, 23),
    (123, 23),
    
    (74, 74),
    (174, 74),
    
    (13, 13),
    (113, 13),

	(50, 50),
    (90, 50),
    (150, 50),
    (190, 50),
    (750, 50)
 go
 
INSERT INTO Chikunov.Persons VALUES
    ('Иван', 'Иванов'),
    ('Петр', 'Петров'),
    ('Василий', 'Васильев'),
    ('Татьяна', 'Татьянова'),
    ('Михаил', 'Михайлов')
 go

INSERT INTO Chikunov.Cars VALUES
    ('Honda', 'Красный',  'B387ТХ', 96, 1),
    ('Toyota', 'Черный',  'А064ВТ', 96, 1),
    ('Mazda', 'Черный',  'О360СК', 66, 2),
    ('BMW', 'Красный',  'С777АК', 174, 3),
    ('Mercedes', 'Белый',  'Н404НН', 777, 4),
    ('Daewoo', 'Оранжевый',  'А202КЕ', 123, 5),
    ('Bently', 'Желтый',  'А501СВ', 23, 4)
 go

INSERT INTO Chikunov.RegionCodes VALUES
(000,50)

INSERT INTO Chikunov.Cars VALUES
    ('Honda', 'Красный',  'B387ТA', 000, 1)
go
 
INSERT INTO Chikunov.Cars VALUES
    ('Honda', 'Красный',  'Z777ZZ', 23, 1)
go


INSERT INTO Chikunov.Posts VALUES
    ('Северный пост'),
    ('Южный пост'),
    ('Западный пост'),
    ('Восточный пост'),
    ('Северо-Западный пост')
go

INSERT INTO Chikunov.Records VALUES
    (1, 4, 1, '12:30'),
    (2, 4, 0, '14:15'),
    (1, 4, 1, '15:30'),
    (2, 4, 0, '16:15'),
    (3, 1, 0, '15:15'),
    (4, 1, 1, '16:15'),
    (5, 5, 1, '17:15'),
    (5, 5, 0, '18:15'),
	(3, 7, 0, '18:15')
go
	
INSERT INTO Chikunov.Records VALUES
	(3, 7, 0, '18:15')
go

SELECT Convert(nvarchar,r.record_time,108) AS Время, post.name AS Пост, IIF(r.incoming=1, 'Да', 'Нет') AS 'В город',
    c.mark AS Марка, c.color AS Цвет, c.number AS Номер, 
    reg.name AS Регион, pers.family AS Фамилия, pers.name AS Имя
    FROM Chikunov.Records AS r
        INNER JOIN Chikunov.Cars AS c ON r.car_id=c.id 
        INNER JOIN Chikunov.Persons AS pers ON c.owner=pers.id
        INNER JOIN Chikunov.Posts AS post ON post.id=r.post_id
        INNER JOIN Chikunov.RegionCodes AS codes ON codes.code=c.region_code
        INNER JOIN Chikunov.Regions AS reg ON codes.region_id=reg.id
    ORDER BY r.record_time
go

DECLARE @CurrentRegion int = (SELECT id FROM Chikunov.Regions WHERE name='Свердловская область')

DECLARE @transit table(car_id int)
INSERT INTO @transit SELECT DISTINCT t1.car_id FROM Chikunov.Records AS t1
	WHERE
		t1.incoming = 1 AND
		(SELECT regc.region_id
			FROM Chikunov.Cars AS cars 
			JOIN Chikunov.RegionCodes AS regc ON cars.region_code=regc.code
				WHERE cars.id=t1.car_id)!=@CurrentRegion AND
		EXISTS (SELECT * FROM Chikunov.Records AS t2 WHERE
			t1.car_id = t2.car_id AND
			t1.post_id != t2.post_id AND
			t1.record_time < t2.record_time AND
			t2.incoming = 0
		)

DECLARE @outer table(car_id int)
INSERT INTO @outer SELECT DISTINCT t1.car_id FROM Chikunov.Records AS t1
	WHERE
		t1.incoming = 1 AND
		EXISTS (SELECT * FROM Chikunov.Records AS t2 WHERE
			t1.car_id = t2.car_id AND
			t1.post_id = t2.post_id AND
			t1.record_time < t2.record_time AND
			t2.incoming = 0
		) AND t1.car_id NOT IN (SELECT * FROM @transit)

DECLARE @local table(car_id int)
INSERT INTO @local SELECT DISTINCT t1.car_id FROM Chikunov.Records AS t1
	WHERE
		t1.incoming = 0 AND
		(SELECT b.region_id
			FROM Chikunov.Cars AS a 
			JOIN Chikunov.RegionCodes AS b ON a.region_code=b.code
				WHERE a.id=t1.car_id)=@CurrentRegion AND
		EXISTS (SELECT * FROM Chikunov.Records AS t2 WHERE
			t1.car_id = t2.car_id AND
			t1.record_time < t2.record_time AND
			t2.incoming = 1
		) AND t1.car_id NOT IN (SELECT * FROM @transit) AND
		t1.car_id NOT IN (SELECT * FROM @outer)

-- Другие
DECLARE @other table(car_id int)
INSERT INTO @other SELECT DISTINCT t1.car_id FROM Chikunov.Records AS t1
	WHERE
		t1.car_id NOT IN (SELECT * FROM @transit) AND
		t1.car_id NOT IN (SELECT * FROM @outer) AND
		t1.car_id NOT IN (SELECT * FROM @local)

SELECT b.id AS 'Транзитные', b.mark AS 'Марка', b.color as 'Цвет' , b.number AS 'Номер',
	b.region_code AS 'Код региона', reg.name as 'Регион', pers.family as 'Фамилия', pers.name as 'Имя' FROM @transit AS a 
		JOIN Chikunov.Cars AS b ON a.car_id=b.id
		Join Chikunov.Persons AS pers ON b.owner=pers.id
		JOIN Chikunov.RegionCodes AS codes ON codes.code=b.region_code
		JOIN Chikunov.Regions AS reg ON codes.region_id=reg.id;

SELECT b.id AS ' Иногородние', b.mark AS 'Марка',b.color as 'Цвет' , b.number AS 'Номер',
	b.region_code AS 'Код региона', reg.name as 'Регион', pers.family as 'Фамилия', pers.name as 'Имя' FROM @outer AS a 
		JOIN Chikunov.Cars AS b ON a.car_id=b.id
		Join Chikunov.Persons AS pers ON b.owner=pers.id
		JOIN Chikunov.RegionCodes AS codes ON codes.code=b.region_code
		JOIN Chikunov.Regions AS reg ON codes.region_id=reg.id;

SELECT b.id AS 'Местные', b.mark AS 'Марка',b.color as 'Цвет' , b.number AS 'Номер',
	b.region_code AS 'Код региона', reg.name as 'Регион', pers.family as 'Фамилия', pers.name as 'Имя' FROM @local AS a
		JOIN Chikunov.Cars AS b ON a.car_id=b.id
		Join Chikunov.Persons AS pers ON b.owner=pers.id
		JOIN Chikunov.RegionCodes AS codes ON codes.code=b.region_code
		JOIN Chikunov.Regions AS reg ON codes.region_id=reg.id;

SELECT b.id AS 'Другие', b.mark AS 'Марка',b.color as 'Цвет' , b.number AS 'Номер',
	b.region_code AS 'Код региона', reg.name as 'Регион', pers.family as 'Фамилия', pers.name as 'Имя' FROM @other AS a
		JOIN Chikunov.Cars AS b ON a.car_id=b.id
		Join Chikunov.Persons AS pers ON b.owner=pers.id
		JOIN Chikunov.RegionCodes AS codes ON codes.code=b.region_code
		JOIN Chikunov.Regions AS reg ON codes.region_id=reg.id;
go