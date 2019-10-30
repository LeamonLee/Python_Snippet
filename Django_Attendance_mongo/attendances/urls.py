from django.urls import path
from .views import (
    AttendanceListView,
    UserAttendanceListView
)
# from . import views

app_name = "attendances"

urlpatterns = [
    # path('', views.attendance_list, name="list"),
    path('', AttendanceListView.as_view(), name="list"),
    path('user/<str:username>', UserAttendanceListView.as_view(), name='user-list'),
]