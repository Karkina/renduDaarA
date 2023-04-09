from django.db import models

# Book Model.
class BookModel(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    author = models.CharField(max_length=150, default="None")
    language = models.CharField(max_length=5, default="")
    title = models.CharField(max_length=255, blank=False)
    coverBook = models.CharField(max_length=355,default="")
    text = models.TextField(default="")
    crank = models.FloatField(default="0.0")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'id'], name='unique')
        ]
        ordering = ['title', 'language']


# Index Book Model.
class BookIndexModel(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=150, default="")
    occurence = models.CharField(max_length=5, default="")
    idBook = models.CharField(max_length=100, blank=False)

    class Meta:
        ordering = ['word', 'idBook']

# Graph de Jaccard
class GraphJaccard(models.Model):
    id = models.AutoField(null=False, primary_key=True)
    bookSrc = models.IntegerField(default='-1')
    bookDes = models.IntegerField(default='-1')
    class Meta:
        ordering =('bookSrc','bookDes')