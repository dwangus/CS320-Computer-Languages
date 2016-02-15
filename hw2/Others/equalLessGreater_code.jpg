    tokens = tmp[0:]
    if tokens[0] == 'equal' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (tree1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (tree2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Equal':[tree1,tree2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'less' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (tree1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (tree2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Less':[tree1,tree2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'greater' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (tree1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (tree2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Greater':[tree1,tree2]}, tokens)
