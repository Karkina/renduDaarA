from django.shortcuts import render

import requests
import json
import os
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import Http404, HttpResponse
from gutenberg_api.models import BookIndexModel, BookModel, GraphJaccard
from gutenberg_api.serializers import BookIndexModelSerializer, BookModelSerializer, GraphJaccardSerializer
from gutenberg_api.configs import myApi_utl
import re


#
class RedirectionBooks(APIView):
    def get(self, request, format=None):
        books = BookModel.objects.all()
        jsondata = BookModelSerializer(books, many=True)
        return handleResponse(status="OK", result=jsondata.data, message="Voici la liste des books", codeStatus=200)

#
class RedirectionDetailBook(APIView):
    def get_object(self, id):
        try:
            return BookModel.objects.get(id=id)
        except BookModel.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        book = self.get_object(id)
        print(request.REQUEST["data"])
        jsondata = BookModelSerializer(book)
        return handleResponse(status="OK", result=jsondata.data, message="Voici le livre", codeStatus=200)

# Recherche livre par mot simple
class RedirectionSimpleSearchBook(APIView):
    def get_object(self, word):
        try:
            return BookIndexModel.objects.filter(word=word)
        except BookIndexModel.DoesNotExist:
            raise Http404

    def get(self, request, word, format=None):


        '''egrepString = os.popen("./egrep \"%s\" tmpWords.txt" % word).read()
        listWords = list(filter(None, re.split(', |\n|\]|\[', egrepString)))'''
        '''p = subprocess.Popen("./egrep \"%s\" tmpWords.txt" % word, stdout=subprocess.PIPE)
        (output, err) = p.communicate()'''

        jar_path = 'egrep.jar'

        # Use subprocess to execute the egrep jar file
        process = subprocess.Popen(['java', '-jar', jar_path, word, 'tmpWords.txt'], stdout=subprocess.PIPE)
        output, error = process.communicate()

        # Convert the output to a string and split it into a list of words
        stringOutput = output.decode('utf-8')
        listWords = list(filter(None, re.split(', |\n|\]|\[', stringOutput)))

        booksIndexModel = []
        indexIdBooks = []
        for w in listWords:
            books = self.get_object(w.lower())
            for book in books:
                print(book.id)
                if (book.idBook not in indexIdBooks):
                    indexIdBooks.append(book.idBook)
                    booksIndexModel.append(book)
        
        booksModel = []
        indexNeighboors = []
        for indexBook in booksIndexModel:
            booksModel += BookModel.objects.filter(id=indexBook.idBook)
            indexNeighboors += GraphJaccard.objects.filter(bookSrc=indexBook.idBook)

        neighboors = []
        for neighboor in indexNeighboors:
            neighboors = BookModel.objects.filter(id=neighboor.bookDes)

        suggestions = [ s for s in neighboors if s not in booksModel ]

       
        jsondataBook = BookModelSerializer(booksModel, many=True)
        jsondataSuggestions = BookModelSerializer(suggestions, many=True)
        return handleResponse(
            status="OK",
            result={ "books": jsondataBook.data, "suggestions":jsondataSuggestions.data},
            message="Voici le livre",
            codeStatus=200
        )


# -------------------------------------------------------------------------------------- #
def handleResponse(status, result, message, codeStatus):
    response_data = {}
    response_data['status'] = status
    response_data['message'] = message
    response_data['result'] = result

    return HttpResponse(json.dumps(response_data), content_type="application/json", status=codeStatus)
