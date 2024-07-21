from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
	path('', views.index, name='index'),
	path('index/', views.index, name='index'),
	path('contact/', views.contact, name='contact'),
	path('category/<str:foo>', views.category, name='category'),
	path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
	path('update_user/', views.update_user, name='update_user'),
	path('update_password/', views.update_password, name='update_password'),
	path('update_info/', views.update_info, name='update_info'),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register_user, name='register'),
	path('category_summary/', views.category_summary, name='category_summary'),
	path('search/', views.search, name='search'),
]