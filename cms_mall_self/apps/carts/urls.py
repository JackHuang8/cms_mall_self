from django.conf.urls import url

from carts import views

urlpatterns = [
    url(r'^cart/$',views.CartView.as_view()),
    url(r'^cart/selected/$',views.SelecteAll.as_view()),
    url(r'^cart/count/$',views.CartCountView.as_view()),
]
