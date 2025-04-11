from django.urls import path
from .views import register, login, logout, user_dashboard, admin_dashboard, add_app, update_app, get_subcategories, submit_task, view_tasks, view_points, show_joke

urlpatterns = [
    
    path('register/', register, name='register'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    
    
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    
    path('add_app/', add_app, name='add_app'),
    path('update_app/<int:app_id>/', update_app, name='update_app'),
    path('get_subcategories/', get_subcategories, name='get_subcategories'),
    
    path('submit_task/<int:app_id>/', submit_task, name='submit_task'),
    
    path('tasks/', view_tasks, name='task_page'),
    path('points/', view_points, name='points_page'),
    
    path('see_joke/', show_joke, name='show_joke'),

    
]



