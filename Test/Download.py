'''
Created on 26/10/2018

@author: CO1012351486
'''
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from pandas import DataFrame
import tweepy
import re
import unidecode
import psycopg2



connection  = psycopg2.connect(
    host="localhost",
    database="data_science", 
    user="postgres", 
    password="root"
)


consumer_key = 'NHAvRKM84myniXPn8FnWi5UZp'
consumer_secret = 'jBOpoWC6xUI42VTg5HNWtqLRqpAKXUFInAEkEkmMT7sLCx8YrL'
access_token = '927301438207864832-o6PIyvPVkPanQyLJQIRHmMTHVWfZViw'
access_token_secret = 'otFwtI872mvQ6oX0CozWyEpEdTlmWQaDpgjOiJdZBbgiG'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


def clean(text):
    text = text.lower()
    text = unidecode.unidecode(text)
    text = re.sub('[-!"#$%&()*+,./:;<=>?@\[\\\]_`{|}~]+', '', text)
    #text = re.sub('[ ]+', '_', text)
    text.replace("\n", "")
    text.replace("  ", "")
    text.replace("\t", "")
    text.replace("\r", "")
    print('Texto con reemplazos')
    print(text)
    return text

def downloadData():
    
    cursor = connection.cursor()
    sql_twitter = 'INSERT INTO "DS_TWITTER_DATA" (user_name, user_location, user_followers_count, user_friends_count, user_time_zone, user_following, geo, coordinates, place, full_text, retweet_count, favorite_count, language, created_at, id_tweet,clean_text) VALUES ('

    ## Pendiente filtrar unicamente tweets sin retweets
    for tweet in tweepy.Cursor(api.search,q="@RevistaSemana",count=100,lang="es",since="2018-09-03", tweet_mode='extended').items():
        cleanText = clean(str(tweet.full_text))
        sql_twitter = sql_twitter +"'"+ str(tweet.user.name) + "','"+ str(tweet.user.location) + "','"+ str(tweet.user.followers_count) + "','"+ str(tweet.user.friends_count) + "','"+ str(tweet.user.time_zone) + "','"+ str(tweet.user.following) +"','"+ str(tweet.geo) + "','"+ str(tweet.coordinates) + "','" + str(tweet.place) + "','" + str(tweet.full_text) + "','"+ str(tweet.retweet_count) + "','"+ str(tweet.favorite_count) + "','"+ str(tweet.lang) + "','"+ str(tweet.created_at) + "','"+ str(tweet.id) + "','"+ cleanText +"');"
        cursor.execute(sql_twitter)
        break
    
    connection.commit()
    cursor.close()


def modeling(data,data_labels):
    spanish_stopwords = ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosostros', 'vosostras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 'serán', 'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen', 'sintiendo', 'sentido', 'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 'tenidos', 'tenidas', 'tened']
    vectorizer = CountVectorizer(
        analyzer = 'word',
        lowercase = True,
        stop_words = spanish_stopwords
        )
    nb = MultinomialNB()
            
    features = vectorizer.fit_transform(data)
    features_nd = features.toarray()
    X_train, X_test, y_train, y_test  = train_test_split(features_nd, data_labels, train_size=0.80, random_state=None)
    model = nb.fit(X_train, y_train)
     
    y_pred = model.predict(X_test)
    confusionMatrix = confusion_matrix(y_test, y_pred)
    target_names=['Positive','Negative','Neutral']
    print(confusionMatrix)
    print(classification_report(y_test, y_pred, target_names=target_names))
    print(accuracy_score(y_test, y_pred))
    return nb

def getData():
    cursor = connection.cursor()
    select = 'SELECT clean_text FROM "DS_TWITTER_DATA";'    
    cursor.execute(select)
    result = cursor.fetchall()
    
    for row in result:
        print(row[0])
    
    connection.commit()
    cursor.close()
    
def getTrainingData():
    cursor = connection.cursor()
    select = 'SELECT "Text" FROM "DS_TWITTER_TRAINING_DATA";'    
    cursor.execute(select)
    result = cursor.fetchall()
    
    for row in result:
        print(row[0])
    
    #df = DataFrame(cursor.fetchall())
    #df = pd.DataFrame(cursor.fetchall())
    #df.columns = cursor.keys()
    #print(df)
    connection.commit()
    cursor.close()    
    
def main(): 
    downloadData()
    getTrainingData()
    connection.close()
    
    
main()
    #datos['Date'] = datos.Date.str.replace(r'[a-z]+', '')