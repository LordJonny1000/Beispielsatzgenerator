import part_of_speech

def surface(instance, subject=None, article_type = "determinative", number="singular", genus="neutral", case="nominative",):
    if type(instance) == part_of_speech.noun:
        return instance.declension(case) + " "
    if type(instance) == part_of_speech.adjective:
        return instance.declension(article_type, number, genus, case)
    elif type(instance) == part_of_speech.verb:
        return instance.conjugation(subject.person, subject.number)
    elif type(instance) == part_of_speech.article:
        return instance.word
    elif type(instance) == part_of_speech.pronoun:
        return instance.word + " "
    elif type(instance) == part_of_speech.proper_name:
        return instance.word  + " "
    elif type(instance) == str:
        return instance
    
