from controllers.earning import Earning


def view_every_mentor_earning(user_id=None):
    earning = Earning()

    if user_id is None:
        earning = earning.calculate_mentor_earning()
    else:
        earning = earning.calculate_mentor_earning(user_id)
    if earning is None:
        return {"message": "There are no mentor as of now."}
    response = []
    for value in earning:
        mentor_name = value[0]
        course_name = value[1]
        earning = value[2]

        return_dict = {
            "name": mentor_name,
            "course_name": course_name,
            "earning": earning,
        }
        response.append(return_dict)
    return response
