from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

from django.contrib.auth.models import User

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template' : 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices= STYLE_CHOICES, default='friendly')
#
# Changed to ModelSerializer

class SnippetSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']

    # We need to override this special method in order to pass in "current user object" to serializer,
    # so that serializer can have "current user object" passed in to create "Snippet object"

    # This is the detailed explanation:
    # Since "Snippet" has a member "owner", this "owner" member is ForeignKey to User
    # Now, whenever an "instance of Snippet" is created by serializer, serializer needs to pass "Snippet" the "current user object" as well
    # so that Snippet "owner" member can be linked to "current user object"

    def perform_create(self, serializer):

        # Notes: The variable name "owner" MUST BE THE SAME NAME defined in "Snipped Model"
        serializer.save(owner=self.request.user)



    # With "ModelSerializer", both create & update are auto-implemented 

    # def create(self, validated_data):
    #     """
    #     Update and return a new 'Snippet' instance, given the validated data
    #     """

    #     return Snippet.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing 'Snippet' instance, given the validated data
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.value)
    #     instance.save()

    #     return instance


class UserSerializer(serializers.ModelSerializer):

    # NOTES:
    # variable name "snippets" MUST MATCH to the "related_name" defined in Snippet's model
    # If "related_name" is not set in Snippet's model, then default related name "snippet_set" is used

    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']