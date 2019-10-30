from django.shortcuts import render

# Create your views here.
from .models import Music
from .serializers import MusicSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response

class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    # permission_classes = (IsAuthenticated,)           # needs username and password to use API

    # def create(self, request, **kwargs):
    #     song = request.data.get('song')
    #     singer = request.data.get('singer')
    #     new_music = Music.objects.create(song=song, singer=singer)
    #     serializer = MusicSerializer(new_music)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)