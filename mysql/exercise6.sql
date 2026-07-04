use abc

create table department
(
	did int primary key,
    depname char(30)

)

insert department
values(100,'HR'),(200,'Finance'),(300,'Sales'),(400,'Production')

create table employee
(
	empid char(10) primary key,
    ename char(30),
    did int 
)
alter table employee
add constraint foreign key (did) references department(did)

insert employee
values('e001','David',100),('e002','Tim',200),('e003','Bob',100),('e004','Rita',400),('e005','William',300)


select * from employee
select * from department
select d.depname,count(e.did) as TotalDepartment
from department d JOIN employee e
on d.did=e.did
group by e.did
