import codecs
from nltk.tokenize import sent_tokenize
import sys, random
from twython import Twython
import pytumblr
import yaml

# LETS GET THE CREDENTIALS FOR TUMBLR/twitter
with open('credentials.yaml', 'r') as f:
    config = yaml.load(f)

def get_sentences(filehandle):
    '''
    Tokenize the complete text into sentences. The markov chain
    should terminate at sentence endings.
    '''
    fh = codecs.open(filehandle,"r",encoding="utf8")
    lines = fh.readlines()
    text = "\n".join(lines)
    sent_tokenize_list = sent_tokenize(text)
    return sent_tokenize_list

def generate_markov_list(sentences,order=2,markov_dict={}):
    '''
    generate the key,value storage for the markov chain.
    requires tokenized sentences and
    1. the order of the markov chain (defaults to 2)
    2. a previous dictionary if we want to add to this
    '''
    for sentence in sentences:
        # split sentence into words, only work with it
        # if the length of sentence > the order of the chain
        s_split = sentence.split()
        if len(s_split) > order:
            counter = 0
            # iterate over the sentence to create overlapping
            # key,value pairs
            while counter < len(s_split)-order:
                key = tuple(s_split[counter:counter+order])
                value = s_split[counter+order]
                if markov_dict.has_key(key):
                    markov_dict[key].append(value)
                else:
                    markov_dict[key] = [value]
                counter += 1
    return markov_dict

def generate_single_sentence(markov_dict,charlimit=140,order=2):
    '''
    generate a single sentence from the chain, requires the max.
    sentence length and the order of the chain, otherwise things go awry
    '''
    # get the starting point, make sure it's a sentence start (uppercase)
    sentence = ""
    start = random.choice(markov_dict.keys())
    while start[0][0].isupper() == False:
        start = random.choice(markov_dict.keys())
    sentence += " ".join(start)
    # get the next fragment we want to add and thus decide the next
    # key to use for the chain
    next_frag = random.choice(markov_dict[start])
    sentence += " "+next_frag
    next_key = (start[(order*-1)+1:]) + (next_frag,)
    # now we can do this until we hit either a stop sign, the length limit
    # or encounter a missing key (maybe sentence end != .?!)
    while next_frag[-1][-1] != "." \
    and next_frag[-1][-1] != "?" \
    and next_frag[-1][-1] != "!" \
    and len(sentence) < charlimit:
        if markov_dict.has_key(next_key):
            next_frag = random.choice(markov_dict[next_key])
            sentence += " "+next_frag
            next_key = (next_key[(order*-1)+1:])+(next_frag,)
        else:
            return sentence
    return sentence

def generate_text(markov_dict,charlimit=140,order=2):
    '''
    if the sentences are short enough we can string them together to max.
    the text until hitting the character limit of e.g. twitter
    for this we try adding sentences for a while until giving up.
    '''
    text = ""
    retry_counter = 0
    # make sure the total text stays < then the limit
    while len(text) < charlimit:
        single_sentence = generate_single_sentence(markov_dict,charlimit,order)
        # is the single sentence a complete sentence? if not: ignore, try again
        if single_sentence[-1] == "." or "!" or "?":
            # does the sentence fit the text length limit?
            if (len(text) + len(single_sentence)) < charlimit:
                # is it the first sentence?
                if text == "":
                    text += single_sentence
                else:
                    text += " " + single_sentence
            retry_counter += 1
        # ok, we tried hard enough, lets stop here.
        if retry_counter > 20:
            return text
    return text

def post_tumblr(text,credentials):
    client = pytumblr.TumblrRestClient(
    credentials["tumblr"]["consumer_key"],
    credentials["tumblr"]['consumer_secret'],
    credentials["tumblr"]['token'],
    credentials["tumblr"]['token_secret'],
    )
    client.create_quote("thebloodvoyage", state="published",
    quote=text, source="Cormac R. McDarwin")

def post_twitter(text,credentials):
    twitter = Twython(
    credentials["twitter"]["consumer_key"],
    credentials["twitter"]['consumer_secret'],
    credentials["twitter"]['token'],
    credentials["twitter"]['token_secret'],
    )
    twitter.update_status(status=text)

sentences_one = get_sentences(sys.argv[1])
sentences_two = get_sentences(sys.argv[2])
markov_dict = generate_markov_list(sentences_one,2)
markov_dict = generate_markov_list(sentences_two,2,markov_dict)
text = generate_text(markov_dict,int(sys.argv[3]),2)
print text

if sys.argv[4] == "tumblr":
    post_tumblr(text,config)

if sys.argv[4] == "twitter":
    post_twitter(text,config)
