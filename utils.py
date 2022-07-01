
import random
import linguistics
import part_of_speech
from copy import deepcopy as cp



def surface(instance):

    if type(instance) in([part_of_speech.noun, part_of_speech.adjective]):
        output = instance.declension()
    elif type(instance) in([part_of_speech.verb]):
        output = instance.conjugation()
    elif type(instance) in(part_of_speech.article, part_of_speech.pronoun, part_of_speech.proper_name, part_of_speech.preposition,  part_of_speech.empty_token):
        output = instance.word

    elif type(instance) == str:
        return instance
    return output
    
def list_to_dict(thelist):
    word_to_id = dict()
    for n, i in enumerate(thelist):
        word_to_id[i] = n
    return word_to_id
    
def generate_determinative(noun):
    if isinstance(noun, part_of_speech.noun):
        dets = [part_of_speech.article(random.choice(linguistics.article_types), noun.number, noun.genus, noun.case), part_of_speech.pronoun("possesive",\
                 random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), noun.case, noun.number, noun.genus)]
        
        if noun.mass_noun:
            dets.append(part_of_speech.empty_token())
    elif isinstance(noun, part_of_speech.proper_name) and noun.word != "EMPTY":
        dets = [part_of_speech.article("definite", noun.number, noun.genus, noun.case)]
    
    else:
        dets = [part_of_speech.empty_token()]
    output = random.choice(dets)
    return output


def generate_adjective(target):
    if target.word in("EMPTY", "es", "Es"):
        return part_of_speech.empty_token()
    if type(target) == part_of_speech.proper_name:
        target.determinative = part_of_speech.article("definite", "singular", target.genus, target.case)
    det = target.determinative
    adjective = part_of_speech.adjective("EMPTY")
    if target.word == "" or type(target) == part_of_speech.pronoun:
        return adjective
    adjective = cp(random.choice([part_of_speech.adjective(x) for x in open("vocabulary\general\\adjectives.txt", "r", encoding='utf-8').read().splitlines()]))
    adjective.genus, adjective.case, adjective.number, adjective.article_type = target.genus, target.case, target.number, det.article_type
    return adjective


import json
with open("vocabulary/general/nouns.json", encoding="utf8") as sf:
    sd = json.load(sf)
    list_of_nouns = list()
    for x in sd:
        list_of_nouns.append(part_of_speech.noun(x["word"], x["strong_or_weak"], x["genus"], x["semantic_class"], x["mass_noun"]))
noun = random.choice(list_of_nouns)
noun.number = random.choice(linguistics.numbers)
