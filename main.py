
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    # TO DO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T), MED(S[1:], T[1:])))


def fast_MED(S, T, MED={}):
    # TODO -  implement memoization
    if (S, T) in MED:
        return MED[(S, T)]
    if (S == ""):
        ret = len(T)
    elif (T == ""):
        ret = len(S)
    elif (S[0] == T[0]):
        ret = fast_MED(S[1:], T[1:], MED)
    else:
        ret = 1 + min(fast_MED(S, T[1:], MED), 
                      fast_MED(S[1:], T, MED),  
                      fast_MED(S[1:], T[1:], MED))
    MED[(S, T)] = ret
    return ret


def fast_align_MED(S, T, MED={}):
    # TODO - keep track of alignment
    if (T == ""):
        ret = (S, '-' * len(S))
    elif (S == ""):
        ret = ('-' * len(T), T)
    elif (S[0] == T[0]):
        aS, aT = fast_align_MED(S[1:], T[1:], MED)
        ret = (S[0] + aS, T[0] + aT)
    else:
        minimum = min((fast_MED(S[1:], T[1:], MED)), (fast_MED(S, T[1:], MED)), (fast_MED(S[1:], T, MED)))
        if minimum == (fast_MED(S[1:], T[1:], MED)):
            aS, aT = fast_align_MED(S[1:], T[1:], MED)
            ret = (S[0] + aS, T[0] + aT)
        elif minimum == (fast_MED(S, T[1:], MED)):
            aS, aT = fast_align_MED(S, T[1:], MED)
            ret = ('-' + aS, T[0] + aT)
        else:
            aS, aT = fast_align_MED(S[1:], T, MED)
            ret = (S[0] + aS, '-' + aT)
    return ret

def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])
