from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

# use mixin to simplify the views
from rest_framework import mixins
from rest_framework import generics

# permissions
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly


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

@api_view(['GET',])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new snippet.
    """

    # mixin must remember to put like this
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    # authenticated requests get read-write access
    # unauthenticated requests get read-only access.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # We need to override this special method in order to pass in "current user object" to serializer,
    # so that serializer can have "current user object" passed in to create "Snippet object"

    # This is the detailed explanation:
    # Since "Snippet" has a member "owner", this "owner" member is ForeignKey to User
    # Now, whenever an "instance of Snippet" is created by serializer, serializer needs to pass "Snippet" the "current user object" as well
    # so that Snippet "owner" member can be linked to "current user object"

    def perform_create(self, serializer):

        # Notes: The variable name "owner" MUST BE THE SAME NAME defined in "Snipped Model"
        serializer.save(owner=self.request.user)

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    # lookup_field = 'pk'             # This is the field on the "target" should be used for lookup
    # lookup_url_kwarg = 'primarykey' # This corresponds to the name used in urls param <int:primarykey>

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

        # NOTES: StaticHTMLRenederer will actually render the "Response" in HTML form
        # If you return a "HTML" format, then it will be rendered accordingly

        # return Response(
        #     "<!DOCTYPE html> \
        #     <html> \
        #         <head> \
        #             <title>Static page</title> \
        #         </head> \
        #         <body> \
        #             <h1>This static page is rendered by StaticHTMLRenderer</h1> \
        #             <p>This is nice !!</p> \
        #         </body> \
        #     </html>"
        # )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer