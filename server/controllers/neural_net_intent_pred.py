import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

data = [
    {
        'intent': 'uses',
        'patterns': 
            ["What are the uses of _?", "How is _ used?", "What conditions does _ treat?", "What are the benefits of _?", "What can _ be used for?", "For what purposes is _ prescribed?", "What is _ used for?", "What conditions can _ help with?", "What are the indications for _?", "Why is _ prescribed?", "What does _ help with?", "What ailments does _ address?", "What medical conditions does _ treat?", "In what situations is _ recommended?", "What are the therapeutic uses of _?"],
    },
    {
        'intent': 'warnings',
        'patterns': 
            ["What are the warnings for _?", "What should I be aware of when taking _?", "What are the precautions for _?", "Are there any warnings for _?", "What should I know before taking _?", "What are the risks of taking _?", "What should I avoid when taking _?", "Are there any safety concerns with _?", "What are the danger signs when using _?", "What safety information should I know about _?", "What warnings come with _?", "What precautions should I take with _?", "What are the contraindications for _?", "What are the safety warnings for _?", "Are there any special warnings for _?"],
    },
    {
        'intent': 'dosage',
        'patterns':
            ["What is the dosage of _?", "How much _ should I take?", "What is the recommended dose of _?", "What dosage should be taken for _?", "How many milligrams of _ should I take?", "How often should I take _?", "Can you tell me the dosage of _?", "What is the prescribed dosage for _?", "What amount of _ is safe to take?", "How much _ is recommended?", "What is the daily dose of _?", "What is the standard dosage of _?", "How much _ should I take daily?", "What is the correct dosage of _?", "What is the appropriate dosage of _?", "What is the usual dose of _?"],
    },
    {
        'intent': 'side-effects',
        'patterns':
            ["What are the side effects of _?", "Does _ have any side effects?", "What adverse effects can _ cause?", "Are there any side effects of _?", "What should I watch out for when taking _?", "What are the common side effects of _?", "Can _ cause any side effects?", "What negative effects does _ have?", "Are there any adverse reactions to _?", "What are the potential side effects of _?", "What side effects should I expect from _?", "What are the known side effects of _?", "Does _ have any negative side effects?", "What harmful effects can _ cause?", "Are there any dangerous side effects of _?"],
    },
]

texts = []
labels = []
label_map = {item['intent']: idx for idx, item in enumerate(data)}

for item in data:
    for pattern in item['patterns']:
        texts.append(pattern)
        labels.append(label_map[item['intent']])

# Tokenize and pad sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
max_len = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Convert labels to categorical
labels = tf.keras.utils.to_categorical(labels, num_classes=len(label_map))

# Build the model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=max_len),
    LSTM(64, return_sequences=True),
    Dropout(0.5),
    LSTM(32),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(len(label_map), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(padded_sequences, labels, epochs=10, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(padded_sequences, labels)
print(f'Accuracy: {accuracy}')

# Define the input text
input_text = "What are the uses of aspirin?"

# Tokenize and pad the input text
input_seq = tokenizer.texts_to_sequences([input_text])
input_padded = pad_sequences(input_seq, maxlen=max_len, padding='post')

# Make the prediction
predictions = model.predict(input_padded)

print(predictions)

# Get the predicted class index
predicted_class_index = predictions.argmax(axis=-1)[0]

# Map the index to the intent label
intent = list(label_map.keys())[list(label_map.values()).index(predicted_class_index)]

print(f'Predicted Intent: {intent}')

