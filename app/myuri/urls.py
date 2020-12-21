from django.urls import path, include

from . import views


api_patterns = [
    path('comic/', views.api.ComicList.as_view(), name='api-comic-list'),
    path('comic/<int:pk>', views.api.ComicDetail.as_view(), name='api-comic-detail'),
    path('chapter/', views.api.ChapterList.as_view(), name='api-chapter-list'),
    path('chapter/<int:pk>', views.api.ChapterDetail.as_view(), name='api-chapter-detail')
]


urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    # Add all paths for the API
    path('api/', include(api_patterns))
]
