import functools
import re
import math
input_shanghai = "SH"
input_shanghai_city = "SHC"
def SkelClass(class_name):
    Clz = type(class_name, (), {'_class_name': class_name})
    return Clz()
def StringDistance(*args):
    def distance(s0, s1):
        return None
    class_var = SkelClass('StringDistance')
    class_var.distance = distance
    return class_var
def NormalizedStringDistance(*args):
    def distance(s0, s1):
        return None
    class_var = StringDistance(*args)
    class_var._class_name = 'NormalizedStringDistance;' + class_var._class_name
    class_var.distance = distance
    return class_var
def MetricStringDistance(*args):
    def distance(s0, s1):
        return None
    class_var = StringDistance(*args)
    class_var._class_name = 'MetricStringDistance;' + class_var._class_name
    class_var.distance = distance
    return class_var
def Levenshtein(*args):
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        if len(s0) == 0:
            return len(s1)
        if len(s1) == 0:
            return len(s0)
        v0 = [0] * (len(s1) + 1)
        v1 = [0] * (len(s1) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s0)):
            v1[0] = i + 1
            for j in range(len(s1)):
                cost = 1
                if s0[i] == s1[j]:
                    cost = 0
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            v0, v1 = v1, v0
        return v0[len(s1)]
    class_var = MetricStringDistance(*args)
    class_var._class_name = 'Levenshtein;' + class_var._class_name
    class_var.distance = distance
    return class_var
def LongestCommonSubsequence(*args):
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        return len(s0) + len(s1) - 2 * class_var.length(s0, s1)
    def length(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        s0_len, s1_len = len(s0), len(s1)
        x, y = s0[:], s1[:]
        matrix = [[0] * (s1_len + 1) for _ in range(s0_len + 1)]
        for i in range(1, s0_len + 1):
            for j in range(1, s1_len + 1):
                if x[i - 1] == y[j - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1] + 1
                else:
                    matrix[i][j] = max(matrix[i][j - 1], matrix[i - 1][j])
        return matrix[s0_len][s1_len]
    class_var = StringDistance(*args)
    class_var._class_name = 'LongestCommonSubsequence;' + class_var._class_name
    class_var.distance = distance
    class_var.length = length
    return class_var
def MetricLCS():
    def __init__():
        class_var.lcs = LongestCommonSubsequence()
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        max_len = int(max(len(s0), len(s1)))
        if max_len == 0:
            return 0.0
        return 1.0 - (1.0 * class_var.lcs.length(s0, s1)) / max_len
    class_var = MetricStringDistance()
    class_var._class_name = 'MetricLCS;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    __init__()
    return class_var
def NGram(param_0):
    def __init__(n):
        class_var.n = n
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        special = '\n'
        sl = len(s0)
        tl = len(s1)
        if sl == 0 or tl == 0:
            return 1.0
        cost = 0
        if sl < class_var.n or tl < class_var.n:
            for i in range(min(sl, tl)):
                if s0[i] == s1[i]:
                    cost += 1
            return 1.0 - cost / max(sl, tl)
        sa = [''] * (sl + class_var.n - 1)
        for i in range(len(sa)):
            if i < class_var.n - 1:
                sa[i] = special
            else:
                sa[i] = s0[i - class_var.n + 1]
        p = [0.0] * (sl + 1)
        d = [0.0] * (sl + 1)
        t_j = [''] * class_var.n
        for i in range(sl + 1):
            p[i] = 1.0 * i
        for j in range(1, tl + 1):
            if j < class_var.n:
                for ti in range(class_var.n - j):
                    t_j[ti] = special
                for ti in range(class_var.n - j, class_var.n):
                    t_j[ti] = s1[ti - (class_var.n - j)]
            else:
                t_j = s1[j - class_var.n:j]
            d[0] = 1.0 * j
            for i in range(sl + 1):
                cost = 0
                tn = class_var.n
                for ni in range(class_var.n):
                    if sa[i - 1 + ni] != t_j[ni]:
                        cost += 1
                    elif sa[i - 1 + ni] == special:
                        tn -= 1
                ec = cost / tn
                d[i] = min(d[i - 1] + 1, p[i] + 1, p[i - 1] + ec)
            p, d = d, p
        return p[sl] / max(tl, sl)
    class_var = NormalizedStringDistance()
    class_var._class_name = 'NGram;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    __init__(param_0)
    return class_var
def Damerau(*args):
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        inf = int(len(s0) + len(s1))
        da = dict()
        for i in range(len(s0)):
            da[s0[i]] = str(0)
        for i in range(len(s1)):
            da[s1[i]] = str(0)
        h = []
        for _ in range(len(s0) + 2):
            h.append([0] * (len(s1) + 2))
        for i in range(len(s0) + 1):
            h[i + 1][0] = inf
            h[i + 1][1] = i
        for j in range(len(s1) + 1):
            h[0][j + 1] = inf
            h[1][j + 1] = j
        for i in range(1, len(s0) + 1):
            db = 0
            for j in range(1, len(s1) + 1):
                i1 = int(da[s1[j - 1]])
                j1 = db
                cost = 1
                if s0[i - 1] == s1[j - 1]:
                    cost = 0
                    db = j
                h[i + 1][j + 1] = min(h[i][j] + cost, h[i + 1][j] + 1, h[i][j + 1] + 1, h[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1))
            da[s0[i - 1]] = str(i)
        return h[len(s0) + 1][len(s1) + 1]
    class_var = MetricStringDistance(*args)
    class_var._class_name = 'Damerau;' + class_var._class_name
    class_var.distance = distance
    return class_var
def ShingleBased(param_0):
    def __init__(k):
        class_var.k = k
    def get_k():
        return class_var.k
    def get_profile(string):
        shingles = dict()
        no_space_str = _SPACE_PATTERN.sub(" ", string)
        for i in range(len(no_space_str) - class_var.k + 1):
            shingle = no_space_str[i:i + class_var.k]
            old = shingles.get(shingle)
            if old:
                shingles[str(shingle)] = int(old + 1)
            else:
                shingles[str(shingle)] = 1
        return shingles
    class_var = SkelClass('ShingleBased')
    class_var.__init__ = __init__
    class_var.get_k = get_k
    class_var.get_profile = get_profile
    __init__(param_0)
    return class_var
def StringSimilarity(*args):
    def similarity(s0, s1):
        return None
    class_var = SkelClass('StringSimilarity')
    class_var.similarity = similarity
    return class_var
def NormalizedStringSimilarity(*args):
    def similarity(s0, s1):
        return None
    class_var = StringSimilarity(*args)
    class_var._class_name = 'NormalizedStringSimilarity;' + class_var._class_name
    class_var.similarity = similarity
    return class_var
def Cosine(param_0):
    def __init__(k):
        pass
    def distance(s0, s1):
        return 1.0 - class_var.similarity(s0, s1)
    def similarity(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 1.0
        if len(s0) < class_var.get_k() or len(s1) < class_var.get_k():
            return 0.0
        profile0 = class_var.get_profile(s0)
        profile1 = class_var.get_profile(s1)
        return class_var._dot_product(profile0, profile1) / (class_var._norm(profile0) * class_var._norm(profile1))
    def _dot_product(profile0, profile1):
        small = profile1
        large = profile0
        if len(profile0) < len(profile1):
            small = profile0
            large = profile1
        agg = 0.0
        for k, v in small.items():
            i = large.get(k)
            if not i:
                continue
            agg += 1.0 * v * i
        return agg
    def _norm(profile):
        agg = 0.0
        for k, v in profile.items():
            agg += 1.0 * v * v
        return math.sqrt(agg)
    class_var = ShingleBased(param_0)
    class_var._class_name = 'Cosine;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    class_var.similarity = similarity
    class_var._dot_product = _dot_product
    class_var._norm = _norm
    __init__(param_0)
    return class_var
def Jaccard(param_0):
    def __init__(k):
        pass
    def distance(s0, s1):
        return 1.0 - class_var.similarity(s0, s1)
    def similarity(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 1.0
        if len(s0) < class_var.get_k() or len(s1) < class_var.get_k():
            return 0.0
        profile0 = class_var.get_profile(s0)
        profile1 = class_var.get_profile(s1)
        union = set()
        for ite in profile0.keys():
            union.add(ite)
        for ite in profile1.keys():
            union.add(ite)
        inter = int(len(profile0.keys()) + len(profile1.keys()) - len(union))
        return 1.0 * inter / len(union)
    class_var = ShingleBased(param_0)
    class_var._class_name = 'Jaccard;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    class_var.similarity = similarity
    __init__(param_0)
    return class_var
def JaroWinkler(param_0):
    def __init__(threshold):
        class_var.threshold = threshold
        class_var.three = 3
        class_var.jw_coef = 0.1
    def get_threshold():
        return class_var.threshold
    def similarity(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 1.0
        mtp = class_var.matches(s0, s1)
        m = mtp[0]
        if m == 0:
            return 0.0
        j = (m / len(s0) + m / len(s1) + (m - mtp[1]) / m) / class_var.three
        jw = j
        if j > class_var.get_threshold():
            jw = j + min(class_var.jw_coef, 1.0 / mtp[class_var.three]) * mtp[2] * (1 - j)
        return jw
    def distance(s0, s1):
        return 1.0 - class_var.similarity(s0, s1)
    def matches(s0, s1):
        if len(s0) > len(s1):
            max_str = s0
            min_str = s1
        else:
            max_str = s1
            min_str = s0
        ran = int(max(len(max_str) / 2 - 1, 0))
        match_indexes = [-1] * len(min_str)
        match_flags = [False] * len(max_str)
        matches = 0
        for mi in range(len(min_str)):
            c1 = min_str[mi]
            for xi in range(max(mi - ran, 0), min(mi + ran + 1, len(max_str))):
                if not match_flags[xi] and c1 == max_str[xi]:
                    match_indexes[mi] = xi
                    match_flags[xi] = True
                    matches += 1
                    break
        ms0, ms1 = [0] * matches, [0] * matches
        si = 0
        for i in range(len(min_str)):
            if match_indexes[i] != -1:
                ms0[si] = min_str[i]
                si += 1
        si = 0
        for j in range(len(max_str)):
            if match_flags[j]:
                ms1[si] = max_str[j]
                si += 1
        transpositions = 0
        for mi in range(len(ms0)):
            if ms0[mi] != ms1[mi]:
                transpositions += 1
        prefix = 0
        for mi in range(len(min_str)):
            if s0[mi] == s1[mi]:
                prefix += 1
            else:
                break
        return [matches, int(transpositions / 2), prefix, len(max_str)]
    class_var = NormalizedStringSimilarity()
    class_var._class_name = 'JaroWinkler;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.get_threshold = get_threshold
    class_var.similarity = similarity
    class_var.distance = distance
    class_var.matches = matches
    __init__(param_0)
    return class_var
def NormalizedLevenshtein():
    def __init__():
        class_var.levenshtein = Levenshtein()
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        m_len = max(len(s0), len(s1))
        if m_len == 0:
            return 0.0
        return class_var.levenshtein.distance(s0, s1) / m_len
    def similarity(s0, s1):
        return 1.0 - class_var.distance(s0, s1)
    class_var = NormalizedStringDistance()
    class_var._class_name = 'NormalizedLevenshtein;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    class_var.similarity = similarity
    __init__()
    return class_var
def OptimalStringAlignment(*args):
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        n, m = len(s0), len(s1)
        if n == 0:
            return 1.0 * n
        if m == 0:
            return 1.0 * m
        d = [[0] * (m + 2) for _ in range(n + 2)]
        for i in range(n + 1):
            d[i][0] = i
        for j in range(m + 1):
            d[0][j] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = 1
                if s0[i - 1] == s1[j - 1]:
                    cost = 0
                d[i][j] = min(d[i - 1][j - 1] + cost, d[i][j - 1] + 1, d[i - 1][j] + 1)
                if i > 1 and j > 1 and s0[i - 1] == s1[j - 2] and s0[i - 2] == s1[j - 1]:
                    d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)
        return d[n][m]
    class_var = StringDistance(*args)
    class_var._class_name = 'OptimalStringAlignment;' + class_var._class_name
    class_var.distance = distance
    return class_var
def OverlapCoefficient(param_0):
    def __init__(k):
        pass
    def distance(s0, s1):
        return 1.0 - class_var.similarity(s0, s1)
    def similarity(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 1.0
        union = set()
        profile0, profile1 = class_var.get_profile(s0), class_var.get_profile(s1)
        for k in profile0.keys():
            union.add(k)
        for k in profile1.keys():
            union.add(k)
        inter = int(len(profile0.keys()) + len(profile1.keys()) - len(union))
        return inter / min(len(profile0), len(profile1))
    class_var = ShingleBased(param_0)
    class_var._class_name = 'OverlapCoefficient;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    class_var.similarity = similarity
    __init__(param_0)
    return class_var
def QGram(param_0):
    def __init__(k):
        pass
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        profile0 = class_var.get_profile(s0)
        profile1 = class_var.get_profile(s1)
        return class_var.distance_profile(profile0, profile1)
    def distance_profile(profile0, profile1):
        union = set()
        for k in profile0.keys():
            union.add(k)
        for k in profile1.keys():
            union.add(k)
        agg = 0
        for k in union:
            v0, v1 = 0, 0
            if profile0.get(k) is not None:
                v0 = int(profile0.get(k))
            if profile1.get(k) is not None:
                v1 = int(profile1.get(k))
            agg += abs(v0 - v1)
        return agg
    class_var = ShingleBased(param_0)
    class_var._class_name = 'QGram;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    class_var.distance_profile = distance_profile
    __init__(param_0)
    return class_var
def SIFT4Options(param_0):
    def __init__(options):
        def _code0(x):
            return [i for i in x]
        def _code1(t1, t2):
            return t1 == t2
        def _code2(t1, t2):
            return 1
        def _code3(x):
            return x
        def _code4(c1, c2):
            return 1
        def _code5(lcss, trans):
            return lcss - trans
        class_var.options = {'maxdistance': 0, 'tokenizer': _code0, 'tokenmatcher': _code1, 'matchingevaluator': _code2, 'locallengthevaluator': _code3, 'transpositioncostevaluator': _code4, 'transpositionsevaluator': _code5}
        if isinstance(options, dict) and options.keys() == {'maxdistance'}:
            assert (isinstance(options['maxdistance'], int))
            class_var.options.update(options)
        class_var.maxdistance = class_var.options['maxdistance']
        class_var.tokenizer = class_var.options['tokenizer']
        class_var.tokenmatcher = class_var.options['tokenmatcher']
        class_var.matchingevaluator = class_var.options['matchingevaluator']
        class_var.locallengthevaluator = class_var.options['locallengthevaluator']
        class_var.transpositioncostevaluator = class_var.options['transpositioncostevaluator']
        class_var.transpositionsevaluator = class_var.options['transpositionsevaluator']
    class_var = MetricStringDistance()
    class_var._class_name = 'SIFT4Options;' + class_var._class_name
    class_var.__init__ = __init__
    __init__(param_0)
    return class_var
def SIFT4(*args):
    def distance(s1, s2, maxoffset, options):
        options = SIFT4Options(options)
        t1, t2 = options.tokenizer(s1), options.tokenizer(s2)
        l1, l2 = len(t1), len(t2)
        if l1 == 0:
            return l2
        if l2 == 0:
            return l1
        c1, c2, lcss, local_cs, trans, offset_arr = 0, 0, 0, 0, 0, []
        while (c1 < l1) and (c2 < l2):
            if options.tokenmatcher(t1[c1], t2[c2]):
                local_cs += options.matchingevaluator(t1[c1], t2[c2])
                isTrans = False
                i = 0
                while i < len(offset_arr):
                    ofs = offset_arr[i]
                    if (c1 <= ofs['c1']) or (c2 <= ofs['c2']):
                        isTrans = abs(c2 - c1) >= abs(ofs['c2'] - ofs['c1'])
                        if isTrans:
                            trans += options.transpositioncostevaluator(c1, c2)
                        else:
                            if not ofs['trans']:
                                ofs['trans'] = True
                                trans += options.transpositioncostevaluator(ofs['c1'], ofs['c2'])
                        break
                    else:
                        if (c1 > ofs['c2']) and (c2 > ofs['c1']):
                            offset_arr.pop(i)
                        else:
                            i += 1
                offset_arr.append({'c1': c1, 'c2': c2, 'trans': isTrans})
            else:
                lcss += options.locallengthevaluator(local_cs)
                local_cs = 0
                if c1 != c2:
                    c1 = c2 = min(c1, c2)
                for i in range(maxoffset):
                    if (c1 + i < l1) or (c2 + i < l2):
                        if (c1 + i < l1) and options.tokenmatcher(t1[c1 + i], t2[c2]):
                            c1 += i - 1
                            c2 -= 1
                            break
                    if (c2 + i < l2) and options.tokenmatcher(t1[c1], t2[c2 + i]):
                        c1 -= 1
                        c2 += i - 1
                        break
            c1 += 1
            c2 += 1
            if options.maxdistance:
                temporarydistance = options.locallengthevaluator(max(c1, c2)) - options.transpositionsevaluator(lcss, trans)
                if temporarydistance >= options.maxdistance:
                    return round(temporarydistance)
            if (c1 >= l1) or (c2 >= l2):
                lcss += options.locallengthevaluator(local_cs)
                local_cs = 0
                c1 = c2 = min(c1, c2)
        lcss += options.locallengthevaluator(local_cs)
        return round(options.locallengthevaluator(max(l1, l2)) - options.transpositionsevaluator(lcss, trans))
    class_var = SkelClass('SIFT4')
    class_var.distance = distance
    return class_var
def SorensenDice(param_0):
    def __init__(k):
        pass
    def distance(s0, s1):
        return 1.0 - class_var.similarity(s0, s1)
    def similarity(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 1.0
        union = set()
        profile0, profile1 = class_var.get_profile(s0), class_var.get_profile(s1)
        for k in profile0.keys():
            union.add(k)
        for k in profile1.keys():
            union.add(k)
        inter = int(len(profile0.keys()) + len(profile1.keys()) - len(union))
        return 2.0 * inter / (len(profile0) + len(profile1))
    class_var = ShingleBased(param_0)
    class_var._class_name = 'SorensenDice;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    class_var.similarity = similarity
    __init__(param_0)
    return class_var
def default_insertion_cost(char):
    return 1.0
def default_deletion_cost(char):
    return 1.0
def default_substitution_cost(char_a, char_b):
    return 1.0
def WeightedLevenshtein(param_0, param_1, param_2):
    def __init__(substitution_cost_fn, insertion_cost_fn, deletion_cost_fn):
        class_var.substitution_cost_fn = substitution_cost_fn
        class_var.insertion_cost_fn = insertion_cost_fn
        class_var.deletion_cost_fn = deletion_cost_fn
    def distance(s0, s1):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        if len(s0) == 0:
            return functools.reduce(lambda cost, char: cost + class_var.insertion_cost_fn(char), s1, 0)
        if len(s1) == 0:
            return functools.reduce(lambda cost, char: cost + class_var.deletion_cost_fn(char), s0, 0)
        v0, v1 = [0.0] * (len(s1) + 1), [0.0] * (len(s1) + 1)
        v0[0] = 0
        for i in range(1, len(v0)):
            v0[i] = v0[i - 1] + class_var.insertion_cost_fn(s1[i - 1])
        for i in range(len(s0)):
            s0i = s0[i]
            deletion_cost = class_var.deletion_cost_fn(s0i)
            v1[0] = v0[0] + deletion_cost
            for j in range(len(s1)):
                s1j = s1[j]
                cost = 0
                if s0i != s1j:
                    cost = class_var.substitution_cost_fn(s0i, s1j)
                insertion_cost = class_var.insertion_cost_fn(s1j)
                v1[j + 1] = min(v1[j] + insertion_cost, v0[j + 1] + deletion_cost, v0[j] + cost)
            v0, v1 = v1, v0
        return v0[len(s1)]
    class_var = StringDistance()
    class_var._class_name = 'WeightedLevenshtein;' + class_var._class_name
    class_var.__init__ = __init__
    class_var.distance = distance
    __init__(param_0, param_1, param_2)
    return class_var
def assert_equal(a, b):
    if a != b:
        raise Exception("MyLogError MISMATCH")
def test_levenshtein():
    a = Levenshtein()
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 2)
    assert_equal(a.distance(s0, s3), 3)
    assert_equal(a.distance(s1, s2), 2)
    assert_equal(a.distance(s1, s3), 3)
    assert_equal(a.distance(s2, s3), 1)
def test_longest_common_subsequence():
    a = LongestCommonSubsequence()
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(0, a.distance(s0, s1))
    assert_equal(2, a.distance(s0, s2))
    assert_equal(3, a.distance(s0, s3))
    assert_equal(1, a.distance(s2, s3))
    assert_equal(2, a.length(s2, s3))
    assert_equal(4, a.distance('AGCAT', 'GAC'))
    assert_equal(2, a.length('AGCAT', 'GAC'))
def test_metric_lcs():
    a = MetricLCS()
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 1.0)
    assert_equal(a.distance(s0, s3), 1.0)
    assert_equal(a.distance(s1, s2), 1.0)
    assert_equal(a.distance(s1, s3), 1.0)
    assert_equal(round(a.distance(s2, s3), 2), 0.33)
def test_ngram():
    a = NGram(2)
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 1.0)
    assert_equal(a.distance(s0, s3), 1.0)
    assert_equal(a.distance(s1, s2), 1.0)
    assert_equal(a.distance(s1, s3), 1.0)
    assert_equal(round(a.distance(s2, s3), 2), 0.33)
def test_damerau():
    a = Damerau()
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 2)
    assert_equal(a.distance(s0, s3), 3)
    assert_equal(a.distance(s1, s2), 2)
    assert_equal(a.distance(s1, s3), 3)
    assert_equal(a.distance(s2, s3), 1)
def test_cosine():
    cos = Cosine(1)
    s = ['', ' ', 'Shanghai', 'ShangHai', 'Shang Hai']
    assert_equal(0.0000, round(cos.distance(s[0], s[0]), 4))
    assert_equal(1.0000, round(cos.similarity(s[0], s[0]), 4))
    assert_equal(1.0000, round(cos.distance(s[0], s[1]), 4))
    assert_equal(0.0000, round(cos.similarity(s[0], s[1]), 4))
    assert_equal(1.0000, round(cos.distance(s[0], s[2]), 4))
    assert_equal(0.0000, round(cos.similarity(s[0], s[2]), 4))
    assert_equal(1.0000, round(cos.distance(s[0], s[3]), 4))
    assert_equal(0.0000, round(cos.similarity(s[0], s[3]), 4))
    assert_equal(1.0000, round(cos.distance(s[0], s[4]), 4))
    assert_equal(0.0000, round(cos.similarity(s[0], s[4]), 4))
    assert_equal(0.0000, round(cos.distance(s[1], s[1]), 4))
    assert_equal(1.0000, round(cos.similarity(s[1], s[1]), 4))
    assert_equal(1.0000, round(cos.distance(s[1], s[2]), 4))
    assert_equal(0.0000, round(cos.similarity(s[1], s[2]), 4))
    assert_equal(1.0000, round(cos.distance(s[1], s[3]), 4))
    assert_equal(0.0000, round(cos.similarity(s[1], s[3]), 4))
    assert_equal(0.6985, round(cos.distance(s[1], s[4]), 4))
    assert_equal(0.3015, round(cos.similarity(s[1], s[4]), 4))
    assert_equal(0.0000, round(cos.distance(s[2], s[2]), 4))
    assert_equal(1.0000, round(cos.similarity(s[2], s[2]), 4))
    assert_equal(0.0871, round(cos.distance(s[2], s[3]), 4))
    assert_equal(0.9129, round(cos.similarity(s[2], s[3]), 4))
    assert_equal(0.1296, round(cos.distance(s[2], s[4]), 4))
    assert_equal(0.8704, round(cos.similarity(s[2], s[4]), 4))
    assert_equal(0.0000, round(cos.distance(s[3], s[3]), 4))
    assert_equal(1.0000, round(cos.similarity(s[3], s[3]), 4))
    assert_equal(0.0465, round(cos.distance(s[3], s[4]), 4))
    assert_equal(0.9535, round(cos.similarity(s[3], s[4]), 4))
    assert_equal(0.0000, round(cos.distance(s[4], s[4]), 4))
    assert_equal(1.0000, round(cos.similarity(s[4], s[4]), 4))
def test_jaccard():
    jaccard = Jaccard(1)
    s = ['', ' ', 'Shanghai', 'ShangHai', 'Shang Hai']
    assert_equal(0.0000, round(jaccard.distance(s[0], s[0]), 4))
    assert_equal(1.0000, round(jaccard.similarity(s[0], s[0]), 4))
    assert_equal(1.0000, round(jaccard.distance(s[0], s[1]), 4))
    assert_equal(0.0000, round(jaccard.similarity(s[0], s[1]), 4))
    assert_equal(1.0000, round(jaccard.distance(s[0], s[2]), 4))
    assert_equal(0.0000, round(jaccard.similarity(s[0], s[2]), 4))
    assert_equal(1.0000, round(jaccard.distance(s[0], s[3]), 4))
    assert_equal(0.0000, round(jaccard.similarity(s[0], s[3]), 4))
    assert_equal(1.0000, round(jaccard.distance(s[0], s[4]), 4))
    assert_equal(0.0000, round(jaccard.similarity(s[0], s[4]), 4))
    assert_equal(0.0000, round(jaccard.distance(s[1], s[1]), 4))
    assert_equal(1.0000, round(jaccard.similarity(s[1], s[1]), 4))
    assert_equal(1.0000, round(jaccard.distance(s[1], s[2]), 4))
    assert_equal(0.0000, round(jaccard.similarity(s[1], s[2]), 4))
    assert_equal(1.0000, round(jaccard.distance(s[1], s[3]), 4))
    assert_equal(0.0000, round(jaccard.similarity(s[1], s[3]), 4))
    assert_equal(0.8750, round(jaccard.distance(s[1], s[4]), 4))
    assert_equal(0.1250, round(jaccard.similarity(s[1], s[4]), 4))
    assert_equal(0.0000, round(jaccard.distance(s[2], s[2]), 4))
    assert_equal(1.0000, round(jaccard.similarity(s[2], s[2]), 4))
    assert_equal(0.1429, round(jaccard.distance(s[2], s[3]), 4))
    assert_equal(0.8571, round(jaccard.similarity(s[2], s[3]), 4))
    assert_equal(0.2500, round(jaccard.distance(s[2], s[4]), 4))
    assert_equal(0.7500, round(jaccard.similarity(s[2], s[4]), 4))
    assert_equal(0.0000, round(jaccard.distance(s[3], s[3]), 4))
    assert_equal(1.0000, round(jaccard.similarity(s[3], s[3]), 4))
    assert_equal(0.1250, round(jaccard.distance(s[3], s[4]), 4))
    assert_equal(0.8750, round(jaccard.similarity(s[3], s[4]), 4))
    assert_equal(0.0000, round(jaccard.distance(s[4], s[4]), 4))
    assert_equal(1.0000, round(jaccard.similarity(s[4], s[4]), 4))
def test_jarowinkler():
    a = JaroWinkler(0.7)
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 1.0)
    assert_equal(a.distance(s0, s3), 1.0)
    assert_equal(a.distance(s1, s2), 1.0)
    assert_equal(a.distance(s1, s3), 1.0)
    assert_equal(round(a.distance(s2, s3), 4), 0.0889)
    assert_equal(a.similarity(s0, s1), 1.0)
    assert_equal(a.similarity(s0, s2), 0.0)
    assert_equal(a.similarity(s0, s3), 0.0)
    assert_equal(a.similarity(s1, s2), 0.0)
    assert_equal(a.similarity(s1, s3), 0.0)
    assert_equal(round(a.similarity(s2, s3), 4), 0.9111)
