from django.urls import path, include
from snippets import views
from snippets.views import SnippetViewSet, UserViewSet

from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

# snippet_list = SnippetViewSet.as_view(
# {
#         'get': 'list',
#         'post': 'create'
#     }
# )

# snippet_detail = SnippetViewSet.as_view(
#     {
#         'get': 'retrieve',
#         'put': 'update',
#         'delete': 'destroy',
#         'patch': 'partial_update'
#     }
# )

# snippet_highlight = SnippetViewSet.as_view(
#     {
#         'get': 'highlight'
#     },
    
#     renderer_classes=[renderers.StaticHTMLRenderer]
# )

# user_list = UserViewSet.as_view(
#     {
#         'get': 'list'
#     }
# )

# user_detail = UserViewSet.as_view(
#     {
#         'get' : 'retrieve'
#     }
# )

# urlpatterns = [
#     path('', views.api_root),

#     # path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
#     path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),

#     # path('snippets/', views.snippet_list),
#     # path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
#     path('snippets/', snippet_list, name='snippet-list'),

#     # path('snippets/<int:pk>/', views.snippet_detail)
#     # path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),

#     # path('users/', views.UserList.as_view(), name='user-list'),
#     path('users/', user_list, name='user-list'),

#     # path('users/<int:pk>/', views.UserDetail.as_view()),
#     path('users/<int:pk>/', user_detail)
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

from rest_framework.routers import DefaultRouter

# Create arouter and register our viewsets with it.
router  = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
