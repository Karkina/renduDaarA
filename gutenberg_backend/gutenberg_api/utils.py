from collections import Counter
import re
import io
from stop_words import safe_get_stop_words


def getWordsWithOcc(texte, langue):
    # Mots de grammaire ...
    stop_words = safe_get_stop_words(langue)
    # Transformer le texte en miniscule
    txt = texte.lower()
    # Trouver les mots du texte
    mots = re.findall('[a-zA-Z\u00C0-\u00FF]*', txt)
    # Éliminer les espaces et les éléments courts
    lst = [x for x in mots if x != '' and len(x) > 2 and not x in stop_words]
    # Créer un dict contenant les mots et la fréquence des mots
    motsOcc = Counter(lst)

    return motsOcc


def getListIndexBook(wordsOcc, idBook):
    liste = []
    for word, occ in wordsOcc.items():
        liste.append({
            "word": word,
            "occurence": occ,
            "idBook": idBook,
        })
    return liste


def saveTmpWords(wordsOcc):
    stream = io.open("tmpWords.txt", 'a+')
    for word, occ in wordsOcc.items():
        stream.write(word + ",\n")
    stream.close()

# d1, d2: liste mots -> occ


def distance_jaccard(d1, d2):
    a = 0
    b = 0
    liste_word_d2 = list(d2)
    for key, value in d1.items():
        if key in d2:
            m = max(value, d2[key])
            a += m - min(value, d2[key])
            b += m
            liste_word_d2.remove(key)
        # mot present seulement dans d1
        else:
            a += value
            b += value
    # les mots qui sont seulement dans d2
    for mot in liste_word_d2:
        a += d2[mot]
        b += d2[mot]
    try:
        return a/b
    except:
        return 1


#
def calcule_graphe_jaccard(map_book_wordOcc, seuil):
    graph = []
    total_distance = {}
    nextIndice = 1
    liste_book_wordOcc = list(map_book_wordOcc)
    for book, wordOcc in map_book_wordOcc.items():
        for j in range(nextIndice, len(map_book_wordOcc)):
            dist = distance_jaccard(
                wordOcc, map_book_wordOcc[liste_book_wordOcc[j]])

            # Création des arêtes du graph
            if (dist > seuil):
                graph.append({
                    "bookSrc": book,
                    "bookDes": liste_book_wordOcc[j]
                })
                graph.append({
                    "bookSrc": liste_book_wordOcc[j],
                    "bookDes": book
                })
            total_distance[book] = (
                total_distance[book]+dist) if (book in total_distance.keys()) else dist
            total_distance[liste_book_wordOcc[j]] = (total_distance[liste_book_wordOcc[j]]+dist) if (
                liste_book_wordOcc[j] in total_distance.keys()) else dist

        nextIndice += 1
    return (graph, total_distance)
