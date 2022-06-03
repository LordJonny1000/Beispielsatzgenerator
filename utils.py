from copy import deepcopy as cp
import random
import linguistics
import part_of_speech

def surface(instance):
    if type(instance) == part_of_speech.noun:
        output = instance.declension()
    if type(instance) == part_of_speech.adjective:
        output = instance.declension()
    elif type(instance) == part_of_speech.verb:
        output = instance.conjugation()
    elif type(instance) == part_of_speech.article:
        output = instance.word
    elif type(instance) == part_of_speech.pronoun:
        output = instance.word
    elif type(instance) == part_of_speech.proper_name:
        output = instance.word
    elif type(instance) == part_of_speech.preposition:
        output = instance.word
    elif type(instance) == str:
        return instance
    return output


def generate_determinative(noun, definite_article_only = False):
    det = part_of_speech.article(None, None, None)
    if noun.word == "":
        return det
    if type(noun) == part_of_speech.noun:
        det = cp(random.choice([part_of_speech.article(random.choice(linguistics.article_types), noun.number, noun.genus, noun.case), part_of_speech.pronoun("possesive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), noun.case, noun.number, noun.genus)]))
        if noun.mass_noun:
            return part_of_speech.article(None, None, None)
    if type(det) == part_of_speech.article:
        if det.number == "plural" and det.article_type == "indefinite":
            det = part_of_speech.article(None, None, None)
    return det
        

    


