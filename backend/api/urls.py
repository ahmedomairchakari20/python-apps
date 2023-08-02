from django.urls import path
from . import views

urlpatterns = [
     path('', views.DefaultView.as_view(), name='default'), 
     path('signup', views.SignupView.as_view(), name='signup'),
     path('login', views.UserLoginView.as_view(), name='login'),
     path('forgetPassword', views.ForgetPasswordView.as_view(), name='forgetPassword'),
     path('change_password',views.changepassword.as_view(), name='change_password'),
     path('resetpassword',views.newPassword.as_view(), name='resetpassword'),
     path('add', views.TaskView.as_view(), name='add'),
     path('percentage', views.TaskPercentage.as_view(), name='percentage'),
     path('update', views.UpdateProfileView.as_view(), name='add'),
     path('dashboard', views.DashboardView.as_view(), name= "dashboard"),
     path('search', views.SearchView.as_view(), name="search"),
     path('movetoprogress', views.ProgressView.as_view(), name="inprogress"),
     path('markascomplete', views.CompleteView.as_view(), name="inprogress"),
     path('updateuser',views.ProfileData.as_view(),name='updateuser'),


]