CREATE DATABASE lms;

use lms;

CREATE TABLE users (
	id INT PRIMARY KEY auto_increment,
    user varchar(30),
    email varchar(30)
);

alter table users auto_increment = 0;
truncate table users;
delete from users;
alter table users RENAME column user to name;

drop table users;

CREATE TABLE authentication(
	id INT PRIMARY KEY auto_increment,
    username varchar(30) not null,
    password varchar(50) not null,
    uid INT,
    FOREIGN KEY (uid) references users(id),
    create_at TIMESTAMP
);

alter table authentication add unique (username);
ALTER TABLE authentication modify COLUMN password VARCHAR (200);
drop table authentication;

CREATE TABLE roles (
	id int primary key auto_increment,
    role varchar(50)
);

drop table roles;

create table user_roles (
	id int primary key auto_increment,
    uid int,
    FOREIGN KEY (uid) references users(id),
    role_id int,
    FOREIGN KEY (role_id) references roles(id)
);

drop table user_roles;

CREATE TABLE courses (
	id INT PRIMARY KEY auto_increment,
    name varchar(50),
    content varchar(1000),
    duration int,
    price int,
    avg_rating float,
    approval_status ENUM ("approved", "pending"),
    no_of_students int,
    status ENUM ("active", "deactive"),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

alter table courses add unique (name);
	
drop table courses;

ALTER TABLE authentication MODIFY COLUMN password varchar(30) NOT NULL;

ALTER TABLE courses MODIFY COLUMN status ENUM ("active", "deactive") NOT NULL;

CREATE TABLE course_faq (
	id INT PRIMARY KEY auto_increment,
    cid int,
    FOREIGN KEY (cid) references courses(id),
    question varchar (200),
    answer varchar (200)
);
drop table course_faq;

CREATE TABLE course_feedback (
	id INT PRIMARY KEY auto_increment, 
    cid int,
    FOREIGN KEY (cid) references courses (id),
	uid int,
    FOREIGN KEY (uid) references users (id),
    rating float,
    comments varchar(200),
    created_at TIMESTAMP
);

drop table course_feedback;

CREATE TABLE student_course (
	id int primary key auto_increment,
    uid int,
    FOREIGN KEY (uid) references users(id),
    cid int,
    FOREIGN KEY (cid) references courses (id),
    purchased_on TIMESTAMP
);

drop table student_course;

CREATE TABLE mentor_course (
	id int primary key auto_increment,
    cid int,
    FOREIGN KEY (cid) references courses (id),
    uid int, 
    FOREIGN KEY (uid) references users(id)
);
drop table mentor_course;
show tables;

SET SQL_SAFE_UPDATES = 0;

INSERT INTO courses VALUES (2,"Master DSA", "dsa is easy", 3, 1000, 4.25, "approved", 3, "active", now(), now());
INSERT INTO courses VALUES (1,"Master WEB", "web is easy", 3, 1000, 4.75, "approved", 3, "active", now(), now());

select * from authentication;
select * from users;
INSERT INTO authentication VALUES (1, "naugs", 1234, 2, now());
delete from users;
delete from authentication;

INSERT INTO roles (role) values("Admin");
INSERT INTO roles (role) values("Student");
INSERT INTO roles (role) values("Mentor");
INSERT INTO roles (role) values("Visitor");
select * from roles;

INSERT INTO users (name, email) values ("Aaryan", "Aaryan@gmail.com");
SELECT * FROM users;
-- delete from users;

INSERT INTO authentication (username, password, uid, create_at) values ("naugs", "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", 21, now());
select * from authentication;
UPDATE authentication SET password = "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5" WHERE id = 6;

INSERT INTO user_roles (uid, role_id) values (21, 1);
select * from roles;
select * from users;
select * from user_roles;
update user_roles set role_id = 4 where uid = 23;
select * from courses;
delete from courses where id = 37;
delete from mentor_course where cid = 37;
select * from mentor_course;
select * from student_course;
select * from course_feedback;
select * from course_faq;
UPDATE courses SET status = "active" WHERE id = 9;
SELECT * FROM courses, student_course WHERE uid = 24 and student_course.cid = courses.id;

INSERT INTO course_feedback (cid, uid, rating, comments, created_at) VALUES (5, 24, 4.5, "good course", now());
SELECT * FROM course_feedback;

SELECT * FROM mentor_course, courses WHERE uid = 22 AND mentor_course.cid = courses.id;