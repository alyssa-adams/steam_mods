import pandas as pd
import json, os, re

from rake_nltk import Rake
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# only need to import once
#import nltk
#nltk.download('stopwords')


mods_df = pd.read_pickle("mods_df.p")
r = Rake()

# get list of descriptions
descriptions = list(mods_df['file_description'])

# loop through each description, get list of keywords
descriptions_dict = {}
for i, description in enumerate(descriptions):

    keywords = r.extract_keywords_from_text(description)
    scored_phrases = r.get_ranked_phrases_with_scores()
    descriptions_dict[i] = scored_phrases

# append as new column
mods_df['scored_phrases'] = list(descriptions_dict.values())

# get list of tags
tags = list(mods_df['tags'])

# loop through each tag, reformat
tags_dict = {}
for i, tag in enumerate(tags):
    if not tag:
        tag_list = None
    else:
        tag_list = list(map(lambda x: x['tag'], tag))
    tags_dict[i] = tag_list

# append as new column
mods_df['tags'] = list(tags_dict.values())

# save to pickle
mods_df.to_pickle('mods_df_keywords_and_tags.p')
