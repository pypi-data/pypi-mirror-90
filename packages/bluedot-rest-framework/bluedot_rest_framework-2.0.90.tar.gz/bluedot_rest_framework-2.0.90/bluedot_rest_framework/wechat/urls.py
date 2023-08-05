from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .login.views import WeChatLoginView, WeChatLoginWebSocketView
from .views import JSSdk, OAuth, Token, Menu


urlpatterns = [
    url(r'^wechat/oauth', OAuth.as_view()),
    url(r'^wechat/token', Token.as_view()),
    url(r'^wechat/jssdk', JSSdk.as_view()),
    url(r'^wechat/menu', Menu.as_view()),
    url(r'^wechat/login-websocket', WeChatLoginWebSocketView.as_view()),
    url(r'^wechat/login', WeChatLoginView.as_view()),
]
