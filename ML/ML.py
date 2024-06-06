from flask import Flask, request, jsonify, redirect, url_for, render_template
import joblib
import pandas as pd
from nltk.tokenize import word_tokenize #divir texto en palabras o tokens
from nltk.corpus import stopwords #palabras vacias ("el", "la", "y", "en", etc)
from nltk.stem import PorterStemmer #algoritmo de lematizacion de palabras (lemas)
from sklearn.feature_extraction.text import TfidfVectorizer
from statistics import mode
import snowballstemmer
from spellchecker import SpellChecker

app = Flask(__name__)

# Middleware para manejar las cabeceras CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/", methods=["GET", "POST"])
def recibir_respuestas():
    if request.method == "POST":

        respuestas = request.get_json() # "respuestas" es un diccionario

        lista_tuplas = list(respuestas.items())  #keys() o values()
        print(lista_tuplas)
        df = pd.DataFrame(lista_tuplas)
        df.columns = ['Nombre', 'Respuesta']
        df.to_excel('respuestas_formulario.xlsx', index=False)

        data = pd.read_excel("respuestas_formulario.xlsx")
        data.dropna(inplace=True)
        spell = SpellChecker(language='es')
        stop_words = set(stopwords.words("es"))
        stemmer = snowballstemmer.stemmer('spanish')

        def correct_spelling(text):
            words = text.split()
            corrected_words = [spell.correction(word) for word in words]
            print(corrected_words)
            return " ".join(corrected_words)
        
        def preprocess_text(text):
            text = correct_spelling(text)
            tokens = word_tokenize(text.lower()) #se convierte todo a minusculas y se divide en tokens
            tokens = [token for token in tokens if token not in stop_words] #si un token es una palabra vacia, se elimina
            tokens = [stemmer.stemWord(token) for token in tokens] #a cada token no eliminado se aplica stemmer
            return " ".join(tokens) #tokens procesados en una cadena de texto separados por un espacio en blanco
        
        data["Respuesta"] = data["Respuesta"].apply(preprocess_text)

        tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
        X = tfidf_vectorizer.transform(data["Respuesta"])

        clasificador_cargado = joblib.load('clasificador_entrenado.pkl')
        y_pred = clasificador_cargado.predict(X)
        print(y_pred) #recordar que auditivo:0 kinestésico:1 visual:2

        predicciones_df = pd.Series(y_pred)
        porcentajes = predicciones_df.value_counts(normalize=True) * 100

        # Crear un diccionario para mapear las clases a sus nombres correspondientes
        clase_nombres = {0: "Auditivo", 1: "Kinestésico", 2: "Visual"}

        # Formatear la salida
        resultado = [f"{clase_nombres[clase]}: {porcentaje:.0f}%" for clase, porcentaje in porcentajes.items()]
        resultado = str(" ".join(resultado))

        clase_mas_alta = porcentajes.idxmax()
        porcentaje_mas_alto = porcentajes.max()
        nombre_clase_mas_alta = clase_nombres[clase_mas_alta]
        mas_alto = str(f"{nombre_clase_mas_alta}: {porcentaje_mas_alto:.0f}%")
        print(mas_alto)
        resultado = str(resultado.replace(mas_alto,"").strip())
        resultado = str(f"{mas_alto}, mientras que tus equivalencias con el resto de los estilos son {resultado}")
        print(resultado)

        #######
        return resultado
    
    
    else:
        return "ML Funcionando!"

if __name__ == "__main__":
    app.run(port=5002)
