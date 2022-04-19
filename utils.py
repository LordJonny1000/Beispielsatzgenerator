import part_of_speech

def surface(instance, subject=None, case="nominative"):
    if type(instance) == part_of_speech.noun:
        return instance.declension(instance.number, case) + " "
    elif type(instance) == part_of_speech.verb:
        return instance.conjugation(subject.person, subject.number) + " "
    elif type(instance) == part_of_speech.article:
        return instance.word + " "
    elif type(instance) == part_of_speech.pronoun:
        return instance.word + " "
    elif type(instance) == part_of_speech.person_name:
        return instance.word + " "
    elif type(instance) == str:
        return instance
    
