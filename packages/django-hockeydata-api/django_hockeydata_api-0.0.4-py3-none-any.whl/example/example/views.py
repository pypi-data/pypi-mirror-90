# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.conf import settings


sample_div = getattr(settings, 'EXAMPLE_DIV', '')

def home(request):
    return render(request, 'home.html', {})


def game_slider(request):
    return render(request, 'game_slider.html', {})


def live_games(request):
    return render(request, 'live_games.html', {
        'divId': sample_div
    })


def standings(request):
    return render(request, 'standings.html', {
        'divId': sample_div
    })


def schedule(request):
    return render(request, 'schedule.html', {
        'divId': sample_div
    })


def knockout_stage(request):
    po_div = getattr(settings, 'EXAMPLE_PO_DIV', '')
    return render(request, 'knockout_stage.html', {
        'divId': po_div
    })


def game_report(request, gameId):
    return render(request, 'game_report.html', {
        'gameId': gameId, 
        'divId': sample_div
    })


def game_livebox(request, gameId, divId):
    return render(request, 'game_livebox.html', {
        'gameId': gameId,
        'divId': divId
    })


def game_playbyplay(request, gameId):
    return render(request, 'game_playbyplay.html', {
        'gameId': gameId,
        'divId': sample_div
    })


def player_stats(request):
    return render(request, 'player_stats.html', {
        'divId': sample_div
    })


def full_player(request, playerId):
    return render(request, 'full_player.html', {
        'playerId': playerId,
        'divId': sample_div
    })


def team_fullpage(request, teamId):
    return render(request, 'team_fullpage.html', {
        'teamId': teamId,
        'divId': sample_div
    })
