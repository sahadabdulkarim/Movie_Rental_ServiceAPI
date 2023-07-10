from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework.validators import UniqueValidator
from datetime import date
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Movie.objects.all(), message="Title must be unique."
            ),
            MinLengthValidator(
                10,
                message="Title should have a minimum length of 2 characters after the prefix. 'Movie - '",
            ),
            MaxLengthValidator(
                108,
                message="Title should have a Maximum length of 100 characters after the prefix. 'Movie - '",
            ),
        ],
        error_messages={
            "blank": "Title field is required.",
        },
    )
    release_date = serializers.DateField(
        error_messages={
            "blank": "Release date field is required.",
            "invalid": "Invalid release date format.",
        }
    )
    genre = serializers.ChoiceField(
        choices=["Action", "Drama", "Comedy", "Thriller", "Sci-Fi"],
        error_messages={
            "required": "Genre is required.",
            "invalid_choice": "Invalid genre. Choose from Action, Drama, Comedy, Thriller, or Sci-Fi.",
        },
    )
    duration_minutes = serializers.IntegerField(
        min_value=1,
        max_value=600,
        error_messages={
            "required": "Duration is required.",
            "min_value": "Duration must be at least 1 minute.",
            "max_value": "Duration must be at most 600 minutes.",
        },
    )
    rating = serializers.FloatField(min_value=0.0, max_value=10.0, required=False)

    def validate_duration_minutes(self, value):
        if value < 1:
            raise serializers.ValidationError("Duration must be at least 1 minute.")
        if value > 600:
            raise serializers.ValidationError(
                "Duration must be at most 600 minutes (10 hours)."
            )
        return value

    def validate_title(self, value):
        prefix = "Movie - "
        if not value.startswith(prefix):
            raise serializers.ValidationError("Title must start with 'Movie - '")
        return value

    def validate_release_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Release date cannot be in the future.")
        max_release_date = date.today().replace(year=date.today().year - 30)
        if value < max_release_date:
            raise serializers.ValidationError(
                "Release date cannot be more than 30 years ago."
            )
        return value

    def validate_rating(self, value):
        if value is not None and (value < 0.0 or value > 10.0):
            raise serializers.ValidationError("Rating must be between 0.0 and 10.0.")
        return value

    class Meta:
        model = Movie
        fields = "__all__"
