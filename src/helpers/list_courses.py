from models.fetch_json_data import JsonData
from models.database import DatabaseConnection

DatabaseConnection = DatabaseConnection()

get_query = JsonData.load_data()


def list_my_course(content):
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


def list_course_role_1(content):
    response = []
    for val in content:
        name = val[1]
        duration = val[3]
        price = val[4]
        rating = val[5]
        status = val[8]
        approval_status = val[6]

        return_dict = {
            "name": name,
            "duration (in hrs.)": duration,
            "price (in Rs.)": price,
            "rating": rating,
            "status": status,
            "approval status": approval_status,
        }

        response.append(return_dict)
    return response


def list_course_role_3(content):
    response = []
    for val in content:
        name = val[0]
        duration = val[1]
        price = val[2]
        rating = val[3]
        no_of_students = val[4]
        earning = val[5]

        return_dict = {
            "name": name,
            "duration (in hrs.)": duration,
            "price (in Rs.)": price,
            "rating": rating,
            "no_of_students": no_of_students,
            "earning (in Rs.)": earning,
        }
        response.append(return_dict)
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
            "duration (in hrs.)": duration,
            "price": price,
            "rating (in Rs.)": rating,
        }

        response.append(return_dict)
    return response
