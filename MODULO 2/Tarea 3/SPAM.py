# Importación de librerías necesarias
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re
import nltk
from nltk.corpus import stopwords

# Asegúrate de que tienes los recursos necesarios de NLTK
nltk.download('stopwords')

# Configuración para mostrar todas las columnas
pd.set_option('display.max_columns', None)


            # 1.- CARGA DE DATOS:

# Carga de datos
data = pd.read_csv(r'C:\Users\Christian\Downloads\spam_assassin.csv')

# Mostrar las primeras y las últimas filas del conjunto de datos
print("="*90)
print("\n1.- CARGA DE DATOS \n")
print("="*90)
print(pd.concat([data.head(), data.tail()]))
print("="*90)


            # 2.- PROCESAMIENTO DE DATOS:

print("\n2.- PROCESAMIENTO DE DATOS \n")
print("="*90)
# Mostrar el total de correos antes del preprocesamiento
print("Total de correos antes del preprocesamiento:", len(data))

# 1. Eliminar correos electrónicos duplicados
data_despues_duplicados = len(data)
data = data.drop_duplicates()
registros_sin_duplicados = len(data)
print("Registros sin duplicados:", registros_sin_duplicados)
print("Registros eliminados (duplicados):", data_despues_duplicados - registros_sin_duplicados)

# 2. Convertir todo el texto a minúsculas
data['text'] = data['text'].str.lower()
print("Todos los textos convertidos a minúsculas.")

# 3. Eliminar caracteres especiales
original_length = data['text'].str.len().sum()  # Longitud original
data['text'] = data['text'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))
new_length = data['text'].str.len().sum()  # Longitud después de la eliminación
caracteres_eliminados = original_length - new_length
print("Se han eliminado caracteres especiales:", caracteres_eliminados)

# 4. Tokenizar el texto y eliminar stopwords
stop_words = set(stopwords.words('english'))
palabras_vacias_eliminadas = 0

def tokenizar(text):
    global palabras_vacias_eliminadas
    tokens = [word for word in text.split() if word not in stop_words]
    palabras_vacias_eliminadas += len(text.split()) - len(tokens)
    return tokens

data['text'] = data['text'].apply(tokenizar)
print("Palabras vacías eliminadas:", palabras_vacias_eliminadas)
print("Total de textos tokenizados:", len(data))
print("="*90)


            # 3.- DESARROLLO: EXTRACCION DE CARACTERISTICAS:


                # TF
print("\n3.- EXTRACCION DE CARACTERISTICAS\n")
print("TF \n")
data['text'] = data['text'].astype(str)

# Extracción de características: Frecuencia de términos (TF)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['text'])

# Crear un DataFrame con los conteos de TF
tf_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Mostrar solo el número de palabras y la matriz TF (solo la forma)
print("="*90)
print("Frecuencia de términos (TF):")
print(f"Forma de la matriz TF: {tf_df.shape}")  # Dimensiones de la matriz TF
print("="*90)

# Contar la frecuencia total de cada palabra
word_counts = tf_df.sum().sort_values(ascending=False)

# Mostrar solo las 50 palabras más frecuentes
print("Las 50 palabras más frecuentes en todo el conjunto de datos:")
print(word_counts.head(50))


                # IDF
print("\nIDF \n")
# Calcular TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(data['text'])

# Calcular IDF
idf_values = tfidf_vectorizer.idf_
idf_df = pd.DataFrame(idf_values, index=tfidf_vectorizer.get_feature_names_out(), columns=["IDF"])

# Mostrar las 50 palabras con mayor importancia según IDF
top_idf_words = idf_df.sort_values(by="IDF", ascending=True).head(50)
print("="*90)
print("Frecuencia Inversa de Documentos (IDF):")
print(top_idf_words)
print("="*90)


                # TF-IDF
print("\nTF-IDF \n")
# Calcular TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(data['text'])

# Crear un DataFrame con las palabras y sus puntuaciones de TF-IDF
tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# Calcular la suma de las puntuaciones de TF-IDF para cada palabra
tfidf_sums = tfidf_df.sum(axis=0)

# Crear un DataFrame para las puntuaciones de TF-IDF
tfidf_scores = pd.DataFrame(tfidf_sums, columns=["TF-IDF"])
tfidf_scores.index.name = "Palabra"

# Mostrar las 50 palabras con mayor puntuación de TF-IDF
top_tfidf_words = tfidf_scores.sort_values(by="TF-IDF", ascending=False).head(50)

print("="*90)
print("Frecuencia de Términos-Inversa (TF-IDF):")
print(top_tfidf_words)
print("="*90)


            # MODELO. 
                #1. Calcular la probabilidad previa de spam:
print("="*90)               
print("\n3.- MODELO.")
print("\n1. CALCULAR LA PROBABILIDAD PREVIA DE SPAM.\n")
print("="*90)
numero_correos_spam = data['target'].sum()  # Sumar la columna 'target' para obtener el número de correos spam
total_correos = len(data)  # Total de correos

# Calcular P(Spam)
P_spam = numero_correos_spam / total_correos
print(f'Número total de correos: {total_correos}')
print(f'Número de correos spam: {numero_correos_spam}')
print(f'Probabilidad previa de spam (P(Spam)): {P_spam:.4f}')
print("="*90)


                #2. Calcular la probabilidad de las características del correo electrónico dado que es spam:
