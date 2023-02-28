from django.db import models
from django.core.exceptions import ValidationError


class Player(models.Model):
    player_name = models.CharField(max_length=200)
    ranking = models.FloatField(max_length=200)

    def __str__(self):
        return f"{self.player_name}"


class Match(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_player1")
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_player2")
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_winner")
    pub_date = models.DateTimeField("date published")

    class Meta:
        verbose_name_plural = "matches"

    def clean(self):
        if self.winner not in (self.player1, self.player2):
            raise ValidationError("winner must be one of the players in the match!")

    def __str__(self):
        return f"{self.id}: {self.player1} <> {self.player2} ({self.winner})"

    # TODO: add functionality to update player rankings when they
