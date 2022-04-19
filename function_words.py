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


            