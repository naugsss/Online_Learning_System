GET_NAME = "SELECT name FROM users WHERE id = %s"
COURSE_DETAILS = "SELECT price, no_of_students, name, uid FROM courses, mentor_course WHERE courses.id = mentor_course.cid "
GET_COURSES = "SELECT * FROM courses WHERE approval_status = %s"
INSERT_COURSES = "INSERT INTO courses (name, content, duration, price, avg_rating, approval_status, no_of_students, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
GET_STUDENT_COURSES = "SELECT * FROM courses, student_course WHERE uid = %s and student_course.cid = courses.id"
GET_DETAILS_COURSES = "SELECT * FROM courses WHERE name = %s"
GET_COURSES_STATUS = "SELECT * FROM courses WHERE approval_status = %s and status = %s"
PURCHASE_COURSE_UID_CID = "SELECT * FROM student_course where uid = %s and cid = %s"
INSERT_STUDENT_COURSES = "INSERT INTO student_course (uid, cid, purchased_on) VALUES (%s, %s, %s)"
GET_NO_STUDENTS = "SELECT * from courses where id = %s"
UPDATE_NO_OF_STUDENTS = "UPDATE courses SET no_of_students = %s where id = %s"
GET_USER_ROLES = "SELECT * FROM user_roles where uid = %s"
UPDATE_USER_ROLES = "UPDATE user_roles SET role_id = %s WHERE uid = %s"
PENDING_STATUS = "SELECT * FROM courses WHERE approval_status = %s"
UPDATE_PENDING_APPROVAL_STATUS = "UPDATE courses SET approval_status = %s WHERE id = %s"
DELETE_FROM_MENTOR_COURSE = "DELETE FROM mentor_course WHERE cid = %s"
DELETE_FROM_COURSES = "DELETE FROM courses WHERE id = %s"
UPDATE_COURSE_STATUS = "UPDATE courses SET status = %s WHERE name = %s"
GET_FROM_COURSE_FEEDBACK = "SELECT * FROM course_feedback WHERE cid = %s"
INSERT_INTO_COURSE_FEEDBACK = "INSERT INTO course_feedback (cid, uid, rating, comments, created_at) VALUES (%s, %s, %s, %s, %s)"
GET_AVG_RATING_COURSE_FEEDBACK = "SELECT AVG(rating) FROM course_feedback where cid = %s"
UPDATE_AVG_RATING = "UPDATE courses SET avg_rating = %s WHERE id = %s"
GET_FAQ = "SELECT * FROM courses, course_faq WHERE name = %s AND courses.id = course_faq.cid "
GET_FAQ_DETAILS = "SELECT * FROM mentor_course, courses WHERE uid = %s and mentor_course.cid = courses.id"
INSERT_FAQ = "INSERT INTO course_faq (cid, question, answer) VALUES (%s, %s, %s)"
GET_FROM_AUTHENTICATION = "SELECT * FROM authentication WHERE username = %s"
UPDATE_INTO_USER_ROLES = "UPDATE user_roles SET role_id = %s WHERE uid = %s"
GET_EARNING_DATA = "SELECT price, no_of_students, name FROM courses, mentor_course WHERE courses.id = mentor_course.cid AND uid = %s"
GET_USER_DETAILS = "SELECT * FROM student_course"
GET_COURSE_NAME = "SELECT name FROM courses WHERE id = %s"
GET_PENDING_COURSE_COUNT = "SELECT COUNT(approval_status) FROM courses WHERE approval_status = %s and status = %s"
GET_MENTOR_COURSE = "SELECT * FROM mentor_course, courses WHERE uid = %s AND mentor_course.cid = courses.id"







