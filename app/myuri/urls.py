from django.urls import path, include

from . import views


api_patterns = [
    path('comic/', views.APIComicList.as_view(), name='api-comic-list'),
    path('comic/<int:pk>', views.APIComicDetail.as_view(), name='api-comic-detail'),
    path('chapter/', views.APIChapterList.as_view(), name='api-chapter-list'),
    path('chapter/<int:pk>', views.APIChapterDetail.as_view(), name='api-chapter-detail')
]


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('comics', views.ComicList.as_view(), name='comics'),
    path('comics/<int:pk>', views.ComicDetail.as_view(), name='comic-detail'),

    # Add all paths for the API
    path('api/', include(api_patterns))
]
