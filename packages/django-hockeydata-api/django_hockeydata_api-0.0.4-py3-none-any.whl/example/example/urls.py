"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('game_slider/', views.game_slider, name='game_slider'),
    path('live_games/', views.live_games, name='live_games'),
    path('standings/', views.standings, name='standings'),
    path('schedule/', views.schedule, name='schedule'),
    path('knockout_stage/', views.knockout_stage, name='knockout_stage'),

    path('game_report/<str:gameId>/', views.game_report, name='game_report'),
    path('game_livebox/<str:gameId>/<str:divId>', views.game_livebox, name='game_livebox'),

    path('player_stats/', views.player_stats, name='player_stats'),
    path('full_player/<str:playerId>/', views.full_player, name='full_player'),
    path('team_fullpage/<str:teamId>/',
         views.team_fullpage, name='team_fullpage'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
