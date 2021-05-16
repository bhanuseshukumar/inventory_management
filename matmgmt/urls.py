"""department URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from matmgmt import views
urlpatterns = [
    path('', views.index, name='matmgmt_home'),
    path('list_material/',views.show_material, name = "material_master"),
    path('add_material/', views.create_material_master, name='add-material'),
    path('material/<int:pk>/material-edit',views.material_edit, name='material-edit'),
    path('material/<int:pk>/material-delete',views.material_delete, name='material-delete'),


    path('stock_list/', views.inventoryListView, name='stock-list'),
    path('stock/<int:pk>/add', views.add_stock, name = 'add-stock'),
    path('stock/<int:pk>/stock-edit', views.stock_edit, name = 'stock-edit'),
    path('stock/<int:pk>/stock-delete', views.stock_delete, name = 'stock-delete'),

    path('reservations_list/',views.reservationsListView, name = 'reservations-list'),
    path('reservation/<int:pk>/add',views.add_reservation, name = 'add-reservation'),
    path('reservation/<int:pk>/reservation-edit', views.reservation_edit, name='reservation-edit' ),
    path('reservation/<int:pk>/reservation-delete', views.reservation_delete, name='reservation-delete' ),
    path('reservation/<int:pk>/filter' ,views.reservationsFilterView, name = 'reservation-filter'),
    path('reservation/<int:pk>/consume', views.consume, name='consume' ),
    
    path('issues/',views.issuesListView,name = 'issues-list'),
    path('issue/<int:pk>/issue-edit', views.issue_edit, name='issue-edit' ),
    path('issue/<int:pk>/issue-delete', views.issue_delete, name='issue-delete' ),
    path('issue/<int:pk>/filter' ,views.issueFilterView, name = 'issue-filter'),

    path('storeloc/add',views.addLocation, name= 'add-location'),
    
    path('signup',views.signupView, name= 'signup'),
    
    path('test',views.test,name='test'),
    


    
]
