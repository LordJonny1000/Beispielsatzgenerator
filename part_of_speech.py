import random
import linguistics
from vocabulary.semantic_classes import locations, events




class noun:
    def __init__(self, word, strong_or_weak, genus, ability_to_act, mass_noun, period = True):
        self.word = word
        self.genus = genus
        self.strong_or_weak = strong_or_weak
        self.lemma = self.word
        self.ability_to_act = ability_to_act
        self.person = "3rd"
        self.number = random.choice(linguistics.numbers)
        self.case = "nominative"
        self.mass_noun = mass_noun
        self.period = period
        if self.mass_noun:
            self.number = "singular"
        if self.word in [x[0] for x in locations.list_of_locations] or self.word in [x[0] for x in events.list_of_events]:#only unse singular for locations and events
            self.number = "singular"
        if self.word in(linguistics.nouns_without_plural_form):
            self.mass_noun = True
    @classmethod
    def from_list(cls, list_entry):
        if len(list_entry) == 5:
            return cls(list_entry[0], list_entry[1], list_entry[2], list_entry[3], list_entry[4])
        else:
            return cls(list_entry[0], list_entry[1], list_entry[2], list_entry[3], list_entry[4], list_entry[5])
    def declension(self):
        if self.word == "":
            return ""
        if self.number == "singular":
            output = self.lemma 
        if self.number == "plural":  
            if self.strong_or_weak == "strong":
                last_possible_umlaut = ""
                counter = 0
                for l in self.lemma:
                    if l in("a", "o", "u", "A", "O", "U"):
                        last_possible_umlaut = l
                        if last_possible_umlaut == "u" and self.lemma[counter-1] in ("a", "e"):
                            last_possible_umlaut = self.lemma[counter-1]
                    counter = counter + 1
                if last_possible_umlaut == "A":
                    list_for_transformation = list(self.lemma)
                    list_for_transformation[self.lemma.index("A")] = 'Ä'
                    self.lemma = ''.join(list_for_transformation)
                elif last_possible_umlaut == "a":
                    list_for_transformation = list(self.lemma)
                    list_for_transformation[self.lemma.index("a")] = 'ä'
                    self.lemma = ''.join(list_for_transformation)
                elif last_possible_umlaut == "u":
                    list_for_transformation = list(self.lemma)
                    list_for_transformation[self.lemma.index("u")] = 'ü'
                    self.lemma = ''.join(list_for_transformation)
                elif last_possible_umlaut == "o":
                    list_for_transformation = list(self.lemma)
                    list_for_transformation[self.lemma.index("o")] = 'ö'
                    self.lemma = ''.join(list_for_transformation) 
                    
            if self.word[-3:] in("ent", "and", "ant", "ist") and self.genus == "masculine":
                output = self.lemma + "en"
            elif  self.word[-1:] == "e" and self.genus == "masculine":
                output = self.lemma + "n"
            elif self.word[-2:] in("or", "ot",) and self.genus == "masculine":
                output = self.lemma + "en"
            elif self.word[-1:] == "e" and self.genus == "feminine":
                output = self.lemma + "n"
            elif  self.word[-2:] in("ik", "in", "el") and self.genus == "feminine":
                if self.word[-2:] == "el":
                    output = self.lemma + "n"
                else:
                    output = self.lemma + "e"    
            elif  self.word[-4:] in("heit", "keit") and self.genus == "feminine":
                output = self.lemma + "en"
            elif  self.word[-3:] in("ion", "tät","ung") and self.genus == "feminine":
                output = self.lemma + "en"
            elif  self.word[-6:] == "schaft" and self.genus == "feminine":
                output = self.lemma + "en"
            elif  self.word[-2:] in("ma", "um", "us"):
                if self.word[-2:] == "ma":
                    output = self.lemma[:-1] + "en"
                elif self.word[-2:] == "um":
                    output = self.lemma + "e"
                else: 
                    output = self.lemma + "en"
            elif self.word[-4:] == "ling" and self.genus == "masculine":
                output = self.lemma + "e"
            elif self.word[-3:] in("eur","ich", "ier", "uhl", "ehl", "rzt") and self.genus == "masculine":
                output = self.lemma + "e"
            elif self.word[-2:] in("ig", "ör", "al", "äl") and self.genus == "masculine":
                output = self.lemma + "e"
            elif self.word[-2:] in("ff", "rk", "il") and self.genus == "neutral":
                output = self.lemma + "e"
            elif self.word[-3:] == "eid" and self.genus == "neutral":
                output = self.lemma + "er"
            elif self.word[-2:] in("en") and self.genus == "neutral":
                output = self.lemma
            #independent of genus
            elif self.word[-2:] in("er", "el"):
                output = self.lemma
            elif self.word[-2:] == "st":
                output = self.lemma + "e"
            else: 
                output = self.lemma + "s"
        if self.case == "dative":
            if self.number == "plural":
                if output[-1] == "e":
                    output = output + "n"
                if output[-2:] == "el":
                    output = output + "n"
                if output[-3:] == "ent":
                    output = output + "en"
            if self.word in(linguistics.dative_with_en) and output[-1] != "n":
                output += "n"
        if self.case == "accusative" and not self.mass_noun :
            if self.word in(linguistics.accusative_with_en) and output[-1] != "n":
                output = output + "n"
            elif output[-2:] == "ot":
                output = output + "en"
        return output
    

