from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MovieDB(models.Model):
    movie_name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    language = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self):
        return self.movie_name

class ShowDB(models.Model):
    movie = models.ForeignKey(MovieDB,on_delete=models.CASCADE,related_name="Shows")
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=10,decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.movie_name} - {self.show_date}"

class BookingDB(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings")
    shows = models.ForeignKey(ShowDB,on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    booking_status = models.CharField(max_length=100,default="Pending")

    def __str__(self):
        return f"{self.user} - {self.shows}"