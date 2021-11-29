from django.urls import path
from . import views
from .views import ClubChartView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    # for sending the mail to subscribers
    path('home', views.home, name='home'),

    # view for register popup
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),

    # view for reset password
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # view for logout
    path('logout', views.logout, name="logout"),

    path('change_password', views.change_password, name='change_password'),
    path('change_password_view', views.change_password_view,
         name='change_password_view'),

    path('agent', views.agent, name='agent'),
    path('agent_details/<int:id>', views.agent_details, name='agent-details'),

    path('submit_property', views.submit_property, name='submit-property'),
    path('single_property/<int:p_id>', views.single_property, name='single-property'),
    path('user_reviews/<int:property_id>', views.user_reviews, name="user_reviews"),
    #path('property_type/<str:property_status>', views.property_type, name='property-type'),
    #path('single_property', views.single_property, name='single-property'),
    # path('property_type/<int:p_type>', views.property_type, name='property-type'),
    path('property_type/', views.property_type, name='property-type'),

    path('user_dashboard', views.user_dashboard, name='user-dashboard'),
    path('chart', ClubChartView.as_view(), name='chart'),
    path('user_profile', views.user_profile, name='user-profile'),
    path('user_property', views.user_property, name='user-property'),
    path('delete_property/<int:property_id>', views.delete_property, name="delete_property"),
    path('edit_property/<int:property_id>', views.edit_property, name="edit_property"),
    path('edit_property_view', views.edit_property_view, name='edit_property_view'),
    path('view_property/<int:property_id>', views.view_property, name="view_property"),
    path('add_bookmark/<int:property_id>', views.add_bookmark, name="add_bookmark"),
    path('user_bookmark_list', views.user_bookmark_list, name='user-bookmark_list'),
    path('delete_bookmark/<int:property_id>', views.delete_bookmark, name="delete_bookmark"),


    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('faq', views.faq, name='faq'),
    path('privacy', views.privacy, name='privacy'),
    path('404', views.not_found_404, name='404'),
    path('subscribe', views.subscribe, name='subscribe'),
]
