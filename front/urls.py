from django.urls import path
from front import views


urlpatterns=[
    path("",views.index,name="index"),
    path('index',views.index,name='index'),
    path('maths',views.index,name='index'),
    path('yuwen',views.yuwen,name="yuwen"),
    path('english',views.english,name="english"),
]

