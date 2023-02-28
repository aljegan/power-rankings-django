from django.db import models
from django.core.exceptions import ValidationError
from .utils import calculate_new_rankings


class Player(models.Model):
    player_name = models.CharField(max_length=200)
    ranking = models.FloatField(max_length=200)

    def __str__(self):
        return f"{self.player_name}"


class Match(models.Model):
    player1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="match_player1"
    )
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="match_player2"
    )
    winner = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="match_winner",
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField("date published")

    class Meta:
        verbose_name_plural = "matches"

    def clean(self):
        if self.winner is not None and self.winner not in (self.player1, self.player2):
            raise ValidationError("winner must be one of the players in the match!")

    def save(self, *args, **kwargs):
        player1_wins = self.winner == self.player1 if self.winner is not None else None
        player1_new_ranking, player2_new_ranking = calculate_new_rankings(
            self.player1.ranking, self.player2.ranking, winner_is_1=player1_wins
        )

        self.player1.ranking = player1_new_ranking
        self.player2.ranking = player2_new_ranking
        self.player1.save()
        self.player2.save()
        super(Match, self).save(*args, **kwargs)

    def __str__(self):
        winner = str(self.winner) if self.winner is not None else "TIE"
        return f"{self.id}: {self.player1} <> {self.player2} ({winner})"

    # TODO: add functionality to update player rankings when they
