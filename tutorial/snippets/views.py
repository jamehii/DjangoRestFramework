from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.parsers import JSONParser
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

# use mixin to simplify the views
from rest_framework import mixins
from rest_framework import generics


from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer

# Create your views here.

# To simplify our view code further, we can use this view (notes: not mixins anymore):
#   generics.ListCreateAPIView
# We don't even need to define function like: get, post anymore
# Super nice !!


# class SnippetList(APIView):
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):

class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new snippet.
    """

    # mixin must remember to put like this
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return JsonResponse(serializer.data, safe=False)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

        # serializer = SnippetSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         # data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return JsonResponse(serializer.data, status=201)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return JsonResponse(serializer.errors, status=400)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# To simplify our view code further, we can use this view (notes: not mixins anymore):
#   generics.RetrieveUpdateDestroyAPIView
# We don't even need to define function like: get, put, delete
# Super nice !!

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    # must add in for mixin class
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # def get_object(self, pk):

        # try:
        #     return Snippet.objects.get(pk=pk)
        # except Snippet.DoesNotExist :
        #     raise Http404 

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

        # snippet = self.get_object(pk)
        # serializer = SnippetSerializer(snippet)
        # return Response(serializer.data)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

        # snippet = self.get_object(pk)
        # serializer = SnippetSerializer(snippet, data=request.data)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

        # snippet = self.get_object(pk)
        # snippet.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)


# @csrf_exempt
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None) :

#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         # return HttpResponse(status=404)
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         # return JsonResponse(serializer.data)
#         return Response(serializer.data)


#     elif request.method == 'PUT':
#         # data = JSONParser().parse(request)

#         serializer = SnippetSerializer(snippet, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             # return JsonResponse(serializer.data)
#             return Response(serializer.data)
        
#         # return JsonResponse(serializer.errors, status=400)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         # return HttpResponse(status=204)
#         return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer