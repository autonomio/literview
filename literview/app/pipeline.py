import sys
sys.path.insert(0, '/home/mikko/dev/autonomio/dedomena/')
sys.path.insert(0, '/home/mikko/dev/autonomio/signs/')

def fetch_docs(keywords, n):
    
    import dedomena
    data = dedomena.apis.pubmed(keywords, n=n)
    
    return data

def preprocess_docs(data):

    data.dropna(inplace=True)
    
    data = data[data.abstract.str.len() != 0]

    return data[['journal', 'abstract']]

def create_class(data, keywords, class_label, balanced_classes=True):
    
    '''
    data | DataFrame | 
    keywords | str | One or more keywords e.g "COVID-19|coronavirus|Coronavirus"
    class_label | str | to be used for the match class
    
    '''
    
    # create the data with match
    match = data[data["abstract"].str.contains(keywords, na=False)]
    match_index = match.index
    
    # create the data with no match
    no_match = data.drop(match_index)
    
    match['label'] = class_label
    no_match['label'] = 'no-' + class_label
    
    if balanced_classes:
        no_match = no_match.sample(n=len(match))
    
    return match.append(no_match)

def remove_stopwords(data):
    
    import signs
    import numpy as np

    out = []

    for text in data['abstract']:
        out.append([text])

    docs = signs.Transform(out)
    new  = signs.Stopwords(docs.tokens())
    new = [[' '.join(i)] for i in new.docs]
    data['abstract'] = np.array(new)
    
    return data

def generate_visual(data,
                    category,
                    category_name,
                    not_category_name,
                    filename='index.html'):
    
    import spacy
    import scattertext as st

    nlp = spacy.load('en_core_web_sm')

    corpus = st.CorpusFromPandas(data, 
                                 category_col='label', 
                                 text_col='abstract',
                                 nlp=nlp).build()

    html = st.produce_scattertext_explorer(corpus,
                                           category=category,
                                           category_name=category_name,
                                           not_category_name=not_category_name,
                                           width_in_pixels=1000,
                                           metadata=data['journal'])

    return html

def run(base_keywords, n, class_keywords, class_name):

    data = fetch_docs(base_keywords, n=n)
    data = preprocess_docs(data)
    data = create_class(data, class_keywords, class_name)
    data = remove_stopwords(data)
    data = data[data.abstract.str.len() != 0]
    out = generate_visual(data, class_name, class_name, 'no-' + class_name)

    return out

    