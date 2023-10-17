from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SerializersFile
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .models import File
from file_upload_api.sample_tasks import upload_file

class View(APIView):

    def get(self, request):
        files = File.objects.all()

        serializer = SerializersFile(files, many=True)
        return Response(serializer.data)




class Upload(APIView):
    serializer_class = SerializersFile
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            print(file)
            upload_file(file.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # return Response
# Create your views here.
