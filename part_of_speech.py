numbers = ["singular", "plural"]
import random
import linguistics


class noun:
    def __init__(self, word, strong_or_weak, genus, ability_to_act):
        self.word = word
        self.genus = genus
        self.strong_or_weak = strong_or_weak
        self.lemma = self.word
        self.ability_to_act = ability_to_act
        self.person = "3rd"
        self.number = numbers[random.randrange(2)]
    def declension(self, number, case="nominative"):
        if number == "plural":  
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
        elif number == "singular":
            output = self.lemma
        # N for "gefällt den GeneräleN", "empfiehlt dem HaseN"
        #errors: Meister Proper riecht den Hase., sieht der Handgranaten unter der Disco zu.
        if case == "dative" and output[-1] == "e" and output[-2] != "t" :
            output = output + "n"
        elif case == "dative" and output[-1] == "e" and output[-2] != "t" :
            output = output + "n"
        output = output + " "
        return output

class verb:
    def __init__(self, word, strong_or_weak, valency, object_case, θrolls):
        self.word = word
        self.strong_or_weak = strong_or_weak
        self.valency = valency
        self.object_case = object_case
        self.θrolls = θrolls
        if self.word[-2] == "e" and self.word[-1] == "n":
            self.lemma = self.word[:-2]
        elif self.word[-2] != "e" and self.word[-1] == "n":
            self.lemma = self.word[:-1]        
    def conjugation(self, person, number):
        for affix in linguistics.detached_affixes:
            if self.lemma[:len(affix)] == affix:
                self.lemma = self.lemma.replace(affix, "", 1)  
                break
        if self.strong_or_weak == "strong":
            index_of_v_vowel = 0
            index_of_last_vowel = 0

            if (person == "3rd" and number == "singular") or (person == "2nd" and number == "singular"):
                for v in linguistics.vowels:
                    try: 
                        index_of_v_vowel = (len(self.lemma) - self.lemma[::-1].index(v) - 1)
                    except: 
                        pass
                    if index_of_v_vowel > index_of_last_vowel:
                        index_of_last_vowel = index_of_v_vowel
                if self.lemma[index_of_last_vowel] == "a":
                    list_for_transformation = list(self.lemma)
                    list_for_transformation[index_of_last_vowel] = 'ä'
                    self.lemma = ''.join(list_for_transformation)
                if self.lemma[index_of_last_vowel] == "e":
                    list_for_transformation = list(self.lemma)
                    list_for_transformation[index_of_last_vowel] = 'i'
                    self.lemma = ''.join(list_for_transformation)
                
                    self.lemma = ''.join(list_for_transformation)   
                if self.word in linguistics.conjugation_exceptions:
                    if self.word == "laufen" or self.word == "saufen":
                        list_for_transformation = list(self.lemma)
                        list_for_transformation[self.word.index("a")] = 'ä'
                        self.lemma = ''.join(list_for_transformation) 
                    if self.word == "stehlen" or self.word == "empfehlen" or self.word == "sehen" or self.word == "geschehen" or self.word == "befehlen":
                        self.lemma = self.lemma.replace("ih", "ieh") 
                    elif self.word == "lesen":
                        self.lemma = self.lemma.replace("i", "ie")
        if person == "1st" and number == "singular":
            output = self.lemma + "e"
        elif person == "2nd" and number == "singular":
            if self.lemma[-1] == "t":
                output = self.lemma + "est"
            else:
                output = self.lemma + "st"
        elif person == "3rd" and number == "singular":
            if self.lemma[-1:] in("n", "t"):
                output = self.lemma + "et"
            else:
                output = self.lemma + "t"
        elif person == "1st" and number == "plural":
            output = self.lemma + "en"
        elif person == "2nd" and number == "plural":
            output = self.lemma + "t"
        elif person == "3rd" and number == "plural":
            if self.lemma[-2:] in("er", "el") and self.lemma != "spiel":
                output = self.lemma + "n"
            else:
                output = self.lemma + "en"
        else:
            output = "X"

        #exception for sehen
        if person == "3rd" and number == "singular" and self.word in("sehen", "zusehen"):
            output = "sieht"
        
        output = output + " "
        return output

from vocabulary import nouns, verbs
list_of_nouns_as_dicts = nouns.list_of_nouns
list_of_verbs_as_dicts = verbs.list_of_verbs
list_of_nouns = list()
for n in list_of_nouns_as_dicts:
    list_of_nouns.append(noun(n["word"], n["strong_or_weak"], n["genus"], n["ability_to_act"]))
list_of_verbs = list()
for v in list_of_verbs_as_dicts:
    list_of_verbs.append(verb(v["word"], v["strong_or_weak"], v["valency"], v["object_case"], v["θrolls"]))
    
print(list_of_verbs)

