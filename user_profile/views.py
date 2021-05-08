from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import MainCycle, Boost
from .serializer import UserSerializer, UserDetailSerializer, CycleSerializer, CycleSerializerDetail
from rest_framework import generics


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class CycleList(generics.ListAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializer


class CycleDetail(generics.RetrieveAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializerDetail


def call_click(request):
    main_cycle = MainCycle.objects.filter(user=request.user)[0]
    main_cycle.click()
    main_cycle.save()
    return HttpResponse(main_cycle.coinsCount)


def buy_boost(request):
    main_cycle = MainCycle.objects.filter(user=request.user)[0]
    boost = Boost()
    boost.mainCycle = main_cycle
    boost.save()
    boost.upgrade()
    main_cycle.save()
    return HttpResponse(main_cycle.clickPower)

