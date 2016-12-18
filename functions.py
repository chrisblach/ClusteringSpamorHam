import re
from nltk.corpus import stopwords
from stemming.porter2 import stem as st
import math

def text_to_words( raw_review , remove_stop=False, stem=False):

    if stem is False:
        raw_review = raw_review.decode('utf8')
        text = re.sub(r"(?:\@|'|https?\://)\S+", "", raw_review)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub('\t', '', text)
        text = re.sub('\n', '', text)
        text = re.sub("\d+", "", text)

        lower_case = text.lower()
        words = lower_case.split()
        if remove_stop:

            stops = set(stopwords.words("english"))
            meaningful_words = [w for w in words if not w in stops]
            meaningful_words = [w for w in meaningful_words if len(w) > 2]
            return (" ".join(meaningful_words))
        else:
            words = [w for w in words if len(w) > 2]
            return (words)
    else:
        text = re.sub(r"(?:\@|'|https?\://)\S+", "", raw_review)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub('\t', '', text)
        text = re.sub('\n', '', text)
        text = re.sub("\d+", "", text)

        lower_case = text.lower()
        words = lower_case.split()
        if remove_stop:

            stops = set(stopwords.words("english"))
            meaningful_words = [w for w in words if not w in stops]
            meaningful_words = [w for w in meaningful_words if len(w) > 2]
            count = 0
            for sw in meaningful_words:
               meaningful_words[count] =  st(sw)
               count += 1
            return (" ".join(meaningful_words))
        else:
            words = [w for w in words if len(w) > 2]
            return (words)

def stringToBool (boolString):
    if "False" in boolString:
        return False
    elif "True" in boolString:
        return True
def stringToFloat (floatString):
    try:
        floater = float(floatString)
        floatertemp = math.ceil(floater * 10000) / 10000
        return float(floatertemp)
    except ValueError:
        return int (floatString)