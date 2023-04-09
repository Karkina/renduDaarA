from django.core.management.base import BaseCommand
from gutenberg_api.models import BookIndexModel, BookModel, GraphJaccard
from gutenberg_api.serializers import BookIndexModelSerializer, BookModelSerializer, GraphJaccardSerializer
from gutenberg_api.configs import api_url, nb_page
import requests
import time
from stop_words import get_stop_words
from gutenberg_api.utils import calcule_graphe_jaccard, getListIndexBook, getWordsWithOcc, saveTmpWords
import os


THRESHOLD_DISTANCE = 0.4 

class Command(BaseCommand):
    help = 'Refresh the list of index books'

    def handle(self, *args, **kwargs):
        self.stdout.write('['+time.ctime()+'] Refreshing data...')
        # delete oldest books
        BookModel.objects.all().delete()
        BookIndexModel.objects.all().delete()
        GraphJaccard.objects.all().delete()
        os.system("rm tmpWords.txt")

        map_book_wordOcc = {}

        for i in range(1, nb_page):
            response = requests.get(
                api_url+'/books?mime_type=text&'+'page=' + str(i))
            jsondata = response.json()
            data = jsondata['results']

            for livre in data:
                try:
                    url_text = livre['formats']["text/plain; charset=utf-8"]
                    url_text = url_text.replace(".zip", ".txt")
                except:
                    continue
                serializer = BookModelSerializer(data={
                    "id": livre['id'],
                    "author": ('None' if len(livre['authors']) == 0 else livre['authors'][0]['name']),
                    "language": livre['languages'][0],
                    "title": livre['title'],
                    "coverBook": livre['formats']['image/jpeg'],
                    "text": url_text
                }
                )
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS(
                        '['+time.ctime()+'] Successfully added book id="%s" ' % livre['id']))

                    text_response = (livre['title']) + " ".join(livre['subjects'])
                    wordsOcc = getWordsWithOcc(
                        text_response, livre['languages'][0])

                    # 
                    saveTmpWords(wordsOcc)

                    dataIndex = getListIndexBook(wordsOcc, livre['id'])
                    # print(dataIndex)
                    serializerIndex = BookIndexModelSerializer(
                        data=dataIndex, many=True)
                    if serializerIndex.is_valid():
                        map_book_wordOcc[(livre['id'])] = wordsOcc
                        serializerIndex.save()

                    self.stdout.write(self.style.SUCCESS('['+time.ctime()+'] Successfully added index book id="%s" ' % livre['id']))

        self.stdout.write('['+time.ctime()+'] Refreshing Jaccard Graph ...')
        (jaccardGraph, totalDistance) = calcule_graphe_jaccard(map_book_wordOcc, THRESHOLD_DISTANCE)
        serializerGraphJaccard = GraphJaccardSerializer(data=jaccardGraph, many=True)
        if serializerGraphJaccard.is_valid():
            serializerGraphJaccard.save()
        self.stdout.write(self.style.SUCCESS('['+time.ctime()+'] Successfully calculate Jaccard Graph '))
        
        self.stdout.write('['+time.ctime()+'] Refreshing crank (closeness centrality ) of books ...')
        #add score to db
        for idBook in totalDistance:
            score = (len(totalDistance)-1) / totalDistance[idBook]
            book = BookModel.objects.get(id=idBook)
            book.crank=score
            book.save()
            self.stdout.write(self.style.SUCCESS(
                        '['+time.ctime()+'] Successfully added book crank to bookId="%s" ' % book.id))

        self.stdout.write('['+time.ctime()+'] Data refresh terminated.')
