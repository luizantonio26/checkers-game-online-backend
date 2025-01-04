
import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class GameMatch(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4(), editable=False)
    status_choices = [
        ('playing', 'Playing'),
        ('finished', 'Finished'),
        ('canceled', 'Canceled'),
        ('surrendered', 'Surrendered'),
    ]
    
    match_date = models.DateTimeField(auto_now_add=True)
    white_player = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="white_player",
    )
    black_player = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="black_player",
    )
    winner = models.CharField(max_length=255, null=True, blank=True)
    game_status = models.CharField(max_length=255, choices=status_choices)

    class Meta:
        verbose_name = _("GameMatch")
        verbose_name_plural = _("GameMatches")

    def get_absolute_url(self):
        return reverse("GameMatch_detail", kwargs={"pk": self.pk})

class GameMatchMovement(models.Model):
    PIECE_COLORS = [
        ('white', 'White'),
        ('black', 'Black'),
    ]
    PIECE_TYPES = [
        ('normal', 'Normal'),
        ('dama', 'Dama'),
    ]
    
    game_match = models.ForeignKey(GameMatch, on_delete=models.CASCADE)
    piece_color = models.CharField(max_length=6, choices=PIECE_COLORS)
    piece_type = models.CharField(max_length=6, choices=PIECE_TYPES)
    origin_x = models.IntegerField()
    origin_y = models.IntegerField()
    destiny_x = models.IntegerField()
    destiny_y = models.IntegerField()
    state_before_move = models.JSONField()
    state_after_move = models.JSONField()
    was_capture = models.BooleanField()

    class Meta:
        verbose_name = _("GameMatchMovements")
        verbose_name_plural = _("GameMatchMovements")