def test_normalized_levenshtein():
    a = NormalizedLevenshtein()
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 1.0)
    assert_equal(a.distance(s0, s3), 1.0)
    assert_equal(a.distance(s1, s2), 1.0)
    assert_equal(a.distance(s1, s3), 1.0)
    assert_equal(round(a.distance(s2, s3), 2), 0.33)
    assert_equal(a.similarity(s0, s1), 1.0)
    assert_equal(a.similarity(s0, s2), 0.0)
    assert_equal(a.similarity(s0, s3), 0.0)
    assert_equal(a.similarity(s1, s2), 0.0)
    assert_equal(a.similarity(s1, s3), 0.0)
    assert_equal(round(a.similarity(s2, s3), 2), 0.67)
def test_optimal_string_alignment():
    a = OptimalStringAlignment()
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 0.0)
    assert_equal(a.distance(s0, s3), 0.0)
    assert_equal(a.distance(s1, s2), 0.0)
    assert_equal(a.distance(s1, s3), 0.0)
    assert_equal(round(a.distance(s2, s3), 2), 1)
def test_overlap_coefficient_0():
    sim = OverlapCoefficient(3)
    s1, s2 = "eat", "eating"
    actual = sim.distance(s1, s2)
    assert_equal(0, actual)
def test_overlap_coefficient_1():
    sim = OverlapCoefficient(3)
    s1, s2 = "eat", "eating"
    actual = sim.similarity(s1, s2)
    assert_equal(1, actual)
