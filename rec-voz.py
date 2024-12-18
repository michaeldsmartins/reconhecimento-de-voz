!apt-get update
!apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxss1 libxcomposite1 libasound2 libxrandr2
!pip install selenium gtts SpeechRecognition
!apt-get install -y chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

import speech_recognition as sr
from google.colab import files
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from gtts import gTTS
import time
import os
from IPython.display import Audio, display

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Modo invisível
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def recognize_uploaded_audio():
    uploaded_file = files.upload()
    for file_name in uploaded_file.keys():
        print(f"Reconhecendo o arquivo de áudio: {file_name}")
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(file_name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="pt-BR")
                print(f"Texto reconhecido: {text}")
                return text
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento de fala: {e}")
    return None

# Função para realizar a busca no Google usando Selenium
def google_search(query):
    print("Pesquisando no Google...")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    time.sleep(2)
    
   
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3) 
    
    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    search_results = [result.text for result in results[:3]]
    
    driver.quit()
    return search_results

def text_to_speech(text):
    tts = gTTS(text=text, lang='pt-br')
    tts.save("response.mp3")
    display(Audio("response.mp3", autoplay=True))


def main():
    print("Faça upload de um arquivo de áudio...")
    spoken_text = recognize_uploaded_audio()
    
    if spoken_text:
        search_results = google_search(spoken_text) 
        if search_results:
            response = f"Os primeiros resultados são: {search_results[0]}, {search_results[1]} e {search_results[2]}."
            print(response)
            text_to_speech(response)  
        else:
            print("Nenhum resultado encontrado.")
            text_to_speech("Nenhum resultado encontrado.")
    else:
        print("Nenhum texto foi reconhecido.")


main()
