from . import views
from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    path('',views.index,name='index'),
    path('verify_code/', views.verify_code),
    path('register/', views.register.as_view(), name='register'),
    path('guan/',views.guan,name='guan'),
    path('guanzhu/<int:sid>/',views.guanzhu,name='guanzhu'),
    path('guanzhurenyuan/',views.renyuan,name='guanzhurenyuan'),
    path('dds/<int:sid>/',views.dd,name='dd'),
    path('wenzhang/',views.wenzhang,name='wenzhang'),
    path('del/<int:sid>/',views.del_ArticleModel,name='del'),
    path('haoyou/',views.haoyou,name='haoyou'),
    path('chazhao/',views.chazhao,name='chazhao'),
    path('dd/<str:sd>/',views.de,name='de'),
    path('login/',views.LIndex.as_view(),name='login'),
    path('per_home/',views.per_home,name='per_home'),
    path('flush/',views.flush,name='flush'),
    path('thumbsup/<int:sid>/',views.thumbsup,name='thumbsup'),
    path('repyle1/<int:id>/',views.repyle1,name='repyle1'),
    path('pinglun/<int:sid>/',views.pinglun,name='pinglun'),
    path('write_ArticleModel/',views.write_ArticleModel,name='write_ArticleModel'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
