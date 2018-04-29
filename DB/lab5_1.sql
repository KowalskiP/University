/*
Задача 4. База данных фирмы, проводящей аукционы .
Фирма занимается продажей с аукциона антикварных изделий и 
произведений искусства. Владельцы вещей, выставляемых на проводимых фирмой
аукционах, юридически являются продавцами. Лица, приобретающие эти вещи, 
именуются покупателями. Получив от продавцов партию предметов, фирма решает, 
на котором из аукционов выгоднее представить конкретный предмет. 
Перед проведением очередного аукциона каждой из выставляемых на нем 
вещей присваивается отдельный номер лота. Две вещи, 
продаваемые на различных аукционах, могут иметь одинаковые номера лотов. 
В книгах фирмы делается запись о каждом аукционе. Там отмечаются дата, 
место и время его проведения, а также специфика (например, 
выставляются картины, на писанные маслом и не ранее 1900 г.). 
Заносятся также сведения о каждом продаваемом предмете: 
аукцион, на который он заявлен, номер лота, продавец, отправная цена 
и краткое словесное описание. Продавцу разрешается выставлять 
любое количество вещей, а покупатель имеет право приобретать 
любое количество вещей. Одно и то же лицо или фирма может выступать 
и как продавец, и как покупатель. После аукциона служащие фирмы, 
проводящей аукционы, записывают фактическую цену, уплаченную 
за проданный предмет, и фиксируют данные покупателя. 
Создать триггер для проверки того, что вещь в один день не находится 
на двух аукционах.
Написать запросы, осуществляющие следующие операции:
1) Вывести список аукционов с указанием отсортированных по величине
 суммарных доходов от продажи.
2) Для указанного интервала дат вывести список проданных на аукционах 
 предметов. Для каждого из предметов дать список аукционов, 
 где выставлялся этот же предмет.
3) Для указанного интервала дат вывести список продавцов в порядке убывания
 общей суммы, полученной ими от продажи предметов в этот промежуток времени.
4) Для указанного места вывести список аукционов, отсортированных 
 по количеству выставленных вещей.
5) Для указанного интервала дат вывести список продавцов, которые принимали участие в аукционах, с указанием для каждого из них списка выставленных предметов.
6) Вывести список покупателей с указанием количества приобретенных предметов в указанный период времени.
*/

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

if OBJECT_ID('clients', 'u') is not null
	drop table clients
if OBJECT_ID('books', 'u') is not null
	drop table books
if OBJECT_ID('goods', 'u') is not null
	drop table goods
if OBJECT_ID('auct_type', 'u') is not null
	drop table auct_type
if OBJECT_ID('lot', 'u') is not null
	drop table lot
if OBJECT_ID('buy', 'u') is not null
	drop table buy
if OBJECT_ID('correct_data', 't') is not null
	drop trigger correct_data
if OBJECT_ID('listauc') is not null
	drop trigger listauc
if OBJECT_ID('listgoods') is not null
	drop trigger listgoods
go


create table clients(
	id int PRIMARY KEY IDENTITY NOT NULL,
	name nvarchar(128)
)
go

insert into clients values
('Фирма 1'),
('Фирма 2'),
('Фирма 3'),
('Фирма 4'),
('Фирма 5')
go

create table auct_type(
	id int PRIMARY KEY IDENTITY NOT NULL,
	auct_type_name varchar(128) NOT NULL
)
go

insert into auct_type values
('Специфика 1'),
('Специфика 2'),
('Специфика 3'),
('Специфика 4')
go


create table books(
	id int PRIMARY KEY IDENTITY NOT NULL,
	auct_date date NOT NULL,
	auct_time time NOT NULL,
	auct_place varchar(128) NOT NULL,
	auct_type_id int NOT NULL

	FOREIGN KEY (auct_type_id) REFERENCES auct_type(id)
)
go

