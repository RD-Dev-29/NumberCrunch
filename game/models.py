from django.db import models


class Puzzle(models.Model):
    puzzle_date = models.DateField("Puzzle Date")
    puzzle_mode = models.CharField(max_length=8)
    puzzle_type = models.CharField(max_length=4)
    puzzle_start = models.IntegerField()
    puzzle_goal = models.IntegerField()


class PuzzleDistinctSolution(models.Model):
    puzzle = models.ForeignKey('Puzzle', on_delete=models.CASCADE)
    unique_sol = models.CharField(max_length=50)
    found = models.BooleanField()
