import numpy as np
import tensorflow as tf
from googleapiclient.discovery import build


# 1. Load data from file
with open('your path to file with data', 'r', encoding='utf-8') as file:
    lines = file.readlines()

questions = []
answers = []

for line in lines: 
    question, answer = line.strip().split('\t')
    questions.append(question)
    answers.append(answer)

# 2. Token text
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(questions + answers)

# Compare text on numbers (number reprezetation words)
question_sequences = tokenizer.texts_to_sequences(questions)
answer_sequences = tokenizer.texts_to_sequences(answers)

# Padding sequencion on same length
max_len = max(len(seq) for seq in question_sequences + answer_sequences)
question_sequences = tf.keras.preprocessing.sequence.pad_sequences(question_sequences, maxlen=max_len, padding='post')
answer_sequences = tf.keras.preprocessing.sequence.pad_sequences(answer_sequences, maxlen=max_len, padding='post')

# Defining input and output data
input_data = np.array(question_sequences)
output_data = np.array(answer_sequences)

# 3. Create LSTM model
vocab_size = len(tokenizer.word_index) + 1  
embedding_dim = 64
lstm_units = 64

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    tf.keras.layers.LSTM(lstm_units, return_sequences=True),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

# Compile modelu
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# 4. Train model
model.fit(input_data, np.expand_dims(output_data, axis=-1), epochs=500)

# 5. Configuration Google Custom Search API
api_key = ''
cse_id = ''

def google_search(query, api_key, cse_id, num_results=1):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        result = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
        return result.get('items', [])
    except Exception as e:
        print(f"Chyba pri vyhľadávaní: {e}")
        return []

def generate_google_response(query):
    try:
        results = google_search(query, api_key, cse_id)
        if results:
            response = results[0].get('snippet', 'No snippet available')
            link = results[0].get('link', 'No link available')
            return f"{response} Viac info: {link}"
        else:
            return "Prepáč, nepodarilo sa mi nájsť relevantnú odpoveď."
    except Exception as e:
        return f"Chyba pri generovaní odpovede: {e}"

# 6. Function to generate answers from google or file
def generate_response(user_input):
    input_seq = tokenizer.texts_to_sequences([user_input])
    input_seq = tf.keras.preprocessing.sequence.pad_sequences(input_seq, maxlen=max_len, padding='post')
    prediction = model.predict(input_seq)
    response_seq = np.argmax(prediction, axis=-1)
    
    response = ''
    for word_index in response_seq[0]:
        if word_index != 0:
            response += tokenizer.index_word.get(word_index, '') + ' '
    
    return response.strip()

def respond_with_model_or_google(user_input):
    response = generate_response(user_input)
    
    if not response or len(response) < 10:  
        response = generate_google_response(user_input)
    
    return response

# 7. Testing chatbot
while True:
    user_input = input("Ty: ")
    if user_input.lower() in ['zbohom', 'koniec', 'stop']:
        print("Bot: Zbohom! Maj sa pekne!")
        break
    
    response = respond_with_model_or_google(user_input)
    print("Bot:", response)
