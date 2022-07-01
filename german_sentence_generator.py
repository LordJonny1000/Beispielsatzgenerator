# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 23:39:18 2022

@author: jonny
"""

import random
from copy import deepcopy as cp
import part_of_speech
import linguistics
import utils
from probability_settings import probability
import json



with open("vocabulary/general/nouns.json", encoding="utf8") as sf:
    sd = json.load(sf)
    list_of_nouns = list()
    for x in sd:
        list_of_nouns.append(part_of_speech.noun(x["word"], x["strong_or_weak"], x["genus"], x["semantic_class"], x["mass_noun"]))
with open("vocabulary/general/verbs.json", encoding="utf8") as sf:
    sd = json.load(sf)
    list_of_verbs = list()
    for x in sd:
        x["θrolls"] = x["θ\u200brolls"]
        del x["θ\u200brolls"]
        list_of_verbs.append(part_of_speech.verb(x["word"], x["strong_or_weak"], x["valency"], x["object_case"], x["θrolls"], x["movement"], x["additional_complement"], x["individual_preposition_infos"]))
with open("vocabulary/general/prepositions.json", encoding="utf8") as sf:
    sd = json.load(sf)
    list_of_prepositions = list()
    for x in sd:
        list_of_prepositions.append(part_of_speech.preposition(x["word"], x["preposition_type"], x["movement_modes"], x["case"]))

list_of_persons = [part_of_speech.proper_name(x[:-2], x[-1]) for x in open("vocabulary\proper_names\persons.txt", "r", encoding='utf-8').read().splitlines()]


def generate_sentence(): 
    
    #initialize tokens
    interrogative_word = subject = subject.adjective = predicate = object1 = object1.determinative = object1.adjective = object2 = object2.determinative = event = \
    event_preposition = event.determinative = event.adjective = location = location_preposition = location.determinative = location.adjective = individual_preposition = \
    individual_noun = individual_noun.determinative = individual_noun.adjective = detached_affix_if_required = part_of_speech.empty_token()
    
    #set sentence mode
    x = probability("interrogative_clause")
    sentence_mode = linguistics.sentence_modes[x]
    closing_punctuation_mark = linguistics.closing_punctuation_marks[x]
    del x
    
    #generate predicate
    predicate = cp(random.choice(list_of_verbs))
    for affix in linguistics.detached_affixes:
        if predicate.lemma[:len(affix)] == affix:
            detached_affix_if_required =  part_of_speech.proper_name(affix, "neutral")
            break

    #generate subject
    subject = cp(random.choice([random.choice(list_of_persons), part_of_speech.pronoun("personal", random.choice(linguistics.persons), \
                random.choice(linguistics.numbers), random.choice(linguistics.genera), None), random.choice([x for x in list_of_nouns if x.semantic_class in("person", "animal", "mythical creature")])]))
    subject.adjective = part_of_speech.empty_token()
    if predicate.valency == 0:
        subject = part_of_speech.proper_name("es", "neutral")
    subject.case = "nominative"
    if isinstance(subject, part_of_speech.noun):
        subject.determinative = random.choice([part_of_speech.article(random.choice(linguistics.article_types), subject.number, subject.genus, subject.case), part_of_speech.pronoun("possesive",\
                 random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), subject.case, subject.number, subject.genus)])
    
    
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
    else:
        if predicate.additional_complement and random.randrange(2) < 1:
            object2 = cp(random.choice([x for x in list_of_nouns if x.semantic_class not in("person", "animal", "mythical creature")]))
    object2.case = "accusative"
    object2.determinative = utils.generate_determinative(object2)

    #generate temporal complement
    if probability("temporal_complement"):
        event_preposition = cp(random.choice([x for x in list_of_prepositions if "temporal" in(x.preposition_type)]))
        event = cp(random.choice([x for x in list_of_nouns if x.semantic_class == "event"]))
        event.number = "singular"
        event.case = "dative"
        event.determinative = utils.generate_determinative(event)
        #generate event adjective
        if probability("event_adjective"):
            event.adjective = utils.generate_adjective(event)
    

    #generate local complement
    if probability("local_complement"):
        location_preposition = cp(random.choice([x for x in list_of_prepositions if "local" in (x.preposition_type) and predicate.movement in x.movement_modes]))
        location = cp(random.choice([x for x in list_of_nouns if x.semantic_class == "location"]))
        location.number, location.case, location.determinative = "singular", location_preposition.case, utils.generate_determinative(location)
        if predicate.movement == "stay":
            location.case = "dative"
        else:
            location.case = "accusative"
        location.determinative = utils.generate_determinative(location)
        #generate location adjective
        
        if probability("location_adjective"):
            location.adjective = utils.generate_adjective(location)
    
    #individual complement
    if predicate.individual_preposition_infos[0] != None and random.randrange(2) < 1:
        individual_preposition = [x for x in list_of_prepositions if predicate.individual_preposition_infos[0]][0]
        if predicate.individual_preposition_infos[1] == "anything":
            individual_noun = cp(random.choice([random.choice(list_of_persons), random.choice(list_of_nouns), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), individual_preposition.case[0])]))
        elif predicate.individual_preposition_infos[1] == "living_thing":
            individual_noun = cp(random.choice([random.choice(list_of_persons), random.choice([x for x in list_of_nouns if x.semantic_class in("person", "animal", "mythic creature")]), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), individual_preposition.case[0])]))
        elif predicate.individual_preposition_infos[1] == "person":
            individual_noun = cp(random.choice([random.choice(list_of_persons), random.choice([x for x in list_of_nouns if str(x.semantic_class) in("person")]), part_of_speech.pronoun("reflexive", random.choice(linguistics.persons), random.choice(linguistics.numbers), random.choice(linguistics.genera), individual_preposition.case[0])]))
        elif predicate.individual_preposition_infos[1] == "activity":
            individual_noun = cp(random.choice([x for x in list_of_verbs if x.θrolls[0] == "agent"]))
            individual_noun = part_of_speech.noun(individual_noun.word.capitalize(), "weak", "neutral", "activity")
            individual_noun.number = "singular"
            individual_noun.determinative.article_type = "indefinite"
        individual_noun.case = predicate.individual_preposition_infos[2]
        individual_noun.determinative = utils.generate_determinative(individual_noun)
        if random.randrange(4) > 2:
            individual_noun.adjective = utils.generate_adjective(individual_noun)
    
    #grouped complements
    local_complement = [location_preposition, location.determinative, location.adjective, location]
    individual_complement = [individual_preposition, individual_noun.determinative, individual_noun.adjective, individual_noun]
    temporal_complement = [event_preposition, event.determinative, event.adjective, event]
    
    #initialize sentence
    sentence_list = [subject.determinative, subject.adjective, subject, predicate, object1.determinative, object1.adjective, object1, object2.determinative, \
                    object2, event_preposition, event.determinative, event.adjective, event, location_preposition, location.determinative, location.adjective, location, \
                    individual_preposition, individual_noun.determinative, individual_noun.adjective, individual_noun, detached_affix_if_required]
        
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
            interrogative_word = random.choice(interrogative_words)
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
                sentence_list.remove(location_preposition), sentence_list.remove(location.determinative), sentence_list.remove(location.adjective), sentence_list.remove(location)
            elif interrogative_word == "wann":
               sentence_list.remove(event_preposition), sentence_list.remove(event.determinative), sentence_list.remove(event.adjective),  sentence_list.remove(event)
            interrogative_word = part_of_speech.proper_name(interrogative_word, None)
    sentence_list = [interrogative_word] + sentence_list
    
    features = {"interrogative_word":interrogative_word.word, "sentence_mode":sentence_mode, "subject.determinative.article_type":subject.determinative.article_type, "subject.adjective.word":subject.adjective.word,\
                "subject.word":subject.word, "subject.number":subject.number, "predicate.word":predicate.word, "object1.determinative.article_type":object1.determinative.article_type,\
                "object1.adjective.word":object1.adjective.word, "object1.word":object1.word, "object1.number":object1.number, \
                "object2.determinative.article_type":object2.determinative.article_type, \
                "object2.word":object2.word, "object2.number":object2.number, "event_preposition.word":event_preposition.word,\
                "event.determinative.article_type":event.determinative.article_type, "event.adjective.word":event.adjective.word, "event.word":event.word, \
                "location_preposition.word":location_preposition.word, "location.determinative.article_type":location.determinative.article_type, \
                "location.adjective.word":location.adjective.word, "location.word":location.word, "individual_preposition.word":individual_preposition.word,\
                "individual_noun.determinative.article_type":individual_noun.determinative.article_type, "individual_noun.adjective.word":individual_noun.adjective.word,\
                "individual_noun.word":individual_noun.word, "individual_noun.number":individual_noun.number}
    
    #surface transformation
    output = " ".join([utils.surface(x) for x in sentence_list if x.word and not isinstance(x, part_of_speech.empty_token)])
    
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
    output = output[0].upper() + output[1:] + closing_punctuation_mark
    


    return output, list(features.values())
    

        
#print(generate_sentence()[0])

for x in range(1000):
    generate_sentence()





#pseudo function for reproducing error
#x = generate_sentence()
#while "frech Einhörner" not in x[0]:
#   x = generate_sentence()
#print(x)
    

            


#subject.wordXpredicate.word, subject.wordXsubject_determinative.article_type, subject.wordXsubject_adjective.word
#predicate.wordXobject1.word, predicate.wordXobject1.number, predicate.wordXobject1_adjective.word, predicate.wordXobject1_determinative.article_type
#predicate.wordXobject2.word, predicate.wordXobject2.number, predicate.wordXobject2_adjective.word, predicate.wordXobject2_determinative.article_type
#event.wordXevent_preposition.word, event.wordXevent_adjective.word, predicate.wordXlocation.wordXlocation_preposition.word, location.wordXlocation_preposition.word,
#location.wordXlocation_adjective.word, individual_noun.wordXindividual_noun.determinative.article_type, individual_noun.wordXindividual_noun.adjective.word, 
#individual_noun.wordXindividual_noun.number





    











        





        