def test_overlap_coefficient_2():
    sim = OverlapCoefficient(3)
    s1, s2 = "eat", "eating"
    actual = sim.similarity(s1, s2)
    assert_equal(1, actual)
def test_overlap_coefficient_3():
    sim = OverlapCoefficient(2)
    s1, s2 = "car", "bar"
    assert_equal(1 / 2, sim.similarity(s1, s2))
    assert_equal(1 / 2, sim.distance(s1, s2))
def test_qgram():
    a = QGram(1)
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 2)
    assert_equal(a.distance(s0, s3), 3)
    assert_equal(a.distance(s1, s2), 2)
    assert_equal(a.distance(s1, s3), 3)
    assert_equal(a.distance(s2, s3), 1)
def test_sift4():
    s = SIFT4()
    results = [('This is the first string', 'And this is another string', 5, 11.0), ('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'Amet Lorm ispum dolor sit amet, consetetur adixxxpiscing elit.', 10, 12.0)]
    for a, b, offset, res in results:
        assert_equal(res, s.distance(a, b, offset, None))
def test_sorensen_dice():
    a = SorensenDice(2)
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(round(a.distance(s2, s3), 2), 0.33)
    assert_equal(round(a.similarity(s2, s3), 2), 0.67)
def test_weighted_levenshtein():
    a = WeightedLevenshtein(default_substitution_cost, default_insertion_cost, default_deletion_cost)
    s0 = ""
    s1 = ""
    s2 = input_shanghai
    s3 = input_shanghai_city
    assert_equal(a.distance(s0, s1), 0.0)
    assert_equal(a.distance(s0, s2), 2)
    assert_equal(a.distance(s0, s3), 3)
    assert_equal(a.distance(s1, s2), 2)
    assert_equal(a.distance(s1, s3), 3)
    assert_equal(a.distance(s2, s3), 1)
def test():
    test_levenshtein()
    test_longest_common_subsequence()
    test_metric_lcs()
    test_ngram()
    test_damerau()
    test_cosine()
    test_jaccard()
    test_jarowinkler()
    test_normalized_levenshtein()
    test_optimal_string_alignment()
    test_overlap_coefficient_0()
    test_overlap_coefficient_1()
    test_overlap_coefficient_2()
    test_overlap_coefficient_3()
    test_qgram()
    test_sift4()
    test_sorensen_dice()
    test_weighted_levenshtein()
    additional_tests()
def additional_tests():
    s = StringDistance()
    tmp = s.distance("a", "b")
    assert_equal(tmp, None)
    s = NormalizedLevenshtein()
    tmp = s.distance("a", "b")
    assert_equal(tmp, 1.0)
    s = OptimalStringAlignment()
    tmp = s.distance("a", "b")
    assert_equal(tmp, 1)
    s = NormalizedStringDistance()
    tmp = s.distance("a", "b")
    assert_equal(tmp, None)
    s = SIFT4()
    results = [('This is the first string', 'And this is another string', 5, 11.0), ('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'Amet Lorm ispum dolor sit amet, consetetur adixxxpiscing elit.', 10, 12.0)]
    options = {"maxdistance": 0}
    for a, b, offset, res in results:
        assert_equal(res, s.distance(a, b, offset, options))
    s = MetricStringDistance()
    tmp = s.distance("a", "b")
    assert_equal(tmp, None)
    s = Cosine(1)
    tmp = s.distance("a", "b")
    assert_equal(tmp, 1.0)
    s = NormalizedStringSimilarity()
    tmp = s.similarity("a", "b")
    assert_equal(tmp, None)
    s = StringSimilarity()
    tmp = s.similarity("a", "b")
    assert_equal(tmp, None)
_SPACE_PATTERN = re.compile("\\s+")
test()