from django.urls import path
from .views import index,home,example,user_login,user_logout,device_filter,UserProfileApi
# from .api import LoginApiView,ExampleView,LoginView
from knox import views as knox_views
from core.api import CreateUserView, LoginView, ManageUserView,LoginAPI


app_name = "core"

urlpatterns = [
    # path('', home, name="AnimalView"),
    path('index/',index, name="index"),
    path('example/',example, name="example"),
    # path('login/',user_login, name="login"),
    # path('logout/',user_logout, name="logout"),
    path('home/',home, name="home"),

    # path('user-profile/',ExampleView.as_view(), name="LoginApiView"),


    path('create/', CreateUserView.as_view(), name="create"),
    path('profile/', ManageUserView.as_view(), name='profile'),
    path('new/', NewView.as_view(), name='new'),

    path('login/', LoginAPI.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]

htmx_urlpatterns = [
path('device_filter/',device_filter, name="device_filter"),
]

urlpatterns += htmx_urlpatterns