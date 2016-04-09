
# django-drf imports
from rest_framework import serializers

# app level imports
from .models import Player, Team


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'id', 'name', 'rating', 'teams',
            'install_ts', 'update_ts'
        )


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'id', 'name', 'rating', 'players',
            'install_ts', 'update_ts'
        )
