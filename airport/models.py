import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def airplane_image_file_path(instance, filename):
    """Generate file path for airplane image"""
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/airplanes/", filename)


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_from"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_to"
    )
    distance = models.IntegerField()

    class Meta:
        ordering = ["source"]

    def __str__(self):
        return f"{self.source} - {self.destination}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name_plural = "crews"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=airplane_image_file_path
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return (
            f"{self.route.source} - {self.route.destination} "
            f"({self.departure_time})"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self):
        return (
            f"Flight {self.flight} (row: {self.row}, seat: {self.seat})"
        )

    def clean(self):
        if self.row > self.flight.airplane.rows:
            raise ValidationError(
                f"Row number must be in range: "
                f"(1, {self.flight.airplane.rows})"
            )
        if self.seat > self.flight.airplane.seats_in_row:
            raise ValidationError(
                f"Seat number must be in range: "
                f"(1, {self.flight.airplane.seats_in_row})"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
