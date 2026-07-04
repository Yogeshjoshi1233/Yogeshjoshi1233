create database computer_course 
use computer_course;
create table course_table(
course_name varchar(20),
duration int(5),
start_date date,
fees decimal(5,2)
);
describe course_table;
alter table computer_course
modify column course_name char(20);
create database product_sales
use product_sales
create table stock(
product_code int(4),
product_name char(15),
description text,
cost_price decimal(8,2)
);
insert stock(product_code,product_name,description,cost_price)
values(101,'bags','leather_bags',150),(102,'books','notepads',10),(103,'pens','fine_tip_pens',20);
select * from stock;
select * from stock where cost_price<25;
alter table stock
add column quantity int;
select * from stock where product_name='books';

alter table stock
add constraint product_code primary key(product_code);
alter table stock 
drop column description;

rename table stock to product_sales;
