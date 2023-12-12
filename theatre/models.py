from django.db import models

from theatre_api_service import settings


class Actor(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="plays")
    actors = models.ManyToManyField(Actor, related_name="plays")

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.performance} (row: {self.row},seat: {self.seat})"
