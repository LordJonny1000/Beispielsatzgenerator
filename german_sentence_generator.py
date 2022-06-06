# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 23:39:18 2022

@author: jonny
"""
import random
from vocabulary.general import verbs, prepositions, nouns
from vocabulary.proper_names import persons
from vocabulary.semantic_classes import locations, events
from copy import deepcopy as cp
import part_of_speech
import linguistics
from probability_settings import probability
import utils

list_of_nouns = [part_of_speech.noun.from_list(x) for x in nouns.list_of_nouns]
list_of_verbs = [part_of_speech.verb.from_list(x) for x in verbs.list_of_verbs]
list_of_persons = [part_of_speech.proper_name.from_list(x) for x in persons.list_of_persons]
list_of_prepositions = [part_of_speech.preposition.from_list(x) for x in prepositions.list_of_prepositions]
list_of_events = [part_of_speech.noun.from_list(x) for x in events.list_of_events]
list_of_locations = [part_of_speech.noun.from_list(x) for x in locations.list_of_locations]

def generate_sentence():  
    
    #initialize
    detached_affix_if_required = ""
    subject_adjective = part_of_speech.adjective("")
    object1 = part_of_speech.noun("", "", "", "", "")
    object1_adjective = part_of_speech.adjective.from_string("")
    object2 = part_of_speech.noun("", "", "", "", "")
    event = part_of_speech.noun("", "", "", "", "")
    event_preposition = part_of_speech.preposition("", "", "", "")
    event_determinative = part_of_speech.article("", "", "")
    event_adjective = part_of_speech.adjective.from_string("")
    location = part_of_speech.noun("", "", "", "", "")
    location_preposition = part_of_speech.preposition("", "", "", "")
    location_determinative = part_of_speech.article("", "", "")
    location_adjective = part_of_speech.adjective.from_string("")

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
                random.choice(linguistics.numbers), random.choice(linguistics.genera), None), random.choice([x for x in list_of_nouns if x.ability_to_act])]))
    if predicate.valency == 0:
        subject = part_of_speech.proper_name("es", "neutral")
    subject.case = "nominative"
    subject_determinative = utils.generate_determinative(subject)
    predicate.person, predicate.number = subject.person, subject.number
    
    #generate subject adjective
    if probability("subject_adjective") and predicate.valency != 0 and type(subject) != part_of_speech.pronoun:
        if type(subject) == part_of_speech.proper_name:
            subject_determinative = part_of_speech.article("definite", "singular", subject.genus)
        subject.determinative = subject_determinative
        subject_adjective = utils.generate_adjective(subject)   

    #generate object1 if valency >= 2
    if predicate.valency >= 2:
        if predicate.θrolls[1] == "patient":
           object1 = cp(random.choice([random.choice(list_of_persons), random.choice(list_of_nouns), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
        elif predicate.θrolls[1] == "experiencer":
           object1 = cp(random.choice([random.choice(list_of_persons), random.choice([x for x in list_of_nouns if x.ability_to_act]), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
    object1.case = predicate.object_case
    object1_determinative = utils.generate_determinative(object1)
    if probability("object1_adjective"):
        if type(object1) == part_of_speech.proper_name:
            object1_determinative = part_of_speech.article("definite", "singular", object1.genus, object1.case)
        object1.determinative = object1_determinative
        object1_adjective = utils.generate_adjective(object1)
        
        
    #generate object2 if valency >= 3
    if predicate.valency >= 3:
        if predicate.θrolls[2] == "patient":
           object2 = cp(random.choice([random.choice(list_of_persons), random.choice(list_of_nouns), part_of_speech.pronoun("reflexive", "3rd", random.choice(linguistics.numbers), random.choice(linguistics.genera), "accusative")]))
        elif predicate.θrolls[2] == "experiencer":
           object2 = cp(random.choice([random.choice(list_of_persons), [x for x in list_of_nouns if x.ability_to_act][0], part_of_speech.pronoun("reflexive", "3rd", random.choice(linguistics.numbers), random.choice(linguistics.genera), predicate.object_case)]))
    object2.case = "accusative"
    object2_determinative = utils.generate_determinative(object2)

    #generate temporal_complement
    if probability("temporal_complement"):
        event_preposition = cp(random.choice([x for x in list_of_prepositions if "temporal" in (x.preposition_type)]))
        if "period" in event_preposition.movement_or_period:
            event = cp(random.choice([x for x in list_of_events if x.period]))
        else:
            event = cp(random.choice(list_of_events))
        event.case = "dative"
        event.number = "singular"
        event_determinative = utils.generate_determinative(event)
        event.determinative = event_determinative
        #generate event_adjective
        if probability("event_adjective"):
            event_adjective = utils.generate_adjective(event)

    #generate local_complement
    if probability("local_complement"):
        location_preposition = cp(random.choice([x for x in list_of_prepositions if "local" in (x.preposition_type) and predicate.movement in x.movement_or_period]))
        location = cp(random.choice(list_of_locations))
        location.case = location_preposition.case
        if predicate.movement == "stay":
            location.case = "dative"
        else:
            location.case = "accusative"
        location_determinative = utils.generate_determinative(location)
        location.determinative = location_determinative
        #generate location_adjective
        if probability("location_adjective"):
            location_adjective = utils.generate_adjective(location)
    
    #initialize sentence
    sentence_list = [subject_determinative, subject_adjective, subject, predicate, object1_determinative, object1_adjective, object1, \
                     object2_determinative, object2, event_preposition, event_determinative, event_adjective, event,  \
                         location_preposition, location_determinative, location_adjective, location, detached_affix_if_required]
    
    #adjust word order:
    if object2:
        if type(object2) == part_of_speech.pronoun:
            sentence_list.remove(object2)
            sentence_list.insert(sentence_list.index(object1_determinative), object2)
    
    #add interrogative clause
    if sentence_mode == "interrogative":
        sentence_list.remove(predicate), sentence_list.insert(0, predicate)
        #add innterogative words
        if random.randrange(2) < 1:
            interrogative_words = cp(linguistics.interrogative_words)
            if  predicate.valency < 2:
                interrogative_words.remove("was")
            interrogative_word = random.choice([x for x in interrogative_words])
            if interrogative_word == "wer":
              sentence_list.remove(subject_determinative), sentence_list.remove(subject_adjective), sentence_list.remove(subject)
              predicate.person, predicate.number = "3rd", "singular"
            if random.randrange(2) < 1:
              if interrogative_word == "was":
                  if predicate.object_case == "dative":
                      interrogative_word = "wem"
                  elif predicate.object_case == "accusative":
                      interrogative_word = "wen"
                  sentence_list.remove(object1_determinative), sentence_list.remove(object1_adjective), sentence_list.remove(object1)
            elif interrogative_word == "wo":
                sentence_list.remove(location_determinative), sentence_list.remove(location_adjective), sentence_list.remove(location)
            elif interrogative_word == "wann":
               sentence_list.remove(event_determinative), sentence_list.remove(event_adjective),  sentence_list.remove(event)
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
#while "am" not in x:
#   x = generate_sentence()
#print(x)

































        





        

