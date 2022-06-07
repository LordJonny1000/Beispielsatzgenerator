# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 23:39:18 2022

@author: jonny
"""
import random
import numpy as np
from vocabulary.general import verbs, prepositions, nouns
from vocabulary.proper_names import persons
from vocabulary.semantic_classes import locations, events
from copy import deepcopy as cp
import part_of_speech
import linguistics
import utils
from probability_settings import probability
import compatibility_matrices as MX

list_of_nouns = [part_of_speech.noun.from_list(x) for x in nouns.list_of_nouns]
list_of_verbs = [part_of_speech.verb.from_list(x) for x in verbs.list_of_verbs]
list_of_persons = [part_of_speech.proper_name.from_list(x) for x in persons.list_of_persons]
list_of_prepositions = [part_of_speech.preposition.from_list(x) for x in prepositions.list_of_prepositions]
list_of_events = [part_of_speech.noun.from_list(x) for x in events.list_of_events]
list_of_locations = [part_of_speech.noun.from_list(x) for x in locations.list_of_locations]
for x in list_of_events:
    x.semantic_class = "event"
for x in list_of_locations:
    x.semantic_class = "location"



def generate_sentence():  
    
    #initialize optional tokens
    detached_affix_if_required = ""
    object1 = part_of_speech.noun("", "", "", "")
    object2 = part_of_speech.noun("", "", "", "")
    event = part_of_speech.noun("", "", "", "")
    event_preposition = part_of_speech.preposition("", "", "", "")
    event.determinative = part_of_speech.article("", "", "")
    location = part_of_speech.noun("", "", "", "")
    location_preposition = part_of_speech.preposition("", "", "", "")
    location.determinative = part_of_speech.article("", "", "")
    
    #set sentence mode
    x = probability("interrogative_clause")
    sentence_mode = linguistics.sentence_modes[x]
    closing_punctuation_mark = linguistics.closing_punctuation_marks[x]
    del x
    
    #generate predicate
    predicate = cp(random.choice(list_of_verbs))
    for affix in linguistics.detached_affixes:
        if predicate.lemma[:len(affix)] == affix:
            detached_affix_if_required = affix
            break

    #generate subject
    subject = cp(random.choice([random.choice(list_of_persons), part_of_speech.pronoun("personal", random.choice(linguistics.persons), \
                random.choice(linguistics.numbers), random.choice(linguistics.genera), None), random.choice([x for x in list_of_nouns if x.semantic_class in("person", "animal", "mythical creature")])]))
    if predicate.valency == 0:
        subject = part_of_speech.proper_name("es", "neutral")
    subject.case = "nominative"
    subject.determinative = utils.generate_determinative(subject)
    predicate.person, predicate.number = subject.person, subject.number
    
    #generate subject adjective
    if probability("subject_adjective") and predicate.valency != 0 and type(subject) != part_of_speech.pronoun:
        subject.adjective = utils.generate_adjective(subject) 

    #generate object1 if valency >= 2
    if predicate.valency >= 2:
        if predicate.θrolls[1] == "patient":
           object1 = cp(random.choice([random.choice(list_of_persons), random.choice(list_of_nouns), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
        elif predicate.θrolls[1] == "experiencer":
           object1 = cp(random.choice([random.choice(list_of_persons), random.choice([x for x in list_of_nouns if x.semantic_class in("person", "animal", "mythical creature")]), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
    object1.case = predicate.object_case
    object1.determinative = utils.generate_determinative(object1)
    if probability("object1_adjective"):  
        object1.adjective = utils.generate_adjective(object1)
        
        
    #generate object2 if valency >= 3
    if predicate.valency >= 3:
        if predicate.θrolls[2] == "patient":
           object2 = cp(random.choice([random.choice(list_of_persons), random.choice(list_of_nouns), part_of_speech.pronoun("reflexive", "3rd", random.choice(linguistics.numbers), random.choice(linguistics.genera), "accusative")]))
        elif predicate.θrolls[2] == "experiencer":
           object2 = cp(random.choice([random.choice(list_of_persons), [x for x in list_of_nouns  if x.semantic_class in("person", "animal", "mythical creature")], part_of_speech.pronoun("reflexive", "3rd", random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
    object2.case = "accusative"
    object2.determinative = utils.generate_determinative(object2)

    #generate temporal complement
    if probability("temporal_complement"):
        event_preposition = cp(random.choice([x for x in list_of_prepositions if "temporal" in (x.preposition_type)]))
        possible_events_vec = MX.event_to_temporal_preposition[utils.word_to_id([x.word for x in list_of_prepositions if "temporal" in x.preposition_type])[event_preposition.word]][:]
        possible_events = []
        counter = 0
        for e in list_of_events:
            if possible_events_vec[counter]:
                possible_events.append(e)
            counter += 1
        event = random.choice(possible_events)
        event.number = "singular"
        event.case = "dative"
        event.determinative = utils.generate_determinative(event)
        #generate event adjective
        if probability("event_adjective"):
            event.adjective = utils.generate_adjective(event)

    #generate local complement
    if probability("local_complement"):
        location_preposition = cp(random.choice([x for x in list_of_prepositions if "local" in (x.preposition_type) and predicate.movement in x.movement_modes]))
        possible_locations = []
        possible_locations_vec = MX.location_to_local_preposition[utils.word_to_id([x.word for x in list_of_prepositions if "local" in x.preposition_type])[location_preposition.word]]
        counter = 0
        for l in list_of_locations:
            if possible_locations_vec[counter]:
                possible_locations.append(l)
            counter += 1
        location = random.choice(possible_locations)
        location.number = "singular"
        location.case = location_preposition.case
        location.determinative = utils.generate_determinative(location)
        if predicate.movement == "stay":
            location.case = "dative"
        else:
            location.case = "accusative"
        location.determinative = utils.generate_determinative(location)
        #generate location adjective
        if probability("location_adjective"):
            location.adjective = utils.generate_adjective(location)

    #initialize sentence
    sentence_list = [subject.determinative, subject.adjective, subject, predicate, object1.determinative, object1.adjective, object1, \
                     object2.determinative, object2, event_preposition, event.determinative, event.adjective, event,  \
                         location_preposition, location.determinative, location.adjective, location, detached_affix_if_required]
    
    #adjust word order:
    if object2:
        if type(object2) == part_of_speech.pronoun:
            sentence_list.remove(object2)
            sentence_list.insert(sentence_list.index(object1.determinative), object2)
            
    #add interrogative clause and interrogative word
    if sentence_mode == "interrogative":
        sentence_list.remove(predicate), sentence_list.insert(0, predicate)
        #add interrogative words
        if random.randrange(2) < 1:
            interrogative_words = cp(linguistics.interrogative_words)
            if  predicate.valency < 2:
                interrogative_words.remove("was")
            interrogative_word = random.choice([x for x in interrogative_words])
            if interrogative_word == "wer":
              sentence_list.remove(subject.determinative), sentence_list.remove(subject.adjective), sentence_list.remove(subject)
              predicate.person, predicate.number = "3rd", "singular"
            if random.randrange(2) < 1:
              if interrogative_word == "was":
                  if predicate.object_case == "dative":
                      interrogative_word = "wem"
                  elif predicate.object_case == "accusative":
                      interrogative_word = "wen"
                  sentence_list.remove(object1.determinative), sentence_list.remove(object1.adjective), sentence_list.remove(object1)
            elif interrogative_word == "wo":
                sentence_list.remove(location.determinative), sentence_list.remove(location.adjective), sentence_list.remove(location)
            elif interrogative_word == "wann":
               sentence_list.remove(event.determinative), sentence_list.remove(event.adjective),  sentence_list.remove(event)
            sentence_list = [interrogative_word] + sentence_list
            
    #surface transformation
    output = " ".join([utils.surface(x) for x in sentence_list if len(utils.surface(x)) > 0])
    
    #contraction               
    counter = 0
    occuring_contraction_words = []
    for x in linguistics.contraction_words:
        if " " + x + " " in output:
            for y in range(output.count(" " + x + " ")):
                occuring_contraction_words.append(x)
            counter += output.count(" " + x + " ")
    contracnum = random.randrange(counter + 1)
    for x in range(contracnum):
        thechoice = random.choice(occuring_contraction_words)
        occuring_contraction_words.remove(thechoice)
        output = output.replace(" " + thechoice + " ", " " + linguistics.contraction_words[thechoice] + " ")
    del contracnum, counter, occuring_contraction_words             
    
    #finish          
    while output[-1] in(" ", ","):
        output = output[:-1]
    output = output[0].upper() + output[1:] + closing_punctuation_mark
    
    return output

print(generate_sentence())




#pseudo function for reproducing error
#x = generate_sentence()
#while "Verspielt!!" not in x[0]:
#   x = generate_sentence()
#print(x)


#print(MX.noun_to_article_type[-1][:])
#print(len(MX.noun_to_article_type[-1][:]))



























        





        

