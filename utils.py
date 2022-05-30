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
    while output[-2:] == "  ":
        output = output[:-1]
    
    if output != "":
        output = output + " "
    return output



#def find
"""
if sentence_mode == "declarative":
    output = surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") + surface(subject) + surface(predicate, subject) + surface(object1_determinative, predicate.object_case) \
             + surface(object1, case=predicate.object_case) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
            + surface(preposition) + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required#
    if object2:
        if type(object2) == part_of_speech.pronoun:
            output = surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") \
                + surface(subject) + surface(predicate, subject) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
                + surface(object1_determinative, predicate.object_case) + surface(object1, case=predicate.object_case) + surface(preposition)\
                + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required
elif sentence_mode == "interrogative":
    output = surface(predicate, subject) + surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") + surface(subject) + surface(object1_determinative, predicate.object_case) \
             + surface(object1, case=predicate.object_case) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
            + surface(preposition) + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required#
    if object2:
        if type(object2) == part_of_speech.pronoun:
            output = surface(predicate, subject) + surface(subject_determinative) + surface(subject_adjective, subject, subject_determinative.article_type, subject.number, subject.genus, "nominative") \
                + surface(subject) + surface(object2_determinative, predicate.object_case) + surface(object2, case="accusative") \
                + surface(object1_determinative, predicate.object_case) + surface(object1, case=predicate.object_case) + surface(preposition)\
                + surface(location_article) + surface(location_adjective, article_type="determinative", number="singular", genus=location.genus, case="dative") + surface(location) + detached_affix_if_required
"""