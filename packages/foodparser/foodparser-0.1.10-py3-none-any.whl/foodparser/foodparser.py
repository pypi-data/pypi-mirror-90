# Development version
import pickle
import re
import string
import numpy as np
import pandas as pd

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, words
nltk.download('words')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

from spellchecker import SpellChecker
import pkg_resources

food_parser_data_dir = '../foodparser/data/'

class FoodParser():
    def __init__(self):
        # self.__version__ = '0.1.9'
        self.wnl = WordNetLemmatizer()
        self.spell = SpellChecker()
        return

    def read_gram_set(self, pilepath):
        # combined_df = pd.read_csv(pilepath).drop_duplicates()
        combined_df = self.test().drop_duplicates()
        all_gram_set = []
        for i in range(1, 6):
            all_gram_set.append(set(combined_df.query('gram_type == ' + str(i)).gram_key.values))
        combined_df.index = combined_df.gram_key
        food_type_dict = dict(combined_df.food_type)
        return all_gram_set, food_type_dict

    def run_setup(self, ):
        gram_mask = pickle.load(open(food_parser_data_dir + 'gram_mask.pickle', 'rb'))
        my_stop_words = pickle.load(open(food_parser_data_dir + 'my_stop_words.pickle', 'rb'))
        final_measurement = pickle.load(open(food_parser_data_dir + 'final_measurement.pickle', 'rb'))
        all_gram_set, food_type_dict = self.read_gram_set(food_parser_data_dir + 'combined_gram_set.csv')
        correction_dic = pickle.load(open(food_parser_data_dir + 'correction_dic.pickle', 'rb'))
        return gram_mask, my_stop_words, final_measurement, all_gram_set, correction_dic, food_type_dict

    def test(self):
        test_file = pkg_resources.resource_stream(__name__, "data/combined_gram_set.csv")
        tmp_df = pd.read_csv(test_file)
        return tmp_df

    def initialization(self):
        gram_mask, my_stop_words, final_measurement, all_gram_set, correction_dic, food_type_dict = self.run_setup()
        self.my_stop_words = my_stop_words
        self.final_measurement = final_measurement
        self.all_gram_set = all_gram_set
        self.gram_mask = gram_mask
        self.correction_dic = correction_dic
        self.food_type_dict = food_type_dict

        self.tmp_correction = {}
        self.spell = SpellChecker()

        # Load common stop words
        stop_words = stopwords.words('english')
        # Updated by Katherine August 23rd 2020
        stop_words.remove('out') # since pre work out is a valid beverage name
        stop_words.remove('no')
        stop_words.remove('not')
        self.stop_words = stop_words
        return

    ########## Pre-Processing ##########
    # Function for removing numbers
    def handle_numbers(self, text):
        clean_text = text
        clean_text = re.sub('[0-9]+\.[0-9]+', '' , clean_text)
        clean_text = re.sub('[0-9]+', '' , clean_text)
        clean_text = re.sub('\s\s+', ' ', clean_text)
        return clean_text

    # Function for removing punctuation
    def drop_punc(self, text):
        clean_text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        return clean_text

    # Remove normal stopwords
    def remove_stop(self, my_text):
        text_list = my_text.split()
        return ' '.join([word for word in text_list if word not in self.stop_words])

    def remove_my_stop(self, text):
        text_list = text.split()
        return ' '.join([word for word in text_list if word not in self.my_stop_words])

    def pre_processing(self, text):
        text = text.lower()
        return self.remove_my_stop(self.remove_stop(self.handle_numbers(self.drop_punc(text)))).strip()

    ########## Handle Format ##########
    def handle_front_mixing(self, sent, front_mixed_tokens):
        # print(sent)
        cleaned_tokens = []
        for t in sent.split():
            if t in front_mixed_tokens:
                number = re.findall('\d+[xX]*', t)[0]
                for t_0 in t.replace(number, number + ' ').split():
                    cleaned_tokens.append(t_0)
            else:
                cleaned_tokens.append(t)
        return ' '.join(cleaned_tokens)

    def handle_x2(self, sent, times_x_tokens):
        # print(sent)
        for t in times_x_tokens:
            sent = sent.replace(t, ' ' + t.replace(' ', '').lower() + ' ')
        return ' '.join([s for s in sent.split() if s != '']).strip()

    def clean_format(self, sent):
        return_sent = sent

        # Problem 1: 'front mixing'
        front_mixed_tokens = re.findall('\d+[^\sxX]+', sent)
        if len(front_mixed_tokens) != 0:
            return_sent = self.handle_front_mixing(return_sent, front_mixed_tokens)

        # Problem 2: 'x2', 'X2', 'X 2', 'x 2'
        times_x_tokens = re.findall('[xX]\s*?\d', return_sent)
        if len(times_x_tokens) != 0:
            return_sent = self.handle_x2(return_sent, times_x_tokens)
        return return_sent

    ########## Handle Typo ##########
    def fix_spelling(self, entry, speller_check = False):
        result = []
        for token in entry.split():
            # Check known corrections
            if token in self.correction_dic.keys():
                token_alt = self.wnl.lemmatize(self.correction_dic[token])
            else:
                if speller_check and token in self.tmp_correction.keys():
                    token_alt = self.wnl.lemmatize(self.tmp_correction[token])
                elif speller_check and token not in self.food_type_dict.keys():
                    token_alt = self.wnl.lemmatize((self.spell.correction(token)))
                    self.tmp_correction[token] = token_alt
                else:
                    token_alt = self.wnl.lemmatize(token)
            result.append(token_alt)
        return ' '.join(result)

    ########### Combine all cleaning ##########
    def handle_all_cleaning(self, entry):
        cleaned = self.pre_processing(entry)
        cleaned = self.clean_format(cleaned)
        cleaned = self.fix_spelling(cleaned)
        return cleaned

    ########## Handle Gram Matching ##########
    def parse_single_gram(self, gram_length, gram_set, gram_lst, sentence_tag):
        food_lst = []
        # print(gram_length, gram_lst, sentence_tag)
        for i in range(len(gram_lst)):
            if gram_length > 1:
                curr_word = ' '.join(gram_lst[i])
            else:
                curr_word = gram_lst[i]
            # print(curr_word, len(curr_word))
            if curr_word in gram_set and sum([t != 'Unknown' for t in sentence_tag[i: i+gram_length]]) == 0:
                # Add this founded food to the food list
                # food_counter += 1
                sentence_tag[i: i+gram_length] = str(gram_length)
                # tmp_dic['food_'+ str(food_counter)] = curr_word
                food_lst.append(curr_word)
                # print('Found:', curr_word)
        return food_lst

    def parse_single_entry(self, entry, return_sentence_tag = False):
        # Pre-processing and Cleaning
        cleaned = self.handle_all_cleaning(entry)
        # print(cleaned)

        # Create tokens and n-grams
        tokens = nltk.word_tokenize(cleaned)
        bigram = list(nltk.ngrams(tokens, 2)) if len(tokens) > 1 else None
        trigram = list(nltk.ngrams(tokens, 3)) if len(tokens) > 2 else None
        quadgram = list(nltk.ngrams(tokens, 4)) if len(tokens) > 3 else None
        pentagram = list(nltk.ngrams(tokens, 5)) if len(tokens) > 4 else None
        all_gram_lst = [tokens, bigram, trigram, quadgram, pentagram]

        # Create an array of tags
        sentence_tag = np.array(['Unknown'] * len(tokens))
        for i in range(len(sentence_tag)):
            if tokens[i] in self.final_measurement:
                sentence_tag[i] = 'MS'

        all_food = []
        food_counter = 0
        for gram_length in [5, 4, 3, 2, 1]:
            if len(tokens) < gram_length:
                continue
            tmp_food_lst = self.parse_single_gram(gram_length,
                                                self.all_gram_set[gram_length - 1],
                                                all_gram_lst[gram_length - 1],
                                                sentence_tag)
            all_food += tmp_food_lst
        # print(sentence_tag)
        if return_sentence_tag:
            return all_food, sentence_tag
        else:
            return all_food

    def parse_food(self, entry, return_sentence_tag = False):
        result = []
        unknown_tokens = []
        num_unknown = 0
        num_token = 0
        for w in entry.split(','):
            all_food, sentence_tag = self.parse_single_entry(w, return_sentence_tag)
            result += all_food
            if len(sentence_tag) > 0:
                num_unknown += sum(np.array(sentence_tag) == 'Unknown')
                num_token += len(sentence_tag)
                cleaned = nltk.word_tokenize(self.handle_all_cleaning(w))

                # Return un-catched tokens, groupped into sub-sections
                tmp_unknown = ''
                for i in range(len(sentence_tag)):
                    if sentence_tag[i] == 'Unknown':
                        # unknown_tokens.append(cleaned[i])
                        tmp_unknown += (' ' + cleaned[i])
                        if i == len(sentence_tag) - 1:
                            unknown_tokens.append(tmp_unknown)
                    elif tmp_unknown != '':
                        unknown_tokens.append(tmp_unknown)
                        tmp_unknown = ''
        for i in range(len(result)):
            if result[i] in self.gram_mask.keys():
                 result[i] = self.gram_mask[result[i]]
        if return_sentence_tag:
            return result, num_token, num_unknown, unknown_tokens
        else:
            return result

    def find_food_type(self, food):
        if food in self.food_type_dict.keys():
            return self.food_type_dict[food]
        else:
            return 'u'
