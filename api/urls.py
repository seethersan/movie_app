from django.urls import path
from api.views import RoleViewSet, PersonViewSet, MovieViewSet

urlpatterns = [
    path('movies', MovieViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('movies/<int:pk>', MovieViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('persons', PersonViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('persons/<int:pk>', PersonViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('roles/<int:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }))
]