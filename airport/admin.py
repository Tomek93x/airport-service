from django.contrib import admin

from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket
)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "closest_big_city")
    search_fields = ("name", "closest_big_city")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance")
    list_filter = ("source", "destination")


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "airplane_type",
        "rows",
        "seats_in_row",
        "capacity"
    )
    list_filter = ("airplane_type",)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "airplane",
        "departure_time",
        "arrival_time"
    )
    list_filter = ("departure_time", "airplane")
    inlines = [TicketInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user")
    list_filter = ("created_at",)
    inlines = [TicketInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("flight", "row", "seat", "order")
    list_filter = ("flight",)
