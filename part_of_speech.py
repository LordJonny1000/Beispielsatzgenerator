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
        self.number = linguistics.numbers[random.randrange(2)]
    @classmethod
    def from_list(cls, list_entry):
        return cls(list_entry[0], list_entry[1], list_entry[2], list_entry[3])
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
    @classmethod
    def from_list(cls, list_entry):
        return cls(list_entry[0], list_entry[1], list_entry[2], list_entry[3], list_entry[4])
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
        return output

class adjective:
    def __init__(self, word):
        self.word = word
    @classmethod
    def from_string(cls, string):
        return cls(string)
    def declension(self, number, article_type, case="nominative",):
        output = self.word + "e"
        if case=="nominative" and number =="singular" :
            output = output
            if article_type == "indefinite":
                output = output + "r"
        else:
            output = output + "n"
            
class person_name:

    def __init__(self, word, genus):
        self.word = word
        self.genus = genus
        self.person = "3rd"
        self.number = "singular"
    @classmethod
    def from_list(cls, list_entry):
        return cls(list_entry[0], list_entry[1])
    def declension(self, number, case="nominative"):
        return self.word


    
class preposition:
        def __init__(self, word, preposition_type):
            self.word = word
            self.preposition_type = preposition_type
        @classmethod
        def from_list(cls, list_entry):
            return cls(list_entry[0], list_entry[1])
        
class pronoun:
        def __init__(self, pronoun_type, person, number, genus, case):
            self.pronoun_type = pronoun_type
            self.person = person
            self.number = number
            self.genus = genus
            self.case = case
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
        if case == "nominative" or case == 0:
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
            print(number, genus, article_type, case)
            output = "Achtung, der Artikel konnte nicht gebildet werden!"  
        self.word = output


            