insert into books values
('20100101', '12:00:00', 'Место 1', 1),
('20110102', '12:00:00', 'Место 2', 2),
('20120103', '12:00:00', 'Место 3', 4),
('20130104', '12:00:00', 'Место 4', 1),
('20100101', '13:00:00', 'Место 2', 1)
go

create table goods(
	id int PRIMARY KEY IDENTITY NOT NULL,
	name nvarchar(128) NOT NULL,
	seller int NOT NULL

	FOREIGN KEY (seller) REFERENCES clients(id)
)
go

insert into goods values
('Вещь 1', 1),
('Вещь 2', 1),
('Вещь 3', 2),
('Вещь 4', 3),
('Вещь 5', 4),
('Вещь 6', 5),
('Вещь 7', 5)
go


create table lots(
	id int PRIMARY KEY IDENTITY NOT NULL,
	id_good int not null,
	id_lot int not null,
	id_auct int not null,
	start_cost float not null,
	descr_id int not null
	
	FOREIGN KEY (id_good) REFERENCES goods(id),
	FOREIGN KEY (descr_id) REFERENCES auct_type(id),
	FOREIGN KEY (id_auct) REFERENCES books(id)
)
go


create trigger correct_data ON lots AFTER INSERT AS
begin
	DECLARE @counter int = (
								SELECT count(*) 
								FROM inserted
								INNER JOIN books AS IBooks ON IBooks.id = inserted.id_auct
								INNER JOIN lots ON lots.id_good = inserted.id_good
								INNER JOIN books AS CBooks ON CBooks.id = lots.id_auct
								WHERE inserted.id != lots.id and 
									inserted.id_good = lots.id_good and 
									IBooks.auct_date = CBooks.auct_date and 
									IBooks.auct_place != CBooks.auct_place
							)
	IF @counter > 0
	BEGIN
		print ('В этот день товар уже выставлен на другом аукционе'); 
		ROLLBACK TRANSACTION;
		RETURN
	END
end
go


insert into lots values
(1, 1, 1, 15, 1),
(2, 2, 1, 10, 1),
(3, 1, 2, 5, 2),
(2, 2, 2, 10, 2),
(4, 3, 2, 20, 2),
(5, 6, 3, 10, 4),
(6, 2, 4, 25, 1),
(7, 3, 5, 20, 1)
go
--плохо для триггера
insert into lots values
(1, 2, 5,  20, 4)
go


create table buy(
	fact_cost int not null,
	id_buyer int not null,
	id_good int not null,
	id_auct int not null

	FOREIGN KEY (id_buyer) REFERENCEs clients(id),
	FOREIGN KEY (id_good) REFERENCES goods(id),
	FOREIGN KEY (id_auct) REFERENCES books(id)
)
go

insert into buy values
(20, 2, 1, 1),
(30, 3, 2, 1),
(10, 1, 3, 2),
(20, 2, 4, 2),
(30, 3, 5, 3),
(40, 1, 6, 4),
(50, 1, 7, 5)
go

--Вывести список аукционов с указанием отсортированных по величине суммарных доходов от продажи.
SELECT books.id as 'Номер аукциона', sum(fact_cost-start_cost) as 'Доход'
FROM books
join  buy on buy.id_auct=books.id
join lots on lots.id_good = buy.id_good
group by books.id
ORDER BY 'Доход' DESC
go


--Для указанного интервала дат вывести список проданных на аукционах предметов. Для каждого из предметов дать список аукционов, где выставлялся этот же предмет.
create function listauc()
returns @listing table (id int, list nvarchar(100))
as
begin
	declare @c int = (select count(id) from goods),
			@i int = 1
	while @i<= @c
	begin
		declare @curauc nvarchar(100), @listauc nvarchar(100);
		set @listauc = ''
		DECLARE cursor_i CURSOR FOR (select id_auct from lots where id_good = @i);
		open cursor_i;
		FETCH NEXT FROM cursor_i INTO @curauc
		WHILE @@FETCH_STATUS = 0
		BEGIN
			if (@listauc like '')
				set @listauc = @curauc
			else
				set @listauc = CONCAT(@listauc,', ',@curauc)
			FETCH NEXT FROM cursor_i INTO @curauc
		end
		CLOSE cursor_i;
		DEALLOCATE cursor_i;
		insert into @listing values
		(@i, @listauc)
		
		set @i = @i + 1
	end
	return
