from django.contrib.auth.models import User

from rest_framework import serializers

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template' : 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices= STYLE_CHOICES, default='friendly')
#
# Changed to ModelSerializer

# class SnippetSerializer(serializers.ModelSerializer):

# Change to HyperlinkedModelSerializer
class SnippetSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.username")
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['id', 'highlight', 'title', 'code', 'linenos', 'language', 'style', 'owner']

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


class StringRepresentation(serializers.Field):

    def to_representation(self, instance):
        if ( type(instance) is not str):
            return str(instance)
        return str(instance)

# class UserSerializer(serializers.ModelSerializer):

# Changed to use HyperlinkedModelSerializer
class UserSerializer(serializers.HyperlinkedModelSerializer):

    # NOTES:
    # variable name "snippets" MUST MATCH to the "related_name" defined in Snippet's model
    # If "related_name" is not set in Snippet's model, then default related name "snippet_set" is used

    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    id = StringRepresentation()

    # Nested relationships use below
    # snippets = SnippetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

