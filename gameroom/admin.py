from django.contrib import admin

from gameroom.models.game_match import GameMatch, GameMatchMovement

# Register your models here.
admin.site.register(GameMatch)
admin.site.register(GameMatchMovement)