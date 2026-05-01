from django.urls import path
from . import views

urlpatterns = [
    # Landing
    path('', views.home, name='home'),

    # Auth
    path('login/student/', views.login_student, name='login_student'),
    path('login/alumni/', views.login_alumni, name='login_alumni'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/alumni/', views.register_alumni, name='register_alumni'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),

    # Admin Actions
    path('admin-panel/approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('admin-panel/reject/<int:user_id>/', views.reject_user, name='reject_user'),

    # Alumni
    path('alumni/', views.alumni_list, name='alumni_list'),

    # Mentorship
    path('mentorship/request/<int:alumni_id>/', views.send_mentorship_request, name='send_mentorship_request'),
    path('mentorship/<int:request_id>/<str:action>/', views.handle_mentorship_request, name='handle_mentorship_request'),

    # Messages
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:user_id>/', views.chat, name='chat'),

    # Posts
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='view_profile'),
    path('profile/modal/<int:user_id>/', views.profile_modal, name='profile_modal'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notif_id>/read/', views.mark_notification_read, name='mark_notification_read'),
]
