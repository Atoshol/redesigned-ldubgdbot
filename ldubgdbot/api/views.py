from rest_framework import viewsets
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from ldubgdbot.api.models import Student, User, Teacher, Admin, Group
from ldubgdbot.api.serializers import (StudentSerializer, TeacherSerializer, AdminSerializer,
                                       UserSerializer, GroupSerializer)
from functions.get_data import get_user_id_by_student_id, get_user_id_by_teacher_id
import json
from ldubgdbot.bot.utils.env import Env
import requests


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('user_id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['user_id']


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'group']


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all().order_by('id')
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('id')
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'f_name', 'm_name', 'l_name']


@csrf_exempt
def group_list(request):
    """
    base_url/group_list?
        send_to_group = bool True or False&
        group_name = list of groups
        message = string text&
        teacher_f_name= string f_name&
        teacher_m_name= string m_name&
        teacher_l_name= string l_name&
        subject=subject&
    """
    if request.method == "GET" and request.GET.get('send_group_list'):
        group_lst = Group.objects.all()
        context = {'request': request}
        serializer = GroupSerializer(group_lst, many=True, context=context)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        try:
            json_res = json.loads(request.body)
            group_name = json_res['group_name']
            f_name, m_name, l_name = [
                json_res['teacher_f_name'],
                json_res['teacher_m_name'],
                json_res['teacher_l_name']
            ]
            subject = json_res['subject']
            message = json_res['message']
        except KeyError:
            pass

        groups = Group.objects.filter(name__in=group_name).values_list('pk', flat=True)
        group_id = list(groups)
        students = Student.objects.filter(group_id__in=group_id).values_list('pk', flat=True)
        student_ids = list(students)

        message_to_send = f'Ви отримали повідомлення від: {l_name} {f_name} {m_name}\n' \
                          f'Предмет: {subject}\n\n' \
                          f'{message}'

        ids = [get_user_id_by_student_id(i) for i in student_ids]

        for id_ in ids:
            try:
                response = requests.post(
                    url=f'https://api.telegram.org/bot{Env.TOKEN}/sendMessage',
                    data={
                        'chat_id': id_,
                        'text': message_to_send,
                        'parse_mode': 'MarkdownV2'
                    }
                ).json()

            except:
                pass

        return HttpResponse(f'send to {ids}')


@csrf_exempt
def teacher_res(request):
    """
        base_url/teacher_test_message?
            send_to_teacher=True&
            message=text&
            teacher_f_name=f_name&
            teacher_m_name=m_name&
            teacher_l_name=l_name&
            subject=subject&
        """
    if request.method == 'POST':

        json_res = json.loads(request.body)
        f_name, m_name, l_name = [
            json_res['teacher_f_name'],
            json_res['teacher_m_name'],
            json_res['teacher_l_name']
        ]
        subject = json_res['subject']
        message = json_res['message']
        print(f_name, m_name, l_name)
        message_to_send = f'ТЕСТОВЕ ПОВІДОМЛЕННЯ\n\n' \
                          f'Ви отримали повідомлення від: {l_name} {f_name[0]}. {m_name[0]}.\n' \
                          f'Предмет: {subject}\n\n' \
                          f'{message}'

        teacher_lst = Teacher.objects.filter(
            f_name=f_name, m_name=m_name, l_name=l_name
        ).values_list('pk', flat=True)
        teacher_ids = list(teacher_lst)
        ids = [get_user_id_by_teacher_id(i) for i in teacher_ids]
        for id_ in ids:
            try:
                response = requests.post(
                    url=f'https://api.telegram.org/bot{Env.TOKEN}/sendMessage',
                    data={
                        'chat_id': id_,
                        'text': message_to_send,
                        'parse_mode': 'MarkdownV2'
                    }
                ).json()

            except:
                pass

        return HttpResponse(f'send to {ids}')
