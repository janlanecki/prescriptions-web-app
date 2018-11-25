from ..website.models import *
import numpy as np


def get_classes():
    refunds = Refund.objects.all()
    print(str(refunds.get(pk=1)))

    classess_to_vec = {}
    n = len(refunds)
    i = 0
    for r in refunds:
        vec = np.zeros()
        vec[i] = 1
        classess_to_vec[r] = vec
        i += 1

    return classess_to_vec


def analyze_text(desc):
    words = {}

    for w in desc:
        w = w.lower()
        if w in desc:
            words[w] += 1
        else:
            words[w] = 0

    for k in words:
        if len(k) <= 4:
            words.pop('key', None)

    return words
