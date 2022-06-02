from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializers,PythonCodeSerializer
from django.contrib.auth.models import User
from myUser.models import pythonCode

API_KEY = '12345'

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint' : '/api/users/',
            'method' : 'GET/POST'
        },
        {
            'Endpoint' : '/api/codes/',
            'method' : 'GET/POST'
        },
    ]
    return Response(routes)

@api_view(['GET','POST'])
def getUsers(request):
    if request.method == 'GET':
        return Response("Make POST method request with API_KEY")
    elif request.method == 'POST':
        if request.data.get('API_KEY',None) == None:
            return Response("API_KEY NOT FOUND")
        if request.data.get('API_KEY') != API_KEY:
            return Response("Wrong API_KEY")
        serializer = UserSerializers(User.objects.all(),many=True)
        return Response(serializer.data)



@api_view(['GET','POST'])
def getPythonCode(request):
    if request.method == 'GET':
        return Response("Make POST method request with API_KEY")
    elif request.method == 'POST':
        if request.data.get('API_KEY',None) == None:
            return Response("API_KEY NOT FOUND")
        if request.data.get('API_KEY') != API_KEY:
            return Response("Wrong API_KEY")
        serializer = PythonCodeSerializer(pythonCode.objects.all(),many=True)
        return Response(serializer.data)

