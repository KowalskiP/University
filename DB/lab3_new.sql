USE master
GO
 
IF  EXISTS (
        SELECT name
                FROM sys.databases
                WHERE name = N'ElenaBeklenishcheva'
)
ALTER DATABASE ElenaBeklenishcheva set single_user with rollback immediate
GO
 
IF  EXISTS (
        SELECT name
                FROM sys.databases
                WHERE name = N'ElenaBeklenishcheva'
)
DROP DATABASE [ElenaBeklenishcheva]
GO
 
CREATE DATABASE [ElenaBeklenishcheva]
GO
 
USE [ElenaBeklenishcheva]
GO
 
IF EXISTS(
  SELECT *
    FROM sys.schemas
   WHERE name = N'Scheme'
)
 DROP SCHEMA Scheme
GO
 
CREATE SCHEMA Scheme
GO


IF OBJECT_ID('commands', 'U') IS NOT NULL
	DROP TABLE commands
GO

CREATE TABLE commands (
	command_id int PRIMARY KEY not null,
	command_name varchar(50) UNIQUE not null
)
GO

INSERT INTO commands VALUES
(1, 'Урал'),
(2, 'Спартак'),
(3, 'Рубин')
GO


IF OBJECT_ID('conists', 'U') IS NOT NULL
	DROP TABLE consist
GO

CREATE TABLE consist (
	command_id int not null,
	player_id int PRIMARY KEY not null,
	player_surname varchar(50) not null,
	player_name varchar(50) not null

	FOREIGN KEY (command_id) REFERENCES commands(command_id)
)
GO

INSERT INTO consist VALUES
(1, 1, 'Арапов', 'Дмитрий'),
(1, 2, 'Заболотный', 'Николай'),
(1, 3, 'Жевнов', 'Юрий'),
(1, 4, 'Белозеров', 'Александр'),
(1, 5, 'Фомин', 'Денис'),

(2, 6, 'Ребров', 'Артем'),
(2, 7, 'Гранат', 'Владимир'),
(2, 8, 'Кутепов', 'Илья'),
(2, 9, 'Глушаков', 'Денис'),

(3, 10, 'Кузьмин', 'Олег'),
(3, 11, 'Устинов', 'Виталий'),
(3, 12, 'Сорокин', 'Егор'),
(3, 13, 'Жестоков', 'Максим')
GO


IF OBJECT_ID('games_info', 'U') IS NOT NULL
	DROP TABLE games_info
GO

CREATE TABLE games_info (
	id_game int PRIMARY KEY not null,
	game_date date not null,
	id_command_owner int not null,
	id_command_guest int not null,
	id_kipper_own int not null,
	id_kipper_g int not null,
	score_command_own int not null,
	score_command_guest int not null

	FOREIGN KEY (id_kipper_own) REFERENCES consist(player_id),
	FOREIGN KEY (id_kipper_g) REFERENCES consist(player_id)
)
GO

INSERT INTO games_info VALUES
(1, '20151125', 1, 2, 1, 6, 1, 1),
(2, '20151124', 2, 3, 7, 10, 2, 0),
(3, '20151123', 3, 1, 11, 2, 0, 3),
(4, '20160322', 2, 1, 7, 1, 3, 2),
(5, '20160321', 3, 2, 11, 6, 1, 1),
(6, '20160320', 1, 3, 1, 10, 1, 0)
GO



IF OBJECT_ID('goals', 'U') IS NOT NULL
	DROP TABLE goals
GO

CREATE TABLE goals(
	id_game int not null,
	id_player int not null,
	id_goal int PRIMARY KEY not null

	FOREIGN KEY (id_player) REFERENCES consist(player_id),
	FOREIGN KEY (id_game) REFERENCES games_info(id_game)
)
GO

INSERT INTO goals VALUES
(1, 2, 1),
(1, 7, 2),

(2, 8, 3),
(2, 8, 4),

(3, 2, 5),
(3, 3, 6),
(3, 4, 7),

(4, 6, 8),
(4, 8, 9),
(4, 9, 10),
(4, 3, 11),
(4, 4, 12),

(5, 12, 13),
(5, 8, 14),

(6, 3, 15)
GO
go
CREATE FUNCTION dbo.raiting_table() RETURNS @ret_raiting_table TABLE (
	Position int PRIMARY KEY not null,
	Team varchar(50) UNIQUE not null,
	Score int not null,
	Scored int not null,
	Missing int not null
)
AS
BEGIN
	--заполнить таблицу
	DECLARE @temp_table TABLE(tteam varchar(50), 
							  tscore int, 
							  tscored int, 
							  tmissing int)

	DECLARE @temp_str varchar(2000);

	DECLARE @teams_count int;
	SET @teams_count = (SELECT COUNT(commands.command_id)
						FROM commands)
	DECLARE @counter int = 0;
	WHILE(@counter < @teams_count)
		SET @temp_str = (SELECT commands.command_name, games_info.score_command_own, games_info.score_command_own, games_info.score_command_guest
							FROM commands, games_info
							WHERE commands.command_id = games_info.id_command_owner and commands.command_id = @counter)
		print(@temp_str);
		SET @counter = @counter + 1;
	END;

	--INSERT @ret_raiting_table
	--SELECT games_info.id_game, commands.command_name, games_info.score_command_guest, games_info.score_command_guest,games_info.score_command_guest
	--FROM games_info, commands
	--WHERE games_info.id_command_guest =commands.command_id

	RETURN;
END
GO