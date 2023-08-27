def get_pending_course_count():
    try:
        with open("C:\coding\WG\watchguard_daily_task_Aaryan\Online-Learning-System-Project\src\models\global_var",'r') as file:
            val = file.read()
            return int(val)
    except FileNotFoundError:
        return None


def update_pending_course_count(value):
    with open("C:\coding\WG\watchguard_daily_task_Aaryan\Online-Learning-System-Project\src\models\global_var",
              'w') as file:
        file.write(str(value))
