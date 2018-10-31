from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    url(r'^$',views.main_page,name='main_page'),
    url('signin/', views.signin, name='signin'), ## 로그인 화면
    url('signup/', views.signup, name='signup'),
    url('logout/',auth_views.LogoutView.as_view(), name='logout'),
    url('todo_reg/',views.todo_reg,name='todo_reg'),
]