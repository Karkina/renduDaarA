from rest_framework.serializers import ModelSerializer
from gutenberg_api.models import BookIndexModel, BookModel, GraphJaccard

class BookModelSerializer(ModelSerializer):
    class Meta:
        model = BookModel
        fields = ('id', 'author', 'language', 'title' , 'coverBook', 'text', 'crank')

class BookIndexModelSerializer(ModelSerializer):
    class Meta:
        model = BookIndexModel
        fields = ('id', 'word', 'occurence', 'idBook')

class GraphJaccardSerializer(ModelSerializer):
    class Meta:
        model = GraphJaccard
        fields = ('id', 'bookSrc', 'bookDes')