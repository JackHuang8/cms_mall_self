from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^goods/recomment/$', views.GoodsRecommentView.as_view()),
    url(r'^goods/category/$', views.GoodsCategoryView.as_view()),

    url(r'^goods/daohang/(?P<pk>\d+)/$', views.GoodsDaohangView.as_view()),
    url(r'^goods/list/(?P<pk>\d+)/$', views.GoodsListView.as_view()),
    url(r'^goods/detail/(?P<pk>\d+)/$', views.GoodsDetailView.as_view()),
]
