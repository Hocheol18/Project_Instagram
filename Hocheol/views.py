from django.shortcuts import render
from rest_framework.views import APIView

class Sub(APIView):
    def get(self, request):
        return render(request, "Hostagram/main.html")

    def post(self, request):
        return render(request, "Hostagram/main.html")