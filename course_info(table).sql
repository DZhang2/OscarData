create table course_info (
	id varchar(20),
    course_name text,
    credits integer,
    description text,
    primary key (id)
);
-- for courses with variable credit hours (ie: 1-21) set credits to null
SET SQL_SAFE_UPDATES = 0;
update course_info set credits=null where credits < 0;

