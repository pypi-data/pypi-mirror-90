from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .response.views import WeChatResponseEventView, WeChatResponseMaterialView
from .response.response import Response
from .login.views import WeChatLoginView, WeChatLoginWebSocketView
from .views import JSSdk, OAuth, Token, Menu


urlpatterns = [
    url(r'^wechat/response', Response.as_view()),
    url(r'^wechat/oauth', OAuth.as_view()),
    url(r'^wechat/token', Token.as_view()),
    url(r'^wechat/jssdk', JSSdk.as_view()),
    url(r'^wechat/menu', Menu.as_view()),
    url(r'^wechat/login-websocket', WeChatLoginWebSocketView.as_view()),
    url(r'^wechat/login', WeChatLoginView.as_view()),
]

router = DefaultRouter(trailing_slash=False)

router.register(r'wechat/response/material', WeChatResponseMaterialView,
                basename='wechat-response-material')
router.register(r'wechat/response/event', WeChatResponseEventView,
                basename='wechat-response-event')
urlpatterns += router.urls
