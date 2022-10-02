import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from Hocheol.settings import MEDIA_ROOT

class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.png")

        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=404, data=dict(message="다시 확인해주세요."))

        if user.check_password(password):
            # TODO 로그인을 성공했다는 정보를 세션 or 쿠키에 넣는다.
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message="다시 확인해주세요."))

class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")

class UploadProfile(APIView):
    def post(self, request):

        # 먼저 파일을 불러오는 과정
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # 요 코드는 그냥 컨트롤 씨 컨트롤 브이 가능
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name
        email = request.data.get('email')

        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)


