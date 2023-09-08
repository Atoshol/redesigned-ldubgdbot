from ldubgdbot.bot.database.main import Database
from ldubgdbot.bot.database.methods.get import *


db = Database()
conn = db.get_connection()
cursor = db.get_cursor()


def delete_teacher(user_id):
    teacher_id = get_teacher_id(user_id)
    cursor.execute(f"DELETE FROM public.api_user "
                   f"WHERE user_id={user_id}")

    cursor.execute(f"DELETE FROM public.api_teacher "
                   f"WHERE id={teacher_id}")
    conn.commit()


def delete_student(user_id):
    student_id = get_student_id(user_id)
    cursor.execute(f"DELETE FROM public.api_user "
                   f"WHERE user_id={user_id}")

    cursor.execute(f"DELETE FROM public.api_student "
                   f"WHERE id={student_id}")
    conn.commit()


def delete_admin(user_id):
    admin_id = get_admin_id(user_id)
    cursor.execute(f"DELETE FROM public.api_user "
                   f"WHERE user_id={user_id}")

    cursor.execute(f"DELETE FROM public.api_admin "
                   f"WHERE id={admin_id}")
    conn.commit()
