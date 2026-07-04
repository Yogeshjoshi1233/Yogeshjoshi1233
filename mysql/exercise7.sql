use sales
create table salesman
(
sales_manid int,
name char(30),
city char(30),
commission float
)
insert salesman
values(5001,'james hong','new york',0.15),
(5002,'nail knite','paris',0.13),
(5005,'pit alex','london',0.11),
(5006,'Mc lyon','paris',0.14),
(5007,' paul adam','rome',0.13)
select * from salesman

create table customer(
customer_id int,
cust_name char(30),
city char(30),
grade char (10),
salesman_id int
)
alter table customer
modify grade int


insert customer
values(3002,'nick rimando','new york',100,5001),
(3007,'brad davis','new york',200,5001),
(3005,'graham zusi','california',200,5002),
(3008,'julian green','london ',300,5002),
(3004,'fabian jhonson','pairs',300,5006),
(3009,'geoff cameron','berlin',100,5006),
(3003,'jozy alitador','moscow',200,5007)

select customer_id from customer
except
select sales_manid from salesman

select sales_manid,city
from salesman
union
select salesman_id,city
from customer

create table orders(
ord_no  int,
purch_amt float,
ord_date  date,
customer_id int,
salesmna_id int
)
insert orders
values(70001,150.5,'2012-10-05',3005,5002),
(70009,270.65,'2012-09-10',3001,5005),
(70002,65.26,'2012-10-05',3002,5001),
(70004,110.5,'2012-08-17',3009,5003),
(70007,948.5,'2012-09-10',3005,5002),
(70005,2400.6,'2012-07-27',3007,5001),
(70008,5760,'2012-09-10',3002,5001),
(70010,1983.43,'2012-10-10',3004,5006),
(70012,2480.4,'2012-10-10',3009,5003),
(70011,75.29,'2012-08-17',3003,5007),
(70013,3045.6,'2012-04-25',3002,5001)
select * from orders










