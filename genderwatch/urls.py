"""URLS"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from genderwatch import views

urlpatterns = [
    url(r'^$', views.AssemblyListView.as_view(), name="assembly-list"),
    url(r'^assembly/(?P<pk>[0-9]+)/$', views.AssemblyDetailView.as_view(), name="assembly-detail"),
    url(r'^assembly/(?P<pk>[0-9]+)/stat/$', views.AssemblyStatView.as_view(), name="assembly-stat"),
    url(r'^init-verdict/(?P<pk>[0-9]+)/$', views.init_verdict, name="init-verdict"),
    url(r'^update-verdict/$', views.update_verdict, name="update-verdict"),
    url(r'^event-create/$', views.event_create, name="event-create"),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(
        template_name='genderwatch/registration/login.html'), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(
        template_name='genderwatch/registration/logged_out.html'), name='logout'),
    url(r'^accounts/password-change/$', auth_views.PasswordChangeView.as_view(
        template_name='genderwatch/registration/password_change_form.html'),
        name='password_change'),
    url(r'^accounts/password-change/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='genderwatch/registration/password_change_done.html'),
        name='password_change_done'),
]
