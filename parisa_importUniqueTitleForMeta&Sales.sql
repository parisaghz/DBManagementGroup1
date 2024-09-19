-- author: parisa

--import unique title to meta
create table metas as 
select distinct on (title)*
from meta order by title,id;

drop table meta;

alter table metas rename to meta;

select count(distinct title) from meta


--import unique title to sales
create table saless as 
select distinct on (title)*
from sales order by title,id;

drop table sales;

alter table saless rename to sales;

select count(distinct title) from sales
