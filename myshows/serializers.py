from django.contrib.auth.models import User
from myshows.models import MovieDB,ShowDB,BookingDB
from rest_framework import serializers
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDB
        fields = "__all__"

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowDB
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDB
        fields = "__all__"
        read_only_fields = ["user","total_amount"]

    def validate(self,data):
        number_of_seats = data.get("number_of_seats")
        show = data.get("shows")

        if number_of_seats <= 0 :
            raise serializers.ValidationError("Enter a valid number of seats..!")
        
        if number_of_seats>show.available_seats:
            raise serializers.ValidationError("Not Enough Seats..!")


        if show.show_date < timezone.localdate():
            raise serializers.ValidationError("Enter a valid date..!")
        
        return data

    def create(self,validated_data):
        number_of_seats = validated_data.get("number_of_seats")
        show = validated_data.get("shows")
        total_amount = show.ticket_price * number_of_seats
        show.available_seats -= number_of_seats
        show.save()
        booking = BookingDB.objects.create(total_amount = total_amount,**validated_data)
        return booking
    