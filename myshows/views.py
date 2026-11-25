from django.shortcuts import render,get_object_or_404
from myshows.models import MovieDB,ShowDB,BookingDB
from django.contrib.auth.models import User
from myshows.serializers import UserSerializer,MovieSerializer,ShowSerializer,BookingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authentication import BasicAuthentication

# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializer(data = form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message":"User Created Successfully",
                            "User Details":serializer_instance.data})
        else:
            return Response({"message" : "Failed"},status=400)

    def get(self,request):
        qs = User.objects.all()
        serializer_instance = UserSerializer(qs,many = True)
        return Response(data=serializer_instance.data)


class MovieListView(APIView):

    authentication_classes = [BasicAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        else:
            return [AllowAny()]
    def get(self,request):
        qs = MovieDB.objects.all()
        serializer_instance = MovieSerializer(qs,many = True)
        return Response(data = serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = MovieSerializer(data = form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message" : "Movie data Added!",
                             "data" : serializer_instance.data})
        else:
            return Response(data=serializer_instance.errors)


class ShowListView(APIView):
    authentication_classes = [BasicAuthentication]
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        else:
            return [AllowAny()]
        
    def get(self,request):
        qs = ShowDB.objects.all()
        serializer_instance = ShowSerializer(qs,many = True)
        return Response(data = serializer_instance.data)

    def post(self,request):
            form_data = request.data
            serializer_instance = ShowSerializer(data = form_data)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response({"message" : "Show data Added!"})
            else:
                return Response(data=serializer_instance.errors)
    

class BookingListCreateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        qs = BookingDB.objects.filter(user = request.user)
        serializer_instance = BookingSerializer(qs,many = True)
        return Response(data = serializer_instance.data)
    
    def post(self,request):
        form_data = request.data
        serializer_instance = BookingSerializer(data = form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(user = request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class BookingRetrieveUpdateDeleteView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        qs = BookingDB.objects.get(user = request.user,id = pk)
        serializer_instance = BookingSerializer(qs)
        return Response(data=serializer_instance.data)
    def delete(self,request,pk):
        qs = BookingDB.objects.get(user = request.user,id = pk)
        qs.shows.available_seats += qs.number_of_seats
        qs.shows.save()
        qs.delete()
        return Response({"message":"Deletion Successfull..!"})
