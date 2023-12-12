from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from theatre.models import (
    Actor,
    Genre,
    Play,
    Performance,
    Ticket,
    TheatreHall,
    Reservation,
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class ActorDetailSerializer(serializers.ModelSerializer):
    plays = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "plays")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class GenreDetailSerializer(serializers.ModelSerializer):
    plays = plays = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = Genre
        fields = ("id", "name", "plays")


class PlaySerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors", "image")


class PlayListSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )
    performances = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="show_time",
    )

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "genres",
            "actors",
            "image",
            "performances",
        )


class PlayDetailSerializer(PlayListSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)


class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "image")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "reservation")


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlaySerializer(many=False)
    theatre_hall = TheatreHallSerializer(many=False)
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time", "tickets")

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError,
        )
        return data


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation
