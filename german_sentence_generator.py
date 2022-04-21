# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 23:39:18 2022

@author: jonny
"""
import random
from vocabulary import nouns, verbs, adjectives, person_names, prepositions, locations
import part_of_speech
import linguistics
from utils import surface

def generate_sentence():   
    list_of_nouns = [part_of_speech.noun.from_list(x) for x in nouns.list_of_nouns]
    list_of_verbs = [part_of_speech.verb.from_list(x) for x in verbs.list_of_verbs]
    list_of_adjectives = [part_of_speech.adjective.from_string(x) for x in adjectives.list_of_adjectives]
    list_of_person_names = [part_of_speech.person_name.from_list(x) for x in person_names.list_of_person_names]
    list_of_prepositions = [part_of_speech.preposition.from_list(x) for x in prepositions.list_of_prepositions]
    list_of_locations = [part_of_speech.noun.from_list(x) for x in locations.list_of_locations]
    
    #generate predicate
    predicate = list_of_verbs[random.randrange(len(list_of_verbs))]
    detached_affix_if_required = ""
    for affix in linguistics.detached_affixes:
        if predicate.lemma[:len(affix)] == affix:
            detached_affix_if_required = affix
            break
    
    #generate subject
    subject = [list_of_person_names[random.randrange(len(list_of_person_names))], part_of_speech.pronoun("personal", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(2)], None), [x for x in list_of_nouns if x.ability_to_act][random.randrange(len([x for x in list_of_nouns if x.ability_to_act]))]][random.randrange(3)]
    subject_article_if_required = ""
    if predicate.valency == 0:
        subject = part_of_speech.person_name("Es", "neutral")
    if type(subject) == part_of_speech.noun:
        if subject.number == "singular":
            subject_article_if_required = part_of_speech.article(linguistics.article_types[random.randrange(2)], subject.number, subject.genus)
    
    #generate object1 if valency >= 2
    object1 = ""
    object1_article_if_required = ""
    if predicate.valency == 2:
        object1_article_if_required = ""
        if predicate.θrolls[1] == "patient":
           object1 = [list_of_person_names[random.randrange(len(list_of_person_names))], list_of_nouns[random.randrange(len(list_of_nouns))], part_of_speech.pronoun("reflexive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], predicate.object_case)][random.randrange(3)]
        elif predicate.θrolls[1] == "experiencer":
           object1 = [list_of_person_names[random.randrange(len(list_of_person_names))], [x for x in list_of_nouns if x.ability_to_act][0], part_of_speech.pronoun("reflexive", linguistics.persons[random.randrange(3)], linguistics.numbers[random.randrange(2)], linguistics.genera[random.randrange(3)], predicate.object_case)][random.randrange(3)]
        if type(object1) == part_of_speech.noun and object1.number == "singular":
                object1_article_if_required = part_of_speech.article(linguistics.article_types[random.randrange(2)], "singular", object1.genus, predicate.object_case)
                
    #generate prepositional_phrase
    preposition = [x for x in list_of_prepositions if predicate.movement in x.possible_movement_modes][random.randrange(len([x.word for x in list_of_prepositions if predicate.movement in x.possible_movement_modes]))]
    location = list_of_locations[random.randrange(len(list_of_locations))]
    location_article = part_of_speech.article("definite", "singular", location.genus, preposition.case[preposition.possible_movement_modes.index(predicate.movement)])
    #generate location_adjective
    location_adjective = list_of_adjectives[random.randrange(len(list_of_adjectives))].declension("definite", "singular", preposition.case[preposition.possible_movement_modes.index(predicate.movement)])
    prepositional_phrase = preposition.word + " " + location_article.word + location_adjective + " " + surface(location)
    
    


    
    
    #surface transformation
    output = surface(subject_article_if_required).capitalize() + surface(subject) + surface(predicate, subject) + surface(object1_article_if_required, predicate.object_case) + surface(object1, case=predicate.object_case) + prepositional_phrase + detached_affix_if_required
       
    
    #finish   
    if output[-1] == " ":
        output = output[:-1]
    output = output[0].upper() + output[1:] + "."
    return output

print(generate_sentence())












































"""
possible_subjects = list_of_nouns + list_of_person_names + [x for x in list_of_pronouns if x.pronoun_type == "personal"]
possible_agents = [x for x in list_of_nouns if x.ability_to_act]
possible_agents = possible_agents + list_of_names


surface_objectadjective = ""
surface_subjectadjective = ""
def generate_sentence():
    #create predicate
    sentpredicate = list_of_verbs[random.randrange(len(list_of_verbs))]
    
    #create subject
    
    if sentpredicate.valency == 0:
        sentsubject = expletivum
    elif  sentpredicate.valency > 0:
        if sentpredicate.θrolls[0] in("agent", "experiencer"):
            sentsubject = possible_agents[random.randrange(len(possible_agents))]
        else:
            sentsubject = possible_subjects[random.randrange(len(possible_subjects))]
    
    #create surface subject
    if type(sentsubject) is noun:
            chosen_article_type = article_types[random.randrange(2)]
            #create optional subjectadjective
            counter = random.randrange(2)
            if counter < 2:
                subjectadjective = list_of_adjectives[random.randrange(len(list_of_adjectives))]
                #create surface subjectadjective
                if chosen_article_type == "definite" and sentsubject.number == "plural":
                    surface_subjectadjective = subjectadjective.word + "en "
                else:
                    surface_subjectadjective = subjectadjective.word + "e "
            surface_sentsubject = article(chosen_article_type, sentsubject.number, sentsubject.genus, sentpredicate.object_case) + surface_subjectadjective + sentsubject.declension(sentsubject.number, sentpredicate.object_case)
    else:
        surface_sentsubject = sentsubject.declension(sentsubject.number ,"nominative")
    
    #create surface predicate
    surface_sentpredicate = sentpredicate.conjugation(sentsubject.person, sentsubject.number)
    
    #create object 
    if sentpredicate.valency == 2:
        if sentpredicate.θrolls[1] in("agent", "experiencer"):
            sentobject = possible_agents[random.randrange(len(possible_agents))]
        else:
            sentobject = possible_subjects[random.randrange(len(possible_subjects))]
        #create surface object
        if type(sentobject) is noun: 
            chosen_article_type = article_types[random.randrange(2)]
            #create optional objectadjective
            counter = random.randrange(2)
            if counter < 2:
                objectadjective = list_of_adjectives[random.randrange(len(list_of_adjectives))]
                #create surface objectadjective
                if chosen_article_type == "definite" and sentobject.number == "plural":
                    surface_objectadjective = objectadjective.word + "en "
                else:
                    surface_objectadjective = objectadjective.word + "e "
            surface_sentobject = article(chosen_article_type, sentobject.number, sentobject.genus, sentpredicate.object_case) + surface_objectadjective + sentobject.declension(sentobject.number, sentpredicate.object_case)
        elif type(sentobject) is person_name: 
            surface_sentobject = sentobject.declension(sentobject.number, sentpredicate.object_case)
        elif type(sentobject) is pronoun:
            surface_sentobject = sentobject.declension(sentobject.number, sentpredicate.object_case)
    else:
        surface_sentobject = ""
    #create optional prepositional phrase
    counter = random.randrange(2)
    if counter == 0:
        sentprepositional_phrase = [list_of_prepositions[random.randrange(len(list_of_prepositions))], list_of_places[random.randrange(len(list_of_places))]]
    else:
        surface_sentprepositional_phrase = ""
    #create surface prepositional phrase
    if counter == 0:
        surface_sentprepositional_phrase = sentprepositional_phrase[0].word + " " + article("definite", "singular", sentprepositional_phrase[1].genus, "dative") + sentprepositional_phrase[1].word + " "
    
        
    
    #create output
    output = surface_sentsubject + surface_sentpredicate + surface_sentobject + surface_sentprepositional_phrase
    
    #add detached affix
    for affix in detached_affixes:
        if sentpredicate.word[:len(affix)] == affix:
            output = output + affix
    output = output[0].upper() + output[1:]
    while output[-1] == " ":
        output = output[:-1]
    output = output + "."
    
    return output
"""









        





        

