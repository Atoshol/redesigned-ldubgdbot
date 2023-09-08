from ldubgdbot.api.models import User, Teacher, Student, Admin, Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name'
        ]


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    group_id = serializers.IntegerField(source="group.id")

    class Meta:
        model = Student
        fields = [
            'id',
            'username',
            'f_name',
            'group_id',
            'status_of_subs'
        ]


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'f_name',
            'm_name',
            'l_name',
            'status_of_subs'
        ]


class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admin
        fields = [
            'id',
            'username',
            'f_name'
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'status',
            'student_id',
            'teacher_id',
            'admin_id'
        ]