print("="*90)               
print("\n2. CALCULAR LA PROBABILIDAD DE LAS CARACTERISTICAS DEL CORREO ELECTRÓNICO DADO QUE ES SPAM.\n")
# Filtrar solo los correos spam
spam_emails = data[data['target'] == 1]

# Contar la frecuencia de cada palabra en los correos spam
spam_word_counts = vectorizer.transform(spam_emails['text']).sum(axis=0)

# Convertir la matriz de frecuencias a un array
spam_word_counts = np.array(spam_word_counts).flatten()

# Calcular el total de características en correos spam
total_caracteristicas_spam = spam_word_counts.sum()

# Calcular P(Caracteristicas|Spam)
P_caracteristicas_spam = spam_word_counts / total_caracteristicas_spam

# Crear un DataFrame para facilitar la visualización
features_df = pd.DataFrame({
    'word': vectorizer.get_feature_names_out(),
    'probability': P_caracteristicas_spam
})

# Filtrar y ordenar las 50 palabras con mayor probabilidad
top_50_words = features_df.sort_values(by='probability', ascending=False).head(50)

# Imprimir resultados
print("="*90)
print(f'Total de características en correos spam: {total_caracteristicas_spam}')
print('40 palabras con mayor probabilidad de ser spam (P(Caracteristicas|Spam)):')
print(top_50_words)
print("="*90)


                #3. Calcular la probabilidad de las caracteristicas del correo electronico dado que no es spam:
print("="*90)               
print("\n3. CALCULAR LA PROBABILIDAD DE LAS CARACTERISTICAS DEL CORREO ELECTRÓNICO  DADO QUE NO ES SPAM.\n")
# Filtrar solo los correos no spam
no_spam_emails = data[data['target'] == 0]

# Contar la frecuencia de cada palabra en los correos no spam
no_spam_word_counts = vectorizer.transform(no_spam_emails['text']).sum(axis=0)

# Convertir la matriz de frecuencias a un array
no_spam_word_counts = np.array(no_spam_word_counts).flatten()

# Calcular el total de características en correos no spam
total_caracteristicas_no_spam = no_spam_word_counts.sum()

# Calcular P(Caracteristicas|NoSpam)
P_caracteristicas_no_spam = no_spam_word_counts / total_caracteristicas_no_spam

# Crear un DataFrame para facilitar la visualización
no_spam_features_df = pd.DataFrame({
    'word': vectorizer.get_feature_names_out(),
    'probability': P_caracteristicas_no_spam
})

# Filtrar y ordenar las 50 palabras con mayor probabilidad
top_50_no_spam_words = no_spam_features_df.sort_values(by='probability', ascending=False).head(50)

# Imprimir resultados
print("="*90)
print(f'Total de características en correos no spam: {total_caracteristicas_no_spam}')
print('40 palabras con mayor probabilidad de ser no spam (P(Caracteristicas|NoSpam)):')
print(top_50_no_spam_words)
print("="*90)


                #4. Calcular la probabilidad posterior de que el correo electronico sea spam:
print("="*90)
print("\n4. CALCULAR LA PROBABILIDAD POSTERIOR DE QUE EL CORREO ELECTRÓNICO SEA SPAM\n")
# Calcular la probabilidad previa de no spam (P(NoSpam))
P_no_spam = len(data[data['target'] == 0]) / len(data)

# Inicializar un array para almacenar las probabilidades
P_spam_caracteristicas = np.zeros(vectorizer.get_feature_names_out().shape[0])

# Calcular P(Spam|Características) para cada característica
for i in range(len(P_spam_caracteristicas)):
    P_spam_caracteristicas[i] = (P_spam * P_caracteristicas_spam[i]) / (
        P_spam * P_caracteristicas_spam[i] + P_no_spam * P_caracteristicas_no_spam[i]
    )

# Crear un DataFrame para visualizar las probabilidades
spam_probabilities_df = pd.DataFrame({
    'word': vectorizer.get_feature_names_out(),
    'P(Spam|Caracteristicas)': P_spam_caracteristicas
})

# Filtrar y ordenar las 20 palabras con mayor probabilidad posterior
top_50_spam_probabilities = spam_probabilities_df.sort_values(by='P(Spam|Caracteristicas)', ascending=False).head(50)

# Imprimir resultados
print("="*90)
print('50 palabras con mayor probabilidad de ser spam (P(Spam|Características)):')
print(top_50_spam_probabilities)
print("="*90)


                #5. Clasificación.
print("\n5. CLASIFICACION. UN CORREO ELECTRÓNICO SE CLASIFICARÁ COMO SPAM SI.\n")
# Calcular P(Spam|Características)
P_spam_caracteristicas = X @ P_caracteristicas_spam.T
P_spam_caracteristicas = P_spam_caracteristicas.flatten()

# Clasificación: 1 para Spam, 0 para No Spam
clasificaciones = np.where(P_spam_caracteristicas > 0.5, 1, 0)

# Mostrar las clasificaciones
print("="*90)
print('Clasificaciones:', clasificaciones)
print("="*90)

                #6. Evaluación
print("\n6. EVALUACIÓN.\n")
# Evaluación
precision = np.sum(clasificaciones == data["target"]) / len(clasificaciones)
recuperacion = np.sum(clasificaciones == "Spam") / data["target"].sum()

# Mostrar resultados
print("="*90)
print(f'Precisión: {precision:.2f}')
print(f'Recuperación: {recuperacion:.2f}')
print("="*90)