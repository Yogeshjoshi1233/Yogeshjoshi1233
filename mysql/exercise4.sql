create database product;
use product;
create table sales_detail(
product_code int primary key,
selling_price int,
qty int,
units_sold int,
month char(5),
locataion char(10)
);
alter table sales_detail
rename column month to monthh;

alter table sales_detail
modify column locataion char(50);

insert sales_detail(product_code,selling_price,qty,units_sold,monthh,locataion)
value(101,200,1500,1450,'jan','california');
insert sales_detail(product_code,selling_price,qty,units_sold,monthh,locataion)
value(102,100,5000,3000,'jan','newyork');
insert sales_detail(product_code,selling_price,qty,units_sold,monthh,locataion)
values(103,20,2900,2000,'jan','los angleles');
insert sales_detail(product_code,selling_price,qty,units_sold,monthh,locataion)
values (104,56,120,9,'jan','sydney');
insert sales_detail(product_code,selling_price,qty,units_sold,monthh,locataion)
values(105,200,1000,500,'jan','newyork');

select * from sales_detail;

create table stock_details(
product_code int,
product_name char,
description char,
cost_price float,
Date_of_manufacture date
);
alter table stock_details
modify product_name char(10);


alter table stock_details
modify description char(20);

insert stock_details(product_code,product_name,description,cost_price,Date_of_manufacture)
values(101,'bags','leatherbags',150,'2003-10-05')

insert stock_details(product_code,product_name,description,cost_price,Date_of_manufacture)
values(102,'books','notepads',10,'2003-12-05')

insert stock_details(product_code,product_name,description,cost_price,Date_of_manufacture)
values(103,'pens','fine tip pens',20,'2003-01-09')

insert stock_details(product_code,product_name,description,cost_price,Date_of_manufacture)
values(104,'staplers','staplers',40,'2003-10-05')

update sales_detail
set units_sold=2500
where product_code=103;

delete from sales_detail
where product_code=104;

