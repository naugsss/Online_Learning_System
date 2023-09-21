from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from src.controllers.courses import Courses
from src.controllers.faq import Faq
from src.controllers.feedback import Feedback
from src.helpers.entry_menu import EntryMenu
from src.schemas import CourseSchema, PurchaseCourseSchema, FeedbackSchema, FaqSchema

blp = Blueprint("Courses", "Courses", description="operations on courses")


@blp.route("/courses")
class Course(MethodView):
    # function to list all the courses present
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")
        user_id = jwt.get("user_id")

        instance = Courses()
        content = instance.list_course(4, user_id)

        if role == 1:
            return list_course_role_1(content)
        elif role == 2 or role == 4:
            return list_course_role_2_or_role_4(content)
        elif role == 3:
            print("Hii")
            # print(content)
            content = instance.list_course(role, user_id)
            print(content)
            return list_course_role_3(content)

    # @blp.response(CourseSchema)
    # function to add a new course
    @blp.arguments(CourseSchema)
    @jwt_required()
    def post(self, user_data):
        instance = Courses()
        # print("inside post method")
        try:
            jwt = get_jwt()
            user_id = jwt.get("user_id")
            response = instance.add_course(user_id=user_id, course_name=user_data["name"],
                                           content=user_data["content"], duration=user_data["duration"],
                                           price=user_data["price"])
            return {"message": "Course approval request sent to the admin"}
        except Exception as error:
            print(error)
            abort(401, message="Invalid credentials.")

    # mark a course as deactive
    @blp.arguments(CourseSchema)
    def delete(self, user_data):
        instance = Courses()
        instance.delete_course(user_data["name"])
        return {"message": "course marked as deactivated successfully."}

    # @blp.arguments(CourseSchema)
    # def put(self, user_data):
    #     instance = Courses()
    #     instance.approve_course()


def list_course_role_1(content):
    response = []
    for val in content:
        name = val[1]
        duration = val[3]
        price = val[4]
        rating = val[5]
        status = val[8]

        return_dict = {
            "name": name,
            "duration": duration,
            "price": price,
            "rating": rating,
            "status": status
        }

        response.append(return_dict)
    return response


def list_course_role_3(content):
    response = []
    # values.append([row[4], row[6], row[7], row[8], row[10], row[7] * row[10]])
    for val in content:
        name = val[0]
        duration = val[1]
        price = val[2]
        rating = val[3]
        no_of_students = val[4]
        # print(type(no_of_students))
        earning = val[5]

        return_dict = {
            "name": name,
            "duration (in hrs.)": duration,
            "price": price,
            "rating": rating,
            "no_of_students": no_of_students,
            "earning (in Rs.)": earning
        }
        response.append(return_dict)
    # print(response)
    return response


def list_course_role_2_or_role_4(content):
    response = []
    for val in content:
        name = val[1]
        duration = val[3]
        price = val[4]
        rating = val[5]

        return_dict = {
            "name": name,
            "duration": duration,
            "price": price,
            "rating": rating,
        }

        response.append(return_dict)
    return response

# function to purchase a course
@blp.route("/courses/<string:course_name>")
class AccessCourse(MethodView):
    @jwt_required()
    # @blp.arguments(PurchaseCourseSchema)
    def post(self, course_name):

        instance = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        entrymenu = EntryMenu()
        content = instance.list_course(4, user_id)
        name, course_id = entrymenu.check_valid_course(course_name, content)
        message = instance.purchase_course(user_id, course_id)
        return {"message": message}

# function to access the course content
    @jwt_required()
    def get(self, course_name):
        instance = Courses()
        content = instance.view_course_content(course_name)
        return {"content": content}



@blp.route("/courses/<string:course_name>/user_feedback")
class accessFeedback(MethodView):

    #function to add feedback to courses
    @jwt_required()
    @blp.arguments(FeedbackSchema)
    # isme pehle body aati h jo item mein aari h and then dynamic values
    def post(self, user_feedback, course_name):

        feedback = Feedback()
        instance = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        content = instance.list_course(4, user_id)
        entrymenu = EntryMenu()
        ratings = user_feedback["ratings"]
        comments = user_feedback.get("comments")
        if not comments:
            comments = "No comments"
        name, course_id = entrymenu.check_valid_course(course_name, content)
        feedback.add_course_feedback(course_id, ratings, comments, user_id)
        return {"message": "Feedback added successfully"}

# function to view feedback of courses
    @jwt_required()
    def get(self, course_name):
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        instance = Courses()
        content = instance.list_course(4, user_id)
        entrymenu = EntryMenu()
        feedback = Feedback()
        name, course_id = entrymenu.check_valid_course(course_name, content)
        feedback = feedback.view_course_feedback(course_id)
        if feedback is None:
            return {"message": "No feedback exists for this course"}
        print(feedback)
        response = []
        for val in feedback:
            rating = val[3]
            comment = val[4]

            return_dict = {
                "rating": rating,
                "comment": comment
            }
            response.append(return_dict)

        return response


@blp.route("/courses/<string:course_name>/user_faq")
class accessFaq(MethodView):

    #function to add FAQ to courses
    # @jwt_required()
    # @blp.arguments(FaqSchema)
    # # isme pehle body aati h jo item mein aari h and then dynamic values
    # def post(self, user_feedback, course_name):
    #
    #     faq = Faq()
    #     instance = Courses()
    #     jwt = get_jwt()
    #     user_id = jwt.get("user_id")
    #     content = instance.list_course(4, user_id)
    #     entrymenu = EntryMenu()
    #     question = user_feedback["question"]
    #     answer = user_feedback.get("answer")
    #
    #     name, course_id = entrymenu.check_valid_course(course_name, content)
    #     faq.add_faq(course_id, ratings, comments, user_id)
    #     return {"message": "Feedback added successfully"}

# function to view FAQ of courses
    @jwt_required()
    def get(self, course_name):
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        instance = Courses()
        content = instance.list_course(4, user_id)
        entrymenu = EntryMenu()
        faq = Faq()
        name, course_id = entrymenu.check_valid_course(course_name, content)
        faq = faq.view_faq(course_name)
        if faq is None:
            return {"message": "No Faq exists for this course"}
        # print(feedback)
        response = []
        for val in faq:
            answer = val[14]
            question = val[13]

            return_dict = {
                "question": question,
                "answer": answer
            }
            response.append(return_dict)

        return response