end
go

DECLARE @start	date = '20010101'
DECLARE @end	date = '20160101'
SELECT goods.name	AS	'Проданный предмет',
	   books.id		AS	'Аукцион, на котором продали',
	   l.list AS 'Бывшие аукционы'
FROM buy
INNER JOIN goods ON buy.id_good = goods.id
INNER JOIN books ON buy.id_auct = books.id
inner join dbo.listauc() as l on goods.id = l.id
GO


--Для указанного интервала дат вывести список продавцов в порядке убывания общей суммы, полученной ими от продажи предметов в этот промежуток времени.
DECLARE @start	date = '20010101'
DECLARE @end	date = '20151212'
SELECT clients.name as 'Продавцы', sum(buy.fact_cost-lots.start_cost) as 'Доход'
FROM lots
INNER JOIN goods ON goods.id = lots.id_good
INNER JOIN clients ON clients.id = goods.seller
INNER JOIN buy ON lots.id_good = buy.id_good
group by clients.name
ORDER BY 'Доход' DESC

GO

--Для указанного места вывести список аукционов, отсортированных по количеству выставленных вещей
DECLARE @place varchar(128) = 'Место 2'
SELECT books.id as 'Аукцион'
FROM books
join lots on lots.id_auct = books.id
WHERE auct_place = @place
group by books.id
order by count(books.id) Desc
GO

--Для указанного интервала дат вывести список продавцов, которые принимали участие в аукционах, с указанием для каждого из них списка выставленных предметов.
create function listgoods()
returns @listing table (id int, list nvarchar(100))
as
begin
	declare @c int = (select  count( distinct clients.name) from lots join goods on lots.id_good = goods.id join clients on goods.seller = clients.id ),
			@i int = 1
	while @i<= @c
	begin
		declare @curg nvarchar(100), @listg nvarchar(100);
		set @listg = ''
		DECLARE cursor_i CURSOR FOR (select Distinct name from lots join goods on lots.id_good = goods.id where seller = @i);
		open cursor_i;
		FETCH NEXT FROM cursor_i INTO @curg
		WHILE @@FETCH_STATUS = 0
		BEGIN
			if (@listg like '')
				set @listg = @curg
			else
				set @listg = CONCAT(@listg,', ',@curg)
			FETCH NEXT FROM cursor_i INTO @curg
		end
		CLOSE cursor_i;
		DEALLOCATE cursor_i;
		insert into @listing values
		(@i, @listg)
		
		set @i = @i + 1
	end
	return
end
go

select * from dbo.listgoods()

DECLARE @start date = '20010101'
DECLARE @end date = '20160101'
SELECT distinct clients.name AS 'Продавец',
	   l.list AS 'Выставленный предмет'
FROM lots
INNER JOIN goods ON goods.id = lots.id_good
INNER JOIN clients ON goods.seller = clients.id
INNER JOIN books ON books.id = lots.id_auct
inner join dbo.listgoods() as l on l.id = clients.id
WHERE books.auct_date > @start and books.auct_date < @end
go


--Вывести список покупателей с указанием количества приобретенных предметов в указанный период времени.
DECLARE @start date = '20010101'
DECLARE @end date = '20160101'
SELECT clients.name,
	   count(buy.id_good) AS 'Количество приобретенных предметов'
FROM buy
INNER JOIN clients ON buy.id_buyer = clients.id
INNER JOIN books ON books.id = buy.id_auct
WHERE books.auct_date > @start and books.auct_date < @end
group by clients.name
go