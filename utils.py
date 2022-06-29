import numpy as np
import random
import linguistics
import part_of_speech
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

def list_to_dict(thelist):
    word_to_id = dict()
    for n, i in enumerate(thelist):
        word_to_id[i] = n
    return word_to_id
    
def generate_determinative(noun):
    if noun.word == "EMPTY":
        return part_of_speech.proper_name('EMPTY', "neutral")
    existing_dets = [part_of_speech.article("definite", noun.number, noun.genus, noun.case), part_of_speech.article("indefinite", noun.number, noun.genus, noun.case),\
                     part_of_speech.pronoun("possesive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera),\
                     noun.case, noun.number, noun.genus)]
    if noun.mass_noun:
        existing_dets.append(part_of_speech.proper_name('EMPTY', "neutral"))
    if type(noun) == part_of_speech.noun:
        return random.choice(existing_dets)
    else:
        return part_of_speech.proper_name('EMPTY', "")

def generate_adjective(target):
    if target.word == "EMPTY":
        return part_of_speech.adjective("EMPTY")
    if type(target) == part_of_speech.proper_name:
        target.determinative = part_of_speech.article("definite", "singular", target.genus, target.case)
    det = target.determinative
    adjective = part_of_speech.adjective("EMPTY")
    if target.word == "" or type(target) == part_of_speech.pronoun:
        return adjective
    adjective = cp(random.choice([part_of_speech.adjective(x) for x in open("vocabulary\general\\adjectives.txt", "r", encoding='utf-8').read().splitlines()]))
    adjective.genus, adjective.case, adjective.number, adjective.article_type = target.genus, target.case, target.number, det.article_type
    return adjective



