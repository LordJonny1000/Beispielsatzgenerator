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
    subject = [list_of_persons[random.randrange(len(list_of_persons))], part_of_speech.pronoun("personal", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(2)], None), [x for x in list_of_nouns if x.ability_to_act][random.randrange(len([x for x in list_of_nouns if x.ability_to_act]))]][random.randrange(3)]
    subject_determinative = part_of_speech.article("indefinite", "plural", "neutral")
    if predicate.valency == 0:
        subject = part_of_speech.proper_name("es", "neutral")
    if type(subject) == part_of_speech.noun:
        subject_determinative = [part_of_speech.article(linguistics.article_types[random.randrange(2)], subject.number, subject.genus), part_of_speech.pronoun("possesive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], "masculine", "nominative", "singular", "feminine")][0]#<--------!!!!! von 1 auf randrange(2) ändern

    #generate subject adjective
    subject_adjective = ""
    if probability_settings.prepositional_phrase():
        if predicate.valency != 0:
            if type(subject) != part_of_speech.pronoun:
                subject_adjective = list_of_adjectives[random.randrange(len(list_of_adjectives))]
                if type(subject) == part_of_speech.proper_name:
                    subject_determinative = part_of_speech.article("definite", "singular", subject.genus)

    
    #generate object1 if valency >= 2
    object1 = ""
    object1_determinative = ""
    if predicate.valency >= 2:
        object1_determinative = ""
        if predicate.θrolls[1] == "patient":
           object1 = [list_of_persons[random.randrange(len(list_of_persons))], list_of_nouns[random.randrange(len(list_of_nouns))], part_of_speech.pronoun("reflexive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], predicate.object_case)][random.randrange(3)]
        elif predicate.θrolls[1] == "experiencer":
           object1 = [list_of_persons[random.randrange(len(list_of_persons))], [x for x in list_of_nouns if x.ability_to_act][0], part_of_speech.pronoun("reflexive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], predicate.object_case)][random.randrange(3)]
        if type(object1) == part_of_speech.noun and object1.number == "singular":
                object1_determinative = part_of_speech.article(linguistics.article_types[random.randrange(2)], "singular", object1.genus, predicate.object_case)
                if probability_settings.possesive_pronoun_on_object1():
                    object1_determinative = part_of_speech.pronoun("possesive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], object1.genus, predicate.object_case, noun_number = object1.number, noun_genus = object1.genus)
     
    #generate object2 if valency >= 3
    object2 = ""
    object2_determinative = ""
    if predicate.valency >= 3:
        object2_determinative = ""
        if predicate.θrolls[2] == "patient":
           object2 = [list_of_persons[random.randrange(len(list_of_persons))], list_of_nouns[random.randrange(len(list_of_nouns))], part_of_speech.pronoun("reflexive", "3rd", linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], "accusative")][random.randrange(3)]
        elif predicate.θrolls[2] == "experiencer":
           object2 = [list_of_persons[random.randrange(len(list_of_persons))], [x for x in list_of_nouns if x.ability_to_act][0], part_of_speech.pronoun("reflexive", "3rd", linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], predicate.object_case)][random.randrange(3)]

        if type(object2) == part_of_speech.noun and object2.number == "singular":
                object2_determinative = part_of_speech.article(linguistics.article_types[random.randrange(2)], "singular", object2.genus, "accusative")




    #generate prepositional_phrase
    location = part_of_speech.noun("", "", "", "")
    preposition = part_of_speech.preposition("", "", "", "")
    location_article = ""
    location_adjective = part_of_speech.adjective.from_string("")
    if probability_settings.prepositional_phrase():
        preposition = [x for x in list_of_prepositions if predicate.movement in x.possible_movement_modes][random.randrange(len([x.word for x in list_of_prepositions if predicate.movement in x.possible_movement_modes]))]
        location = list_of_locations[random.randrange(len(list_of_locations))]
        location_article = part_of_speech.article("definite", "singular", location.genus, preposition.case[preposition.possible_movement_modes.index(predicate.movement)])
        #generate location_adjective
        if probability_settings.location_adjective():
            location_adjective = list_of_adjectives[random.randrange(len(list_of_adjectives))]


    
    #surface transformation
    if sentence_mode == "declarative":
        output = surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") + surface(subject) + surface(predicate, subject) + surface(object1_determinative, predicate.object_case) \
                 + surface(object1, case=predicate.object_case) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
                + surface(preposition) + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required#
        if object2:
            if type(object2) == part_of_speech.pronoun:
                output = surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") \
                    + surface(subject) + surface(predicate, subject) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
                    + surface(object1_determinative, predicate.object_case) + surface(object1, case=predicate.object_case) + surface(preposition)\
                    + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required
    elif sentence_mode == "interrogative":
        output = surface(predicate, subject) + surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") + surface(subject) + surface(object1_determinative, predicate.object_case) \
                 + surface(object1, case=predicate.object_case) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
                + surface(preposition) + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required#
        if object2:
            if type(object2) == part_of_speech.pronoun:
                output = surface(predicate, subject) + surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") \
                    + surface(subject) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
                    + surface(object1_determinative, predicate.object_case) + surface(object1, case=predicate.object_case) + surface(preposition)\
                    + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required
    
    #finish   
    if output[0] == " ":
        output = output[1:]        
    if output[-1] == " ":
        output = output[:-1]
    output = output[0].upper() + output[1:] + closing_punctuation_mark
    return output


print(generate_sentence())







































        





        

