import part_of_speech

def surface(instance, subject=None, article_type="determinative", number="singular", genus="neutral", case="nominative",):
    if type(instance) == part_of_speech.noun:
        output = instance.declension(case)
    if type(instance) == part_of_speech.adjective:
        output = instance.declension(article_type, number, genus, case)
    elif type(instance) == part_of_speech.verb:
        output = instance.conjugation(subject.person, subject.number)
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

    while output[-2:] == "  ":
        output = output[:-1]
    
    if output != "":
        output = output + " "
    return output