class verb:
    def __init__(self, word, strong_or_weak, valency, object_case, θrolls, movement):
        self.word = word
        self.strong_or_weak = strong_or_weak
        self.valency = valency
        self.object_case = object_case
        self.θrolls = θrolls
        self.movement = movement
        if self.word[-2:] == "en":
            self.lemma = self.word[:-2]
        else:
            self.lemma = self.word[:-1]
    @classmethod
    def from_list(cls, list_entry):
        return cls(list_entry[0], list_entry[1], list_entry[2], list_entry[3], list_entry[4], list_entry[5])
    
    def conjugation(self):
        new_lemma = self.lemma
        for affix in linguistics.detached_affixes:
            if new_lemma[:len(affix)] == affix:
                new_lemma = new_lemma.replace(affix, "", 1)
                break
        if self.strong_or_weak == "strong":
            index_of_v_vowel = 0
            index_of_last_vowel = 0

            if self.number == "singular" and self.person != "1st":
                for v in linguistics.vowels:
                    try: 
                        index_of_v_vowel = len(new_lemma) - new_lemma[::-1].index(v) - 1
                    except: 
                        pass
                    if index_of_v_vowel > index_of_last_vowel:
                        index_of_last_vowel = index_of_v_vowel
                if new_lemma[index_of_last_vowel] in ("a", "e"):
                    list_for_transformation = list(new_lemma)
                    list_for_transformation[index_of_last_vowel] = ["ä", "i"][["a", "e"].index(new_lemma[index_of_last_vowel])]
                    new_lemma = ''.join(list_for_transformation)  
                if self.word in linguistics.conjugation_exceptions:
                    if self.word in("laufen", "saufen"):
                        list_for_transformation = list(new_lemma)
                        list_for_transformation[self.word.index("a")] = 'ä'
                        new_lemma = ''.join(list_for_transformation) 
                    if self.word in("stehlen", "empfehlen", "sehen", "geschehen", "befehlen"):
                        new_lemma = new_lemma.replace("ih", "ieh") 
                    elif self.word == "lesen":
                        new_lemma = new_lemma.replace("i", "ie")
        if self.person == "1st" and self.number == "singular":
            output = new_lemma + "e"
            if self.word[-3:] == "eln":
                output = output[:-3] + output[-2:]
        elif self.person == "2nd" and self.number == "singular":
            if new_lemma[-1] == "t":
                output = new_lemma + "est"
            elif new_lemma[-1] == "s":
                output = new_lemma + "t"
            else:
                output = new_lemma + "st"
        elif self.person == "3rd" and self.number == "singular":
            if new_lemma[-1:] in("n", "t"):
                output = new_lemma + "et"
            else:
                output = new_lemma + "t"
        elif self.person == "1st" and self.number == "plural":
            output = new_lemma + "en"
            if self.word[-3:] in ("ern", "eln"):#<---adjust certain words
                output = output[:-2] + output[-1]

        elif self.person == "2nd" and self.number == "plural":
            output = new_lemma + "t"
        elif self.person == "3rd" and self.number == "plural":
            if new_lemma[-2:] in("er", "el") and new_lemma != "spiel":
                output = new_lemma + "n"
            else:
                output = new_lemma + "en"
        if self.person == "3rd" and self.number == "singular" and self.word in("sehen", "zusehen"):#<---- exception for sehen
            output = "sieht"
        if self.person == "2nd" and self.number == "singular" and self.word in("sehen", "zusehen"):
            output =  "siehst"
        return output



