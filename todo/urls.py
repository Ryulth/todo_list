from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    url(r'^$',views.main_page,name='main_page'),
    url('test/', views.test, name='test'),
    url('signin/', views.signin, name='signin'), ## 로그인 화면
    url('signup/', views.signup, name='signup'),
    url('logout/',auth_views.LogoutView.as_view(), name='logout'),
    url('todo_reg/',views.todo_reg,name='todo_reg'),
    url('todo_type/(?P<pk>\d+)/$',views.todo_type,name='todo_type'),
    url('todo_del/(?P<pk>\d+)/$',views.todo_del,name='todo_del'),
    url('todo_reload/(?P<pk>\d+)/$',views.todo_reload,name='todo_reload'),
    url('todo_detail/(?P<pk>\d+)/$',views.todo_detail,name='todo_detail'),
    url('todo_edit/(?P<pk>\d+)/$',views.todo_edit,name='todo_edit'),
    url('todo_suc/(?P<pk>\d+)/$',views.todo_suc,name='todo_suc'),
]