from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login),
    #url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]