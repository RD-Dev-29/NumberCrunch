from django.contrib import admin
from .models import PuzzleDistinctSolution, Puzzle

# Register your models here.

admin.site.register(Puzzle)
admin.site.register(PuzzleDistinctSolution)