class adjective:
    def __init__(self, word):
        self.word = word
    @classmethod
    def from_string(cls, string):
        return cls(string)
    def declension(self):
        if self.word == "":
            return ""
        if self.case=="nominative":
            if self.number == "singular":
                if self.article_type == "definite":
                    return self.word + "e"
                elif self.article_type == "indefinite":
                    if self.genus == "masculine":
                        return self.word + "er"
                    elif self.genus == "feminine":
                        return self.word + "e"
                    elif self.genus == "neutral":
                        return self.word + "es"
            elif self.number == "plural":
                if self.article_type == "definite":
                    return self.word + "en"
                elif self.article_type == "indefinite":
                    return self.word + "e"
                
            
            else:            
                return self.word + "e"
        elif self.case=="dative":
            return self.word + "en"
        elif self.case=="accusative":
            if self.number =="singular":
                if self.article_type == "definite":
                    
                    if self.genus == "masculine":
                        
                        return self.word + "en"
                    elif self.genus in("feminine", "neutral"):
                        return self.word + "e"
                elif self.article_type == "indefinite":
                    if self.genus == "masculine":
                        return self.word + "en"
                    elif self.genus == "feminine":
                        return self.word + "e"
                    elif self.genus == "neutral":
                        return self.word + "es"
            elif self.number == "plural":
                if self.article_type == "definite":
                    return self.word + "en"
                elif self.article_type == "indefinite":
                    return self.word + "e"
            return self.word
        else:
            return self.word
        return ""
            
class proper_name:

    def __init__(self, word, genus):
        self.word = word
        self.genus = genus
        self.person = "3rd"
        self.number = "singular"
        self.mass_noun = False
    @classmethod
    def from_list(cls, list_entry):
        return cls(list_entry[0], list_entry[1])
    def declension(self):
        return self.word


    
class preposition:
        def __init__(self, word, preposition_type, movement_or_period, case):
            self.word = word
            self.preposition_type = preposition_type
            self.movement_or_period = movement_or_period
            self.case = case
        @classmethod
        def from_list(cls, list_entry):
            return cls(list_entry[0], list_entry[1], list_entry[2], list_entry[3])

class pronoun:
        def __init__(self, pronoun_type, person, number, genus, case, noun_number = "singular", noun_genus = "neutral"):
            self.pronoun_type = pronoun_type
            self.person = person
            self.number = number
            self.genus = genus
            self.case = case
            self.noun_number = noun_number
            self.noun_genus = noun_genus
            self.mass_noun = False
            if self.pronoun_type == "personal":
                if self.number == "singular":
                    if self.person == "1st":
                        self.word =  "ich"
                    elif self.person == "2nd":
                        self.word =  "du"
                    elif self.person == "3rd":
                        if self.genus == "masculine":
                            self.word =  "er"
                        elif self.genus == "feminine":
                            self.word =  "sie"
                        elif self.genus == "neutral":
                            self.word =  "es"
                elif self.number == "plural":
                    if self.person == "1st":
                        self.word =  "wir"
                    elif self.person == "2nd":
                        self.word =  "ihr"
                    elif self.person == "3rd":
                        self.word =  "sie"
            elif self.pronoun_type == "possesive":
                self.article_type = "determinative"
                if self.number == "singular":
                    if self.person == "1st":
                        self.word =  "mein"
                    elif self.person == "2nd":
                        self.word =  "dein"
                    elif self.person == "3rd":
                        if self.genus in("neutral", "masculine"):
                            self.word =  "sein"
                        elif self.genus == "feminine":
                            self.word =  "ihr"
                elif self.number == "plural":
                    if self.person == "1st":
                        self.word =  "unser"
                    elif self.person == "2nd":
                        self.word =  "euer"
                    elif self.person == "3rd":
                        self.word =  "ihr"
                if self.person == "2nd" and self.number == "plural" and self.case == "nominative":
                    if self.noun_genus == "feminine" or self.noun_number == "plural":
                        self.word = "eur"
                if self.case == "nominative":
                    if self.noun_genus == "feminine" or self.noun_number == "plural":
                        self.word = self.word + "e"
                elif self.case == "dative":
                    if self.person == "2nd" and self.number == "plural":
                        self.word = "eur"
                    if self.noun_number == "singular":
                        if self.noun_genus in("masculine", "neutral"):
                            self.word += "em"
                        elif self.noun_genus == "feminine":
                            self.word += "er"
                    elif self.noun_number == "plural":
                        self.word += "en"
                elif self.case == "accusative":
                    if self.person == "2nd" and self.number == "plural":
                        if self.noun_genus in("feminine", "masculine") or self.noun_number == "plural":
                            self.word = "eur"
                    if self.noun_number == "singular":
                        if self.noun_genus == "feminine":
                            self.word += "e"
                        elif self.noun_genus == "masculine":

                            self.word += "en"
                    elif self.noun_number == "plural":
                        self.word += "e"
            elif self.pronoun_type == "reflexive":
                if self.case == "dative":
                    if self.number == "singular":
                        if self.person == "1st":
                            self.word =  "mir"
                        elif self.person == "2nd":
                            self.word =  "dir"
                        elif self.person == "3rd":
                            if self.genus in("neutral", "masculine"):
                                self.word =  "ihm"
                            elif self.genus == "feminine":
                                self.word =  "ihr"
                    elif self.number == "plural":
                        if self.person == "1st":
                            self.word =  "uns"
                        elif self.person == "2nd":
                            self.word =  "euch"
                        elif self.person == "3rd":
                            self.word =  "ihnen"
                elif self.case == "accusative":
                    if self.number == "singular":
                        if self.person == "1st":
                            self.word =  "mich"
                        elif self.person == "2nd":
                            self.word =  "dich"
                        elif self.person == "3rd":
                            if self.genus == "masculine":
                                self.word =  "ihn"
                            elif self.genus == "feminine":
                                self.word =  "sie"
                            elif self.genus == "neutral":
                                self.word =  "es"
                    elif self.number == "plural":
                        if self.person == "1st":
                            self.word =  "uns"
                        elif self.person == "2nd":
                            self.word =  "euch"
                        elif self.person == "3rd":
                            self.word =  "sie"
                            
