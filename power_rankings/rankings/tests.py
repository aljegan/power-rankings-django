from django.test import TestCase
from datetime import datetime
from .models import Match, Player
from .utils import calculate_elo_win_probabilities, calculate_new_rankings
from django.utils.timezone import make_aware
import pytz
from django.core.exceptions import ValidationError
from unittest.mock import patch


PUB_DATE = make_aware(datetime.utcnow(), timezone=pytz.timezone("UTC"))


class MatchModelTests(TestCase):
    def setUp(self):
        Player.objects.create(player_name="player1", ranking=800.0)
        Player.objects.create(player_name="player2", ranking=800.0)
        Player.objects.create(player_name="player3", ranking=800.0)

    def tearDown(self):
        Match.objects.all().delete()
        Player.objects.all().delete()

    def test_string(self):
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")

        match = Match(
            player1=player1,
            player2=player2,
            winner=player1,
            pub_date=PUB_DATE,
        )
        match.id = 42
        self.assertEqual(
            str(match), f"42: {str(player1)} <> {str(player2)} ({str(player1)})"
        )

    def test_string_tie(self):
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")

        match = Match(
            player1=player1,
            player2=player2,
            winner=None,
            pub_date=PUB_DATE,
        )
        match.id = 42
        self.assertEqual(str(match), f"42: {str(player1)} <> {str(player2)} (TIE)")

    def test_winner_not_involved_in_match_raises_exception(self):
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")
        player3 = Player.objects.get(player_name="player3")

        match = Match(
            player1=player1,
            player2=player2,
            winner=player3,
            pub_date=PUB_DATE,
        )
        self.assertRaises(
            ValidationError,
            match.clean,
        )

    @patch("rankings.models.calculate_new_rankings")
    def test_player_rankings_change_based_on_outcome_player1_wins(
        self, mock_calculate_new_rankings
    ):
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")
        match = Match(
            player1=player1,
            player2=player2,
            winner=player1,
            pub_date=PUB_DATE,
        )

        mock_calculate_new_rankings.return_value = (850.0, 750.0)
        match.save()
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")

        self.assertAlmostEqual(player1.ranking, 850.0)
        self.assertAlmostEqual(player2.ranking, 750.0)
        mock_calculate_new_rankings.assert_called_with(800.0, 800.0, winner_is_1=True)

    @patch("rankings.models.calculate_new_rankings")
    def test_player_rankings_change_based_on_outcome_player2_wins(
        self, mock_calculate_new_rankings
    ):
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")
        match = Match(
            player1=player1,
            player2=player2,
            winner=player2,
            pub_date=PUB_DATE,
        )

        mock_calculate_new_rankings.return_value = (850.0, 750.0)
        match.save()
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")

        self.assertAlmostEqual(player1.ranking, 850.0)
        self.assertAlmostEqual(player2.ranking, 750.0)
        mock_calculate_new_rankings.assert_called_with(800.0, 800.0, winner_is_1=False)

    @patch("rankings.models.calculate_new_rankings")
    def test_player_rankings_change_based_on_outcome_tie(
        self, mock_calculate_new_rankings
    ):
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")
        match = Match(
            player1=player1,
            player2=player2,
            winner=None,
            pub_date=PUB_DATE,
        )

        mock_calculate_new_rankings.return_value = (850.0, 750.0)
        match.save()
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")

        self.assertAlmostEqual(player1.ranking, 850.0)
        self.assertAlmostEqual(player2.ranking, 750.0)
        mock_calculate_new_rankings.assert_called_with(800.0, 800.0, winner_is_1=None)

    def test_winner_can_be_none(self):
        player1 = Player.objects.get(player_name="player1")
        player2 = Player.objects.get(player_name="player2")

        match = Match(
            player1=player1,
            player2=player2,
            winner=None,
            pub_date=PUB_DATE,
        )
        match.clean()
        match.save()


class PlayerModelTests(TestCase):
    def setUp(self):
        Player.objects.create(player_name="player1", ranking=800.0)

    def tearDown(self):
        Player.objects.all().delete()

    def test_string(self):
        player1 = Player.objects.get(player_name="player1")
        self.assertEqual(str(player1), "player1")


class UtilsTests(TestCase):
    def test_calculate_elo_win_probabilities(self):
        self.assertTupleEqual(
            calculate_elo_win_probabilities(1000.0, 1000.0), (0.5, 0.5)
        )

        # same difference in elo -> same probabilities
        probs_a = calculate_elo_win_probabilities(1000, 700)
        probs_b = calculate_elo_win_probabilities(1500, 1200)
        self.assertAlmostEqual(probs_a[0], probs_b[0])
        self.assertAlmostEqual(probs_a[1], probs_b[1])

        difference_100 = calculate_elo_win_probabilities(1000, 900)
        self.assertAlmostEqual(difference_100[0], 0.6401, 2)
        self.assertAlmostEqual(difference_100[0] + difference_100[1], 1)

        difference_400 = calculate_elo_win_probabilities(1000, 600)
        self.assertAlmostEqual(difference_400[0], 0.9091, 2)
        self.assertAlmostEqual(difference_400[0] + difference_400[1], 1)

    def test_calculate_new_ratings(self):
        self.assertTupleEqual(
            calculate_new_rankings(1000.0, 1000.0, None), (1000.0, 1000.0)
        )

        # same difference in elo -> same probabilities
        ratings_a = calculate_new_rankings(1000, 700, None)
        ratings_b = calculate_new_rankings(1500, 1200, None)
        self.assertAlmostEqual(ratings_a[0] + 500, ratings_b[0])
        self.assertAlmostEqual(ratings_a[1] + 500, ratings_b[1])

        difference_100 = calculate_new_rankings(1000, 900, True)
        self.assertAlmostEqual(difference_100[0], (1 - 0.6401) * 20 + 1000, 1)
        self.assertAlmostEqual(difference_100[0] + difference_100[1], 1900)

        difference_400 = calculate_new_rankings(1000, 600, False)
        self.assertAlmostEqual(difference_400[0], 1000 - (0.9091 * 20), 1)
        self.assertAlmostEqual(difference_400[0] + difference_400[1], 1600)
