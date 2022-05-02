# Welcome to my project "Beispielsatzgeneator"!
# This non-deterministic script receives annotated lists of words (one list for each part of speech, sored in the folder "vocabulary") and
# generates a german sentence out of it, that is not only correct concerning syntax and morphology but makes sense aswell (at least in a wider sense).
# This are the most important files so far:
# "part_of_speech.py" contains a class for each part of speech, describing the required morphological processes that are necessary to form a sentence
# "linguistics.py" contains a collection of constants that determine certain linguistic basics and makes it possible 
# to choose an option randomly. (e.g."singular" and "plural")
# "probability_settings.py" contains changable values that determine the probability of certain events to occur .(e.g. if the sentence should be in 
# interrogative clause or the object should be modified by an adjective)
# "utils.py" contains a function that can transform an instance of a class item from part_of_speech.py into a surface string, independent of the class.
# The folder "vocabulary" contains files that contain each a list with the vocabulary and its annotations
# "german_sentence_generator.py" puts all together by choosing a rondom verb (predicate) and then adds necessary other arguments according to the verbs
# valency which is stored in the verb's annotation. Beyond that, there is a certain probability that the nouns are modified by adjectives, a phrase with
# a location is added, the article is replaced by a possesive pronoun (this one is still in progress) and much more. 
#
# The aim would be to create more and more complex sentences while the morphological proecesses should happen full automatically and the annotations should
# be used to keep the sentences at least a bit meaningful (this means, it should be sentences that could theoretically be uttered in a situation)
# When the generator is ready, my next step is to generate a great amount of sentences which I will annotate manually with a rating (either binary or in a
# scale) and use this annotated output as training data for a perceptron.
# Then, the perceptron could rate its own sentences after generating them and only return sentences above a certain tresholf (or only meaningful ones in the
# case of binary classification)
#
# Feel free to experiment, enhance it or give some inspiration.
#
#
