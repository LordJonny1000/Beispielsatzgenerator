# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 23:39:18 2022

@author: jonny
"""
import random


vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
conjugation_exceptions = ["laufen", "saufen", "stehlen", "sehen", "zusehen" , "lesen", "empfehlen", "geschehen", "befehlen", "wissen"]
persons = ["1st", "2nd", "3rd"]
genera = ["masculine", "feminine", "neutral"]
numbers = ["singular", "plural"]
article_types = ["definite", "indefinite"]
detached_affixes = ["zu", "aus", "ab", "ein", "nach"]
list_of_preposition_types = ["local"]

def encoding(data):
    data = data.replace("Ã¶", "ö")
    data = data.replace("Ã¤", "ä")
    data = data.replace("Ã¼", "ü")
    data = data.replace("ÃŸ", "ß")
    data = data.replace("Ã³", "ó")
    data = data.replace("Ã“", "Ô")
    data = data.replace("Ãº", "ú")
    data = data.replace("Ã©", "é")
    data = data.replace("Ãœ", "Ü")
    data = data.replace("Ã„", "Ä")
    data = data.replace("Ã¢", "â")
    data = data.replace("Ã–", "Ö")
    data = data.replace("Ã¡", "á")
    data = data.replace("Ã»", "á")
    data = data.replace("Ã­", "í")
    data = data.replace("Ã«", "ë")
    return data

    
class adjective:
    def __init__(self, word):
        self.word = word
    def declension(self, number, article_type, case="nominative",):
        output = self.word + "e"
        if case=="nominative" and number =="singular" :
            output = output
            if article_type == "indefinite":
                output = output + "r"
        else:
            output = output + "n"
    
source = open("list_of_adjectives.txt", "r")
source = source.readlines()
counter = 0
list_of_adjectives = []
while counter < len(source):
    file = "item = " + source[counter]
    exec(file)  
    counter = counter + 1 
    list_of_adjectives.append(item)
for x in list_of_adjectives:
    x.word = encoding(x.word)
        
    

source = open("list_of_verbs.txt", "r")
source = source.readlines()
counter = 0
list_of_verbs = []
while counter < len(source):
    file = "item = " + source[counter]
    exec(file)  
    counter = counter + 1 
    list_of_verbs.append(item)
list_of_verbs = [x[0] for x in list_of_verbs]
for x in list_of_verbs:
    x.word = encoding(x.word)



class person_name:

    def __init__(self, word, genus):
        self.word = word
        self.genus = genus
        self.person = "3rd"
        self.number = "singular"
    def declension(self, number, case="nominative"):
        return self.word + " "


source = open("list_of_names.txt", "r")
source = source.readlines()
counter = 0
list_of_names = []
while counter < len(source):
    file = "item = " + source[counter]
    exec(file)  
    counter = counter + 1 
    list_of_names.append(item)
list_of_names = [x[0] for x in list_of_names]
for x in list_of_names:
    x.word = encoding(x.word)
expletivum = person_name("es", "neutral")#self, word, strong_or_weak, genus, ability_to_act)

class pronoun:
    def __init__(self, word, pronoun_type, person, number, genus, case):
        self.word = word
        self.pronoun_type = pronoun_type
        self.person = person
        self.number = number
        self.genus = genus
        self.case = case 
    def declension(self, number, case="nominative"):
        if case != "naminative":
            for x in list_of_pronouns:
                if x.person == self.person and x.number == self.number and x.genus in(self.genus, "general") and x.case == case:
                    return x.word + " "
        else:
            return self.word + " "
        
    
list_of_pronouns = [pronoun("ich", "personal", "1st", "singular", "general", 0),
                    pronoun("du", "personal", "2nd", "singular", "general", 0),
                    pronoun("er", "personal", "3rd", "singular","masculine", 0), 
                    pronoun("sie", "personal","3rd", "singular", "feminine", 0), 
                    pronoun("es", "personal", "3rd", "singular", "neutral", 0), 
                    pronoun("wir", "personal", "1st", "plural", "general", 0), 
                    pronoun("ihr", "personal", "2nd", "plural", "general", 0), 
                    pronoun("sie", "personal", "3rd", "plural", "general", 0), 
                    pronoun("mein", "possesive", "1st", "singular","general", 0), 
                    pronoun("dein", "possesive", "2nd", "singular", "general", 0), 
                    pronoun("sein", "possesive", "3rd", "singular", "masculine", 0),
                    pronoun("sein", "possesive", "3rd", "singular", "neutral", 0),
                    pronoun("ihr", "possesive", "3rd", "singular", "feminine", 0),
                    pronoun("unser", "possesive", "1st", "plural", "general", 0), 
                    pronoun("euer", "possesive", "2nd", "plural", "general", 0),
                    pronoun("ihr", "possesive", "3nd", "plural", "general", 0),
                    pronoun("mir", "reflexive", "1st", "singular", "general", "dative"),
                    pronoun("dir", "reflexive", "2nd", "singular", "general", "dative"),
                    pronoun("ihm", "reflexive", "3rd", "singular", "masculine", "dative"),
                    pronoun("ihm", "reflexive", "3rd", "singular", "neutral", "dative"),
                    pronoun("ihr", "reflexive", "3rd", "singular", "feminine", "dative"),
                    pronoun("uns", "reflexive", "1st", "plural", "general", "dative"),
                    pronoun("euch", "reflexive", "2nd", "plural", "general", "dative"),
                    pronoun("ihnen", "reflexive", "3rd", "plural", "general", "dative"),
                    pronoun("mich", "reflexive", "1st", "singular", "general", "accusative"),
                    pronoun("dich", "reflexive", "2nd", "singular", "general", "accusative"),
                    pronoun("ihn", "reflexive", "3rd", "singular", "masculine", "accusative"),
                    pronoun("sie", "reflexive", "3rd", "singular", "feminine", "accusative"),
                    pronoun("es", "reflexive", "3rd", "singular", "neutral", "accusative"),
                    pronoun("uns", "reflexive", "1st", "plural", "general", "accusative"),
                    pronoun("euch", "reflexive", "2nd", "plural", "general", "accusative"),
                    pronoun("sie", "reflexive", "3rd", "plural", "general", "accusative")]


possible_subjects = list_of_nouns + list_of_names + [x for x in list_of_pronouns if x.pronoun_type == "personal"]
possible_agents = [x for x in list_of_nouns if x.ability_to_act]
possible_agents = possible_agents + list_of_names


def article(article_type, number, genus, case="nominative"):
    if case == "nominative" or case == 0:
        if article_type == "definite":
            if number == "singular":
                if genus == "masculine":
                    output = "der "
                elif genus == "feminine":
                    output = "die "
                elif genus == "neutral":
                    output = "das "
            elif number == "plural":
                output = "die "
        elif article_type == "indefinite":
            if number == "singular":
                if genus == "masculine":
                    output = "ein "
                elif genus == "feminine":
                    output = "eine "
                elif genus == "neutral":
                    output = "ein "
            if number == "plural":
                output = ""
    elif case == "genitive":
        if article_type == "definite":
            if number == "singular":
                if genus == "masculine":
                    output = "des "
                elif genus == "feminine":
                    output = "der "
                elif genus == "neutral":
                    output = "des "
            elif number == "plural":
                output = "der "
        elif article_type == "indefinite":
            if number == "singular":
                if genus == "masculine":
                    output = "eines "
                elif genus == "feminine":
                    output = "einer "
                elif genus == "neutral":
                    output = "eines "
            if number == "plural":
                output = ""
    elif case == "dative":
        if article_type == "definite":
            if number == "singular":
                if genus == "masculine":
                    output = "dem "
                elif genus == "feminine":
                    output = "der "
                elif genus == "neutral":
                    output = "dem "
            elif number == "plural":
                output = "den "
        elif article_type == "indefinite":
            if number == "singular":
                if genus == "masculine":
                    output = "einem "
                elif genus == "feminine":
                    output = "einer "
                elif genus == "neutral":
                    output = "einem "
            if number == "plural":
                output = ""
    elif case == "accusative":
        if article_type == "definite":
            if number == "singular":
                if genus == "masculine":
                    output = "den "
                elif genus == "feminine":
                    output = "die "
                elif genus == "neutral":
                    output = "das "
            elif number == "plural":
                output = "die "
        elif article_type == "indefinite":
            if number == "singular":
                if genus == "masculine":
                    output = "den "
                elif genus == "feminine":
                    output = "die "
                elif genus == "neutral":
                    output = "das "
            if number == "plural":
                output = ""
    else:
        print(number, genus, article_type, case)
        output = "Achtung"
    return output


class preposition:
        def __init__(self, word, preposition_type):
            self.word = word
            self.preposition_type = preposition_type


source = open("list_of_prepositions.txt", "r")
source = source.readlines()
counter = 0
list_of_prepositions = []
while counter < len(source):
    file = "item = " + source[counter]
    exec(file)  
    counter = counter + 1 
    list_of_prepositions.append(item)
for x in list_of_verbs:
    x.word = encoding(x.word)
         


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
    





print(generate_sentence())








        





        

