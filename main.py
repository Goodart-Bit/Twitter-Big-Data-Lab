import config
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from tweepyclient import TweepyClient
import pprint

bearer_token = config.BEARER_TOKEN
tweepyClient = TweepyClient(bearer_token)

translator = Translator()

# Vader Sentiment analysis is only available in english


def translate(word, dest='en'):
    translation = translator.translate(word, dest)
    return translation.text

def format_for_csv(text):
    return text.replace(',',' ').replace("\n",' ') #Data must be cleaned for the CSV to be readed clearly 

def get_tweets_sentiment(tweet_list, data=[], columns=['id', 'tweet', 'sentimiento', 'entidad']):
    sia = SentimentIntensityAnalyzer()
    for tweet in tweet_list:
        entity = ''
        translated_text = translate(tweet.text)  #Sentiment analysis only works in english
        for context_annotation in tweet.context_annotations:
            entity = context_annotation['entity']['name']
        # SENTIMENT ONLY WORKS IN ENGLISH
        sentiment_dict = sia.polarity_scores(translated_text)
        positive = sentiment_dict["pos"]
        negative = sentiment_dict["neg"]
        bias = 'neutral'
        if (positive > negative):
            bias = 'positivo'
        elif(positive < negative):
            bias = 'negativo'
        else:
            bias = 'neutral'
        cleaned_text = format_for_csv(tweet)
        data.append([tweet.id, cleaned_text, bias, entity])
    # SENTIMENT ANALYSIS DATAFRAME
    return pd.DataFrame(data, columns=columns)


def most_popular_words(tweet_list, excluded_words, max=10):
    words_dict = {}
    for tweet in tweet_list:
        tweet_text = format_for_csv(tweet.text)
        words = tweet_text.lower().split(' ')
        for word in words:
            if word not in excluded_words and len(word) > 3:
                words_dict[word] = words_dict.get(word, 0) + 1
    desc = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)#[:max]
    sorted_words_df = pd.DataFrame.from_dict(dict(desc).items())
    sorted_words_df.columns = ['word','count']
    return sorted_words_df

def save_tweets(tweet_list, data=[], columns=['id', 'tweet', 'entidad', 'dominio']):
    for tweet in tweet_list:
        entity = ''
        domain = ''
        for context_annotation in tweet.context_annotations:
            entity = context_annotation['entity']['name']
            domain = context_annotation['domain']['name']
        cleaned_text = format_for_csv(tweet)
        data.append([tweet.id, cleaned_text, entity, domain])
        return pd.DataFrame(data, columns=columns)


#sq = "covid (azitromicina OR ivermectina OR dioxido) -is:retweet lang:es"
# 1. sq = "remedio context:131.1220701888179359745 -is:retweet"
sq2 = "context:131.1220701888179359745 -is:retweet lang:es"
sq3 = "(medicamento OR \"dioxido de cloro\" OR azitromicina OR ivermectina OR tratamiento OR remedio OR cura OR tomar) (context:131.1220701888179359745 OR context:123.1220701888179359745) -is:retweet lang:es"
sq4 = "sintomas context:123.1220701888179359745 -is:retweet lang:es"
sq5 = "vacuna (context:131.1220701888179359745 OR context:123.1220701888179359745) -is:retweet"
tweets = tweepyClient.search_tweets(sq3, 8000)
#sentiment_df = get_tweets_sentiment(tweets)
#sentiment_df.to_csv('./sentimientos_dioxido_cloro.csv')
esp_regular_exclutions = ['', 'https://t', 'contra', 'este', 'sobre', 'durante', 'más', 'está', 'ha', 'el', 'la', 'los', 'las', 'un', 'no', 'una', 'unos', 'unas', 'al', 'del', 'lo', 'le', 'y', 'e', 'o', 'u', 'de', 'a', 'en', 'que', 'es',
                          'por', 'para', 'con', 'se', 'su', 'les', 'me', 'q', 'te', 'pero', 'mi', 'ya', 'cuando', 'como', 'estoy', 'voy', 'porque', 'he', 'son', 'solo', 'tengo', 'muy', 'si', 'fue', 'síntomas', 'todos', 'mascarilla', 'personas', 'salud', '#covid19',
                          'virus', 'pacientes', 'casos', 'síntomas,', 'tienen', 'después', 'nueva','tienes', 'enfermedad', 'usar', 'días', 'sintomas', 'coronavirus', 'tiene', 'esta', 'covid,', 'caso', 'lucha', 'prueba', 'ahora', 'puede', 'clave', 'estos', 'todo', 
                          'desde', 'llamada', 'están', 'gente', 'niños','positivo', 'hasta', 'entre', 'hacer', 'hace', 'presentan', 'test', 'tener', 'pandemia', 'muchos', 'conoce', 'menos', 'años', 'noviembre', 'también', 'cómo', 'tuve', 'medidas', 'cada', '\nhttps://t',
                          'corona','capital','mejor','antes','bien','@minsa_peru','pandemia','donde','nada','esto','mucho','verdad','pues','siempre','millones','nunca','igual','mismo','país','algo','mismo','estaba','estés','atención''#covid19,','tres','meses','presentas',
                          'algunos','principales','dosis','atención','pruebas','#covid19,','fiebre,','covid?','veces','problemas','casa','negativo','presentar','tenido','covid.','cura','tratamiento','agua','decir','cáncer']
esp_key_exclutions_q4 = ['covid', 'covid-19', 'vacuna', 'vacunas', 'covid-19,','variante','síntomas.',' evitar','mismos','contagio','semana','tomar','@claudiashein','ivermectina.','medicamentos','cuenta','médicos']
eng_regular_exclutions = ['have', 'with', 'that', 'https://t', 'people', 'people', 'long', 'this', 'they', 'know', '&amp;', 'what', 'vaccine', 'just', 'even', 'very', 'your', 'were', 'symptoms,', 'like', 'been', 'because', 'still', 'from', 'would', "it's", 'mild', 'when', 'only', 'vaccinated', 'after', 'well', "don't", 'positive', 'don’t', 'some', 'think', 'testing', 'there', 'about', 'test',
                          'covid-19', 'it’s', "i've", 'home', 'tested', 'really', 'said', 'does', 'many', 'worse', 'more', 'getting', 'also', 'before', 'vaxxed', 'wear', 'mask', 'immune', 'should', 'their', 'infection', 'covid,', 'same', 'life', 'study', "\n\nin", 'sick', "didn’t", "doesn’t", 'most', 'says', 'cold', 'everyone', 'which', '@greg_price11', 'hospital', 'take', 'going', 'better', 'type', 'first', '6000']
eng_key_exclutions = ['symptoms', 'covid']
esp_total_exclutions = esp_regular_exclutions + esp_key_exclutions_q4
eng_total_exclutions = eng_regular_exclutions + eng_key_exclutions
top_words_df = most_popular_words(tweet_list=tweets, excluded_words=esp_total_exclutions,max=20)
top_words_df.to_csv('medicamentos_alternivos.csv')
