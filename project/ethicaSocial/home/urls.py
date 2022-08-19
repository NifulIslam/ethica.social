from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.newsFeed,name="newsFeed"),
    path('profile/', views.profilePage,name="profile"),
    path('message/', views.message,name="message"),
    path('notification/', views.notification,name="notification"),
    path('settings/', views.settings,name="settings"),
    path('bloodDonatin/', views.bloodDonatin,name="bloodDonatin"),
    path('shop/', views.shop,name="shop"),
    path('jobs/', views.jobs,name="jobs"),
    path('news/', views.news,name="news"),
    path('followersPost/', views.followersPost,name="followersPost"),
    path('followers/', views.followers,name="followers"),
    path('followings/', views.followings,name="followings"),
    path('othersProfile/', views.othersProfile,name="othersProfile"),
    path('othersProfile/', views.othersProfile,name="othersProfile"),
    path('createPost/', views.createPost,name="createPost"),
    path('createPostHandle/', views.createPostHandle,name="createPostHandle"),
    
    
    # path('othersProfile/', views.othersProfile,name="othersProfile"),
       
]