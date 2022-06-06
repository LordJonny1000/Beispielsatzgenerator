from copy import deepcopy as cp
import random
import linguistics
import part_of_speech
from vocabulary.general import adjectives



adjectives = [part_of_speech.adjective.from_string(x) for x in adjectives.list_of_adjectives]

def surface(instance):
    if type(instance) in(part_of_speech.noun, part_of_speech.adjective):
        output = instance.declension()
    elif type(instance) in([part_of_speech.verb]):
        output = instance.conjugation()
    elif type(instance) in(part_of_speech.article, part_of_speech.pronoun, part_of_speech.proper_name, part_of_speech.preposition):
        output = instance.word
    elif type(instance) == str:
        return instance
    return output

def generate_determinative(noun):
    det = part_of_speech.article(None, None, None)
    if noun.word == "":
        return det
    if type(noun) == part_of_speech.noun:
        det = cp(random.choice([part_of_speech.article(random.choice(linguistics.article_types), noun.number, noun.genus, noun.case), \
                                part_of_speech.pronoun("possesive", random.choice(linguistics.persons), random.choice(linguistics.numbers), \
                                random.choice(linguistics.genera), noun.case, noun.number, noun.genus)]))
        if noun.mass_noun:
            return part_of_speech.article("indefinite", "plural", noun.genus)
    if type(det) == part_of_speech.article:
        if det.number == "plural" and det.article_type == "indefinite":
            det = part_of_speech.article("indefinite", "plural", noun.genus)
    return det

def generate_adjective(target):
    det = target.determinative
    adjective = part_of_speech.adjective("")
    if target.word == "" or type(target) == part_of_speech.pronoun:
        return adjective
    adjective = cp(random.choice(adjectives))
    adjective.genus, adjective.case, adjective.number, adjective.article_type = target.genus, target.case, target.number, det.article_type
    return adjective

        

    