class article:
    def __init__(self, article_type, number, genus, case="nominative"):
        self.article_type = article_type
        self.number = number
        self.genus = genus
        self.case = case
        self.word = "Achtung, der Artikel konnte nicht gebildet werden!"
        if case == "nominative":
            if article_type == "definite":
                if number == "singular":
                    if genus == "masculine":
                        output = "der"
                    elif genus == "feminine":
                        output = "die"
                    elif genus == "neutral":
                        output = "das"
                elif number == "plural":
                    output = "die"
            elif article_type == "indefinite":
                if number == "singular":
                    if genus == "masculine":
                        output = "ein"
                    elif genus == "feminine":
                        output = "eine"
                    elif genus == "neutral":
                        output = "ein"
                if number == "plural":
                    output = ""
        elif case == "genitive":
            if article_type == "definite":
                if number == "singular":
                    if genus == "masculine":
                        output = "des"
                    elif genus == "feminine":
                        output = "der"
                    elif genus == "neutral":
                        output = "des"
                elif number == "plural":
                    output = "der"
            elif article_type == "indefinite":
                if number == "singular":
                    if genus == "masculine":
                        output = "eines"
                    elif genus == "feminine":
                        output = "einer"
                    elif genus == "neutral":
                        output = "eines"
                if number == "plural":
                    output = ""
        elif case == "dative":
            if article_type == "definite":
                if number == "singular":
                    if genus == "masculine":
                        output = "dem"
                    elif genus == "feminine":
                        output = "der"
                    elif genus == "neutral":
                        output = "dem"
                elif number == "plural":
                    output = "den"
            elif article_type == "indefinite":
                if number == "singular":
                    if genus == "masculine":
                        output = "einem"
                    elif genus == "feminine":
                        output = "einer"
                    elif genus == "neutral":
                        output = "einem"
                if number == "plural":
                    output = ""
        elif case == "accusative":
            if article_type == "definite":
                if number == "singular":
                    if genus == "masculine":
                        output = "den"
                    elif genus == "feminine":
                        output = "die"
                    elif genus == "neutral":
                        output = "das"
                elif number == "plural":
                    output = "die"
            elif article_type == "indefinite":
                if number == "singular":
                    if genus == "masculine":
                        output = "einen"
                    elif genus == "feminine":
                        output = "eine"
                    elif genus == "neutral":
                        output = "ein"
                if number == "plural":
                    output = ""
        else:
            output = "Achtung, der Artikel konnte nicht gebildet werden!"
        try: 
            self.word = output
        except NameError:
            self.word = ""

