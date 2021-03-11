from django.urls import path

from dummy_csv import views
from dummy_csv.views import poll_state, delete_schema

urlpatterns = [
    path('', views.SchemasView.as_view(), name='schemas'),
    path('<int:pk>/', views.NewScheme.as_view(), name='schema'),
    path('new/', views.NewScheme.as_view(), name='new_schema'),
    path('<int:pk>/delete/', delete_schema, name='delete_schema'),
    path('<int:pk>/dataset/', views.DatasetsView.as_view(), name='datasets'),
    path('poll_state/', poll_state, name="poll_state"),
]
