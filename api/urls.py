from django.urls import path
from .views import index,home,example,user_login,user_logout,device_filter,UserProfileApi,random,LogView,testview
# from .api import LoginApiView,ExampleView,LoginView
from knox import views as knox_views
from .api import CreateUserView, LoginView, ManageUserView,LoginAPI,CreateUserAPI


app_name = "core"

urlpatterns = [
    # path('', home, name="AnimalView"),
    path('index/',index, name="index"),
    path('example/',example, name="example"),
    # path('login/',user_login, name="login"),
    # path('logout/',user_logout, name="logout"),
    path('home/',home, name="home"),
    path('',random, name="basic"),
    # path(r'', LogView.as_view()),
    path(r'test/', testview),
    # path('user-profile/',ExampleView.as_view(), name="LoginApiView"),


    path('create/', CreateUserAPI.as_view(), name="create"),
    path('profile/', ManageUserView.as_view(), name='profile'),
    path('login/', LoginAPI.as_view(), name='knox_login'),
    path('logoutview/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutallview/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]

htmx_urlpatterns = [
path('device_filter/',device_filter, name="device_filter"),
]

urlpatterns += htmx_urlpatterns