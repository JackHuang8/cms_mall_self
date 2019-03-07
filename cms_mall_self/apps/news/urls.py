from django.conf.urls import url

from news import views

urlpatterns = [
    url(r'^news/top/$', views.NewsTopView.as_view()),
    url(r'^news/category/$', views.NewsCategoryView.as_view())
]
