import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

# Load the IMDB dataset
data = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=88000)

# Display the first training data entry
print(train_data[0])

# Get the word index dictionary
word_index = data.get_word_index()

# Adjust the word index mapping
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<Pad>"] = 0
word_index["<Start>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

# Create reverse word index for decoding
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# Pad sequences to ensure uniform input length
train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<Pad>"], padding="post", maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=word_index["<Pad>"], padding="post", maxlen=250)

print(len(train_data), len(test_data))

# Function to decode review
def decode_review(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])

# Define the model
model = keras.Sequential([
    keras.layers.Embedding(88000, 16),
    keras.layers.GlobalAveragePooling1D(),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid")
])

# Display model summary
model.summary()

# Compile the model with the correct metrics
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Split the training data into training and validation sets
x_val = train_data[:10000]
x_train = train_data[10000:]

y_val = train_labels[:10000]
y_train = train_labels[10000:]

# Train the model
fitModel = model.fit(x_train, y_train, epochs=40, batch_size=512, validation_data=(x_val, y_val), verbose=1)

# Evaluate the model on the test data
result = model.evaluate(test_data, test_labels)

print("Test set evaluation results:")
print(result)

# Save the model in .h5 format
model.save("model.h5")

def review_encode(s):
    encoded = [1]  # Start with the <Start> token
    
    for word in s:
        encoded.append(word_index.get(word.lower(), 2))  # <UNK> token for unknown words
    
    return encoded

# Load the model
model = keras.models.load_model("model.h5")

# Define the path to the review file
file_path = "C:/Users/Jakub/Desktop/Python/TesxtovaKlasifikacia/review.txt"

# Process the review file
try:
    with open(file_path, encoding="utf-8") as f:
        for line in f.readlines():
            # Preprocess the review
            nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"", "").strip().split(" ")
            # Encode and pad the review
            encode = review_encode(nline)
            encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<Pad>"], padding="post", maxlen=250)
            # Make prediction
            predict = model.predict(encode)
            # Print results
            print("Review:")
            print(line)
            print("Encoded Review:")
            print(encode)
            print("Prediction:", predict[0][0])
except FileNotFoundError:
    print("File 'review.txt' not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")

# Make a prediction on a single test review
test_review = test_data[0]
prediction = model.predict(np.expand_dims(test_review, axis=0))

print("Review:")
print(decode_review(test_review))
print("Prediction: {:.4f}".format(prediction[0][0]))
print("Actual: {}".format(test_labels[0]))