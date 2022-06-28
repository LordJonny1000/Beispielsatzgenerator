import numpy as np
import random
import linguistics
import part_of_speech
import compatibility_matrices as MX
from copy import deepcopy as cp
from vocabulary.general import nouns, verbs, prepositions


def surface(instance):

    if type(instance) in([part_of_speech.noun, part_of_speech.adjective]):
        output = instance.declension()
    elif type(instance) in([part_of_speech.verb]):
        output = instance.conjugation()
    elif type(instance) in(part_of_speech.article, part_of_speech.pronoun, part_of_speech.proper_name, part_of_speech.preposition):
        output = instance.word
    elif type(instance) == str:
        return instance
    return output
    
def string_to_object(string):#works for open classes only
    all_words_as_objects = [part_of_speech.noun.from_list(x) for x in nouns.as_list] + [part_of_speech.verb.from_list(x) for x in verbs.as_list] + [part_of_speech.adjective(x) for x in open("vocabulary\general\\adjectives.txt", "r", encoding='utf-8').read().splitlines()]\
        + [part_of_speech.preposition.from_list(x) for x in prepositions.as_list] \
           + [part_of_speech.noun.from_list(x) for x in nouns.as_list if x[3] == "location"] + [part_of_speech.noun.from_list(x) for x in nouns.as_list if x[3] == "event"]
    matches = [x for x in all_words_as_objects if x.word == string]
    if len(matches) == 0:
        print("Wort >" + string + "< nicht gefunden")
        print(string)
    elif len(matches) > 1:
        print("es wurde mehr als ein Eintrag für >" + string + "< gefunden")
    else:
        return matches[0]

def list_to_dict(l):
    counter = 0
    word_to_id = dict()
    for x in l:
        word_to_id[x] = counter
        counter += 1
    return word_to_id

def create_compabiliy_matrix(l1, l2):
    if type(l1[0]) != str:
        l1 = [x.word for x in l1]
    if type(l2[0]) != str:
        l2 = [x.word for x in l2]
    counter = 0
    word_to_id1, word_to_id2 = dict(), dict()
    for x in l1:
        word_to_id1[x] = counter
        counter += 1
    counter = 0
    for x in l2:
        word_to_id2[x] = counter
        counter += 1
    matrix = np.zeros((len(l2), len(l1)))
    counter = 0
    for x in l2:
        for y in l1:
            decision = ""
            while len(str(decision)) != 1:
                decision = int(input(x + " " + y + " "))
            matrix[counter][word_to_id1[y]] = decision
        counter += 1
    return matrix

def update_compatibility_matrix(rows_list, cols_list, matrix):
    if type(rows_list[0]) != str:
        rows_list = [x.word for x in rows_list]
    if type(cols_list[0]) != str:
        cols_list = [x.word for x in cols_list]
    if np.shape(matrix)[0] < len(rows_list):
        for r in rows_list[-(len(rows_list)-np.shape(matrix)[1]):]:
            thelist = []
            for c in cols_list:
                decision = ""
                while len(str(decision)) != 1:
                    decision = input(c + " " + r + " ")
                thelist.append(int(decision))
            matrix = np.hstack((matrix, np.array([thelist]).T))
    elif np.shape(matrix)[1] < len(cols_list):
        for c in cols_list[-(len(cols_list)-np.shape(matrix)[1]):]:
            thelist = []
            for r in rows_list:
                decision = ""
                while len(str(decision)) != 1:
                    decision = input(r + " " + c + " ")
                thelist.append(int(decision))
            matrix = np.hstack((matrix, np.array([thelist]).T))
    else:
        print("List is already up to date.")
        
    return matrix

    
def generate_determinative(noun):
    if noun.word == "EMPTY":
        return part_of_speech.proper_name('EMPTY', "neutral")
    det = part_of_speech.article(None, None, None)
    existing_dets = [part_of_speech.article("definite", noun.number, noun.genus, noun.case), part_of_speech.article("indefinite", noun.number, noun.genus, noun.case),\
                     part_of_speech.pronoun("possesive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera),\
                    noun.case, noun.number, noun.genus)]
    possible_dets = []
    if noun.word == "":
        return det
    if noun.mass_noun:
        possible_dets.append(det)
    if type(noun) == part_of_speech.noun and noun.semantic_class not in("location", "event"):
        det = random.choice(existing_dets)
    elif noun.semantic_class == "location":
        for x in range(len(existing_dets)):
            if MX.location_or_event_to_article_type[x][list_to_dict([x[0] for x in nouns.as_list if x[3] in("location", "event")])[noun.word]]:
                possible_dets.append(existing_dets[x])
        det = random.choice(possible_dets)
    elif noun.semantic_class == "event":
        for x in range(len(existing_dets)):
            if MX.location_or_event_to_article_type[x][list_to_dict([x[0] for x in nouns.as_list if x[3] in("location", "event")])[noun.word]]:
                possible_dets.append(existing_dets[x])
        det = random.choice(possible_dets)
    return det

def generate_adjective(target):
    if target.word == "EMPTY":
        return part_of_speech.proper_name('EMPTY', "neutral")
    if type(target) == part_of_speech.proper_name:
        target.determinative = part_of_speech.article("definite", "singular", target.genus, target.case)
    det = target.determinative
    adjective = part_of_speech.adjective("")
    if target.word == "" or type(target) == part_of_speech.pronoun:
        return adjective
    adjective = cp(random.choice([part_of_speech.adjective(x) for x in open("vocabulary\general\\adjectives.txt", "r", encoding='utf-8').read().splitlines()]))
    adjective.genus, adjective.case, adjective.number, adjective.article_type = target.genus, target.case, target.number, det.article_type
    return adjective



