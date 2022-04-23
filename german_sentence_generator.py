# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 23:39:18 2022

@author: jonny
"""
import random
from vocabulary.general import nouns, verbs, adjectives, prepositions
from vocabulary.proper_names import persons
from vocabulary.semantic_classes import locations
import part_of_speech
import linguistics
import probability_settings
from utils import surface

list_of_nouns = [part_of_speech.noun.from_list(x) for x in nouns.list_of_nouns]
list_of_verbs = [part_of_speech.verb.from_list(x) for x in verbs.list_of_verbs]
list_of_adjectives = [part_of_speech.adjective.from_string(x) for x in adjectives.list_of_adjectives]
list_of_persons = [part_of_speech.proper_name.from_list(x) for x in persons.list_of_persons]
list_of_prepositions = [part_of_speech.preposition.from_list(x) for x in prepositions.list_of_prepositions]
list_of_locations = [part_of_speech.noun.from_list(x) for x in locations.list_of_locations]

def generate_sentence():   
    #set sentence mode
    x = probability_settings.interrogative_clause()
    sentence_mode = linguistics.sentence_modes[x]
    closing_punctuation_mark = linguistics.closing_punctuation_marks[x]
    del x
    
    #generate predicate
    predicate = list_of_verbs[random.randrange(len(list_of_verbs))]
    detached_affix_if_required = ""
    for affix in linguistics.detached_affixes:
        if predicate.lemma[:len(affix)] == affix:
            detached_affix_if_required = affix
            break
    
    #generate subject
    subject = list_of_persons[random.randrange(len(list_of_persons))]
    subject = [x for x in list_of_nouns if x.ability_to_act][random.randrange(len([x for x in list_of_nouns if x.ability_to_act]))]
    subject_article_if_required = part_of_speech.article("indefinite", "plural", "neutral")

    if predicate.valency == 0:
        subject = part_of_speech.proper_name("es", "neutral")
    if type(subject) == part_of_speech.noun:
        if subject.number == "singular":
            subject_article_if_required = part_of_speech.article(linguistics.article_types[random.randrange(2)], subject.number, subject.genus)
  
    #generate subject adjective
    subject_adjective = ""
    if probability_settings.prepositional_phrase():
        if predicate.valency != 0:
            if type(subject) != part_of_speech.pronoun:
                subject_adjective = list_of_adjectives[random.randrange(len(list_of_adjectives))]
                if type(subject) == part_of_speech.proper_name:
                    subject_article_if_required = part_of_speech.article("definite", "singular", subject.genus)

    
    #generate object1 if valency >= 2
    object1 = ""
    object1_article_if_required = ""
    if predicate.valency == 2:
        object1_article_if_required = ""
        if predicate.θrolls[1] == "patient":
           object1 = [list_of_persons[random.randrange(len(list_of_persons))], list_of_nouns[random.randrange(len(list_of_nouns))], part_of_speech.pronoun("reflexive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], predicate.object_case)][random.randrange(3)]
        elif predicate.θrolls[1] == "experiencer":
           object1 = [list_of_persons[random.randrange(len(list_of_persons))], [x for x in list_of_nouns if x.ability_to_act][0], part_of_speech.pronoun("reflexive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], predicate.object_case)][random.randrange(3)]
        if type(object1) == part_of_speech.noun and object1.number == "singular":
                object1_article_if_required = part_of_speech.article(linguistics.article_types[random.randrange(2)], "singular", object1.genus, predicate.object_case)
                
    #generate prepositional_phrase
    prepositional_phrase = ""
    if probability_settings.prepositional_phrase():
        preposition = [x for x in list_of_prepositions if predicate.movement in x.possible_movement_modes][random.randrange(len([x.word for x in list_of_prepositions if predicate.movement in x.possible_movement_modes]))]
        location = list_of_locations[random.randrange(len(list_of_locations))]
        location_article = part_of_speech.article("definite", "singular", location.genus, preposition.case[preposition.possible_movement_modes.index(predicate.movement)])
        #generate location_adjective
        location_adjective = list_of_adjectives[random.randrange(len(list_of_adjectives))]
        prepositional_phrase = preposition.word + location_article.word + location_adjective.declension("definite", "singular", location.genus, preposition.case[preposition.possible_movement_modes.index(predicate.movement)]) + surface(location)
    
    


    #surface transformation
    if sentence_mode == "declarative":
        output = surface(subject_article_if_required) + surface(subject_adjective, None, subject_article_if_required.article_type, subject.number, subject.genus, "nominative") + surface(subject) + surface(predicate, subject) + surface(object1_article_if_required, predicate.object_case) + surface(object1, case=predicate.object_case) + prepositional_phrase + detached_affix_if_required
    elif sentence_mode == "interrogative":
        output = surface(predicate, subject) + surface(subject_article_if_required) + surface(subject_adjective, None, subject_article_if_required.article_type, subject.number, subject.genus, "nominative") + surface(subject) + surface(object1_article_if_required, predicate.object_case) + surface(object1, case=predicate.object_case) + prepositional_phrase + detached_affix_if_required

    
    #finish   
    if output[-1] == " ":
        output = output[:-1]
    output = output[0].upper() + output[1:] + closing_punctuation_mark
    return output
    #return part_of_speech.adjective.from_string("").declension("definite", "singular", "feminine")
print(generate_sentence())


















































        





        

