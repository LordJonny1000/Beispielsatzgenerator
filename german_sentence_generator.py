# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 23:39:18 2022

@author: jonny
"""
import random
from vocabulary.general import verbs, adjectives, prepositions, nouns
from vocabulary.proper_names import persons
from vocabulary.semantic_classes import locations
from copy import deepcopy as cp
import part_of_speech
import linguistics
import probability_settings
import utils

def generate_sentence():  
    list_of_nouns = [part_of_speech.noun.from_list(x) for x in nouns.list_of_nouns]
    list_of_verbs = [part_of_speech.verb.from_list(x) for x in verbs.list_of_verbs]
    list_of_adjectives = [part_of_speech.adjective.from_string(x) for x in adjectives.list_of_adjectives]
    list_of_persons = [part_of_speech.proper_name.from_list(x) for x in persons.list_of_persons]
    list_of_prepositions = [part_of_speech.preposition.from_list(x) for x in prepositions.list_of_prepositions]
    list_of_locations = [part_of_speech.noun.from_list(x) for x in locations.list_of_locations]    

    #set sentence mode
    x = probability_settings.interrogative_clause()
    sentence_mode = linguistics.sentence_modes[x]
    closing_punctuation_mark = linguistics.closing_punctuation_marks[x]
    del x
    
    #generate predicate
    #predicate = cp(random.choice(list_of_verbs))
    predicate = cp(random.choice(list_of_verbs))
    detached_affix_if_required = ""
    for affix in linguistics.detached_affixes:
        if predicate.lemma[:len(affix)] == affix:
            detached_affix_if_required = affix
            break
    
    #generate subject
    if predicate.valency == 0:
        subject = part_of_speech.proper_name("es", "neutral")
    subject = cp(random.choice([random.choice(list_of_persons), part_of_speech.pronoun("personal", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), None), random.choice([x for x in list_of_nouns if x.ability_to_act])]))
    if predicate.valency == 0:
        subject = part_of_speech.proper_name("es", "neutral")
    subject.case = "nominative"
    subject_determinative = utils.generate_determinative(subject)
        
    #generate subject adjective
    subject_adjective = part_of_speech.adjective("")
    if probability_settings.subject_adjective():
        if predicate.valency != 0:
            if type(subject) != part_of_speech.pronoun:
                subject_adjective = cp(random.choice(list_of_adjectives))
                if type(subject) == part_of_speech.proper_name:
                    subject_determinative = part_of_speech.article("definite", "singular", subject.genus)
    
    #generate object1 if valency >= 2
    object1 = part_of_speech.noun("", None, None, None, None)
    if predicate.valency >= 2:
        if predicate.θrolls[1] == "patient":
           object1 = cp(random.choice([random.choice(list_of_persons), random.choice(list_of_nouns), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
        elif predicate.θrolls[1] == "experiencer":
           object1 = cp(random.choice([random.choice(list_of_persons), random.choice([x for x in list_of_nouns if x.ability_to_act]), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
    object1.case = predicate.object_case
    object1_determinative = utils.generate_determinative(object1)
            
     
    #generate object2 if valency >= 3
    object2 = part_of_speech.noun("", None, None, None, None)
    if predicate.valency >= 3:
        if predicate.θrolls[2] == "patient":
           object2 = cp(random.choice([random.choice(list_of_persons), random.choice(list_of_nouns), part_of_speech.pronoun("reflexive", "3rd", random.choice(linguistics.numbers), random.choice(linguistics.genera), "accusative")]))
        elif predicate.θrolls[2] == "experiencer":
           object2 = cp(random.choice([random.choice(list_of_persons), [x for x in list_of_nouns if x.ability_to_act][0], part_of_speech.pronoun("reflexive", "3rd", random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
    object2.case = "accusative"
    object2_determinative = utils.generate_determinative(object2)


    #generate prepositional_phrase
    location = part_of_speech.noun("", None, None, None, None)
    preposition = part_of_speech.preposition("", "", "", "")
    location_article = part_of_speech.article(None, None, None)
    location_adjective = part_of_speech.adjective.from_string("")
    if probability_settings.prepositional_phrase():
        preposition = cp(random.choice([x for x in list_of_prepositions if predicate.movement in x.possible_movement_modes]))
        location = cp(random.choice(list_of_locations))
        location_article = part_of_speech.article("definite", "singular", location.genus, preposition.case[preposition.possible_movement_modes.index(predicate.movement)])
        #generate location_adjective
        if probability_settings.location_adjective():
            location_adjective = cp(random.choice(list_of_adjectives))

    #assign syntactic relations
    subject_determinative.noun_number = subject.number
    subject_adjective.article_type, subject_adjective.number, subject_adjective.genus = subject_determinative.article_type, subject.number, subject.genus
    subject_adjective.case = "nominative"
    predicate.person, predicate.number = subject.person, subject.number
    object1_determinative.case = predicate.object_case
    location_adjective.article_type, location_adjective.number, location_adjective.genus = location_article.article_type, "singular", location.genus
    if predicate.movement == "stay":
        location_adjective.case = "dative"
    elif predicate.movement == "move":
        location_adjective.case = "accusative" 

    #initialize sentence
    sentence_list = [subject_determinative, subject_adjective, subject, predicate, object1_determinative, object1, \
                     object2_determinative, object2, preposition, location_article, location_adjective, location, detached_affix_if_required]
    
    #adjust word order:
    if object2:
        if type(object2) == part_of_speech.pronoun:
            sentence_list.remove(object2)
            sentence_list.insert(sentence_list.index(object1_determinative), object2)
    
    if sentence_mode == "interrogative":
        sentence_list.remove(predicate)
        sentence_list.insert(0, predicate)
    
    #surface transformation
    output = " ".join([utils.surface(x) for x in sentence_list if len(utils.surface(x)) > 0])
    
    #finish          
    while output[-1] == " ":
        output = output[:-1]
    output = output[0].upper() + output[1:] + closing_punctuation_mark
    
    return output



print(generate_sentence())




#pseudo function for reproducing error
#x = generate_sentence()
#while "nn" not in x:
#   x = generate_sentence()
#print(x)


    






































        





        

