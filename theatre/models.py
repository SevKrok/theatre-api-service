import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from theatre_api_service import settings


class Actor(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    @property
    def full_name(self):
        return str(self)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name


def play_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/plays/", filename)


class Play(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="plays")
    actors = models.ManyToManyField(Actor, related_name="plays")
    image = models.ImageField(null=True, upload_to=play_image_file_path)

    def __str__(self) -> str:
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=64)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    show_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.play} {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )

    def __str__(self) -> str:
        return f"{self.user.email} {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance,
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True,
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ("row", "seat")

    @staticmethod
    def validate_seat(
        seat: int, row: int, max_seats: int, max_rows: int, error_to_raise
    ):
        if not (1 <= seat <= max_seats):
            raise ValidationError(
                {"seat": f"seat must be in range [1, {max_seats}], not {seat}"}
            )
        if not (1 <= row <= max_rows):
            raise error_to_raise(
                {"row": f"row must be in range [1, {max_rows}], not {row}"}
            )

    def clean(self):
        Ticket.validate_seat(
            self.seat,
            self.row,
            self.performance.theatre_hall.seats_in_row,
            self.performance.theatre_hall.rows,
            ValidationError,
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f"{self.performance} (row: {self.row},seat: {self.seat})"
