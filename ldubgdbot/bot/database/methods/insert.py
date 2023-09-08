from ldubgdbot.bot.database.main import Database


db = Database()
conn = db.get_connection()
cursor = db.get_cursor()


def insert_student(username, f_name, group_id):
    cursor.execute(f"INSERT INTO public.api_student (username,f_name,status_of_subs,group_id) "
                   f"VALUES ('{username}', '{f_name}','{False}','{group_id}')")
    cursor.execute(f"SELECT id FROM public.api_student "
                   f"ORDER BY id ASC")
    data = cursor.fetchall()
    id_s = data[-1][0]
    conn.commit()
    return id_s


def insert_teacher(f_name, m_name, l_name):
    cursor.execute(f"INSERT INTO public.api_teacher (f_name,m_name,l_name,status_of_subs) "
                   f"VALUES ('{f_name}', '{m_name}', '{l_name}','{False}')")
    cursor.execute(f"SELECT id FROM public.api_teacher "
                   f"ORDER BY id ASC")
    data = cursor.fetchall()
    id_t = data[-1][0]
    conn.commit()
    return id_t


def insert_user(user_id, id_s=None, id_t=None, id_a=None):
    if id_s is not None:
        cursor.execute(f"INSERT INTO public.api_user (user_id, status, student_id) "
                       f"VALUES ('{user_id}', 'student', '{id_s}')")
    elif id_t is not None:
        cursor.execute(f"INSERT INTO public.api_user (user_id, status, teacher_id) "
                       f"VALUES ('{user_id}', 'student', '{id_t}')")
    elif id_a is not None:
        cursor.execute(f"INSERT INTO public.api_user (user_id, status, admin_id) "
                       f"VALUES ('{user_id}', 'student', '{id_a}')")
    else:
        return None
    conn.commit()


def insert_admin(username, f_name):
    cursor.execute(f"INSERT INTO public.api_admin (username,f_name) "
                   f"VALUES ('{username}','{f_name}')")
    cursor.execute(f"SELECT id FROM public.api_admin "
                   f"ORDER BY id ASC")
    data = cursor.fetchall()
    id_a = data[-1][0]
    conn.commit()
    return id_a


def insert_group(group_name):
    cursor.execute(f"INSERT INTO public.api_group (name) "
                   f"VALUES ('{group_name}')")
    cursor.execute(f"SELECT id FROM public.api_group "
                   f"ORDER BY id ASC")
    data = cursor.fetchall()
    group_id = data[-1][0]
    conn.commit()
    return group_id
