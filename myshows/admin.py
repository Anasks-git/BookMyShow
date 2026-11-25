from django.contrib import admin
from myshows.models import MovieDB,ShowDB,BookingDB
# Register your models here.

admin.site.register(MovieDB)
admin.site.register(ShowDB)
admin.site.register(BookingDB)