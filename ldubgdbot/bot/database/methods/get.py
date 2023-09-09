from ldubgdbot.bot.database.main import Database


db = Database()
conn = db.get_connection()
cursor = db.get_cursor()


def get_status_by_id(user_id):
    cursor.execute(f"SELECT status FROM public.api_user "
                   f"WHERE user_id={user_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None


def get_student_id(user_id):
    cursor.execute(f"SELECT student_id FROM public.api_user "
                   f"WHERE user_id={user_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None


def get_teacher_id(user_id):
    cursor.execute(f"SELECT teacher_id FROM public.api_user "
                   f"WHERE user_id={user_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None


def get_admin_id(user_id):
    cursor.execute(f"SELECT admin_id FROM public.api_user "
                   f"WHERE user_id={user_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None


def get_user_id_by_teacher_id(teacher_id):
    cursor.execute(f"SELECT user_id FROM public.api_user "
                   f"WHERE teacher_id={teacher_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None


def get_user_id_by_student_id(student_id):
    cursor.execute(f"SELECT user_id FROM public.api_user "
                   f"WHERE student_id={student_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None


def get_student_data(student_id):
    cursor.execute(f"SELECT * FROM public.api_student "
                   f"WHERE id={student_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0]
    else:
        return None


def get_teacher_data(teacher_id):
    cursor.execute(f"SELECT id, f_name, m_name, l_name, status_of_subs FROM public.api_teacher "
                   f"WHERE id={teacher_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0]
    else:
        return None


def get_admin_data(admin_id):
    cursor.execute(f"SELECT * FROM public.api_admin "
                   f"WHERE id={admin_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0]
    else:
        return None


def get_group_name_by_id(group_id):
    cursor.execute(f"SELECT name FROM public.api_group "
                   f"WHERE id={group_id}")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None


def get_group_id_by_name(group_name):
    cursor.execute("SELECT id from public.api_group "
                   f"WHERE name='{group_name}'")
    data = cursor.fetchall()
    conn.commit()
    if data:
        return data[0][0]
    else:
        return None
