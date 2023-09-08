from django.db import models


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40)
    f_name = models.CharField(max_length=40)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    status_of_subs = models.BooleanField(default=False)


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=40)
    m_name = models.CharField(max_length=40)
    l_name = models.CharField(max_length=40)
    status_of_subs = models.BooleanField(default=False)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    f_name = models.CharField(max_length=40)


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True, unique=True)
    status = models.CharField(max_length=20)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
