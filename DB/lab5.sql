USE AKovrizhnykh

IF OBJECT_ID('Price') IS NOT NULL
	DROP TABLE Price;
IF OBJECT_ID('GetOptimal') IS NOT NULL
	DROP FUNCTION GetOptimal;
IF OBJECT_ID('Minimal') IS NOT NULL
	DROP FUNCTION Minimal;
IF OBJECT_ID('Maximal') IS NOT NULL
	DROP FUNCTION Maximal;
IF OBJECT_ID('GetOptimalPrices') IS NOT NULL
	DROP PROCEDURE GetOptimalPrices;
IF OBJECT_ID('GetOptimalPricesBrute') IS NOT NULL
	DROP PROCEDURE GetOptimalPricesBrute;

CREATE TABLE Price (
	id int IDENTITY(1,1),
	name nvarchar(100),
	cube_price float,
	piece_price float,
	discount_limit float
	);

INSERT INTO Price VALUES
	('A', 0.25, 1.75, 8),
	('B', 0.66, 3.33, 4),
	('C', 0.33, 2.66, 6);

GO

CREATE FUNCTION GetOptimal(@area float, @amount int)
RETURNS int
AS
BEGIN
	RETURN (SELECT TOP(1) id FROM Price AS p ORDER BY IIF(p.discount_limit IS NULL,
		(p.cube_price*@area + p.piece_price)*@amount, -- (C*S + C')*N
		(p.cube_price*@area + p.piece_price)*dbo.Minimal(@amount, ROUND(p.discount_limit/(p.cube_price*@area + p.piece_price), 0)) + dbo.Maximal(0, @amount - ROUND(p.discount_limit/(p.cube_price*@area + p.piece_price), 0))*p.cube_price*@area -- (C*S + C')*min(N, [T/(C*S+C')]) + max(0, N - [T/(C*S+C')])*C*S
	));
END

GO

CREATE FUNCTION Minimal(@a int, @b int)
RETURNS int
AS
BEGIN
RETURN IIF(@a < @b, @a, @b);
END

GO

CREATE FUNCTION Maximal(@a int, @b int)
RETURNS int
AS
BEGIN
RETURN IIF(@a > @b, @a, @b);
END

GO

-- brute test
CREATE PROCEDURE GetOptimalPricesBrute(@area float)
AS 
BEGIN
	DECLARE @i int = 2,
		@name varchar,
		@left int = 1,
		@max_id int,
		@cur_id int = dbo.GetOptimal(@area, 1);
	WHILE @i < 1000
	BEGIN
		SET @max_id = dbo.GetOptimal(@area, @i);
		IF @max_id != @cur_id
		BEGIN
			SET @name = (SELECT p.name FROM Price AS p WHERE p.id = @cur_id);
			PRINT CONCAT('[', @left, ', ', @i - 1, '] -> ', @name);
			SET @cur_id = @max_id;
			SET @left = @i;
		END 
		SET @i = @i + 1;
	END
	SET @name = (SELECT p.name FROM Price AS p WHERE p.id = @cur_id);
	PRINT CONCAT('[', @left, ', inf] -> ', @name);
END
GO

-- ALGO
GO
CREATE PROCEDURE GetOptimalPrices(@area float)
AS
BEGIN
	DECLARE 
		@k1 float,
		@cur_id int,
		@b1 float = 0,
		@limit float = 0,
		@name varchar,
		@left int = 1;

	SET @cur_id = (SELECT TOP(1) p.id FROM Price AS p ORDER BY p.piece_price + @area*p.cube_price);
	SET @k1 = (SELECT p.piece_price + @area*p.cube_price FROM Price AS p WHERE p.id = @cur_id);

	WHILE 1 = 1
	BEGIN
		DECLARE @k2 float, @b2 float, @next_id int,
			@x0 float, @y0 float,
			@min_x float = NULL, @min_k float, @min_b float, @min_id int;
		DECLARE cursor_i CURSOR FOR (SELECT p.id, @area*p.cube_price, p.piece_price*ROUND(p.discount_limit / (@area*p.cube_price + p.piece_price), 0) FROM Price AS p WHERE p.discount_limit IS NOT NULL AND @area*p.cube_price != @k1);
		OPEN cursor_i;
		FETCH NEXT FROM cursor_i INTO @next_id, @k2, @b2;
		WHILE @@FETCH_STATUS = 0
		BEGIN
			SET @x0 = (@b2 - @b1) / (@k1 - @k2);
			IF @limit < @x0 AND (@min_x IS NULL OR (@x0 < @min_x OR (@x0 = @min_x AND @k2 < @min_k)))
			BEGIN
				SET @min_x = @x0;
				SET @min_k = @k2;
				SET @min_b = @b2;
				SET @min_id = @next_id;
			END
			FETCH NEXT FROM cursor_i INTO @next_id, @k2, @b2;
		END
		CLOSE cursor_i;
		DEALLOCATE cursor_i;
		IF @min_x IS NOT NULL
		BEGIN
			IF @cur_id != @min_id
			BEGIN
				SET @name = (SELECT p.name FROM Price AS p WHERE p.id = @cur_id);
				PRINT CONCAT('[', @left, ', ', FLOOR(@min_x), '] -> ', @name);
				SET @left = FLOOR(@min_x) + 1;
			END
			SET @cur_id = @min_id;
			SET @k1 = @min_k;
			SET @b1 = @min_b;
			SET @limit = @min_x;
		END
		ELSE
		BEGIN
			SET @name = (SELECT p.name FROM Price AS p WHERE p.id = @cur_id);
			PRINT CONCAT('[', @left, ', inf] -> ', @name);
			BREAK;
		END 
	END
END
GO


DECLARE @area float = 1.4;
PRINT 'Algorithm';
EXEC dbo.GetOptimalPrices @area;
PRINT 'Brute';
EXEC dbo.GetOptimalPricesBrute @area;