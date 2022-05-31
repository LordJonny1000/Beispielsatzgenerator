import part_of_speech

def surface(instance):
    if type(instance) == part_of_speech.noun:
        output = instance.declension()
    if type(instance) == part_of_speech.adjective:
        output = instance.declension()
    elif type(instance) == part_of_speech.verb:
        output = instance.conjugation()
    elif type(instance) == part_of_speech.article:
        output = instance.word
    elif type(instance) == part_of_speech.pronoun:
        output = instance.word
    elif type(instance) == part_of_speech.proper_name:
        output = instance.word
    elif type(instance) == part_of_speech.preposition:
        output = instance.word
    elif type(instance) == str:
        return instance
    return output

def basic_word_form(instance):
    if type(instance) == str:
        return ""
    else:
        return instance.word
    
    


