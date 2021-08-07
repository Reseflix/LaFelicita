import nltk,json,pickle,random,numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from unicodedata import normalize

Stemmer = nltk.stem.RSLPStemmer()
treinando, documentos, classes , palavras = list(),list(),list(),list()
ignorar = ["?","!"]
arquivo_de_intencoes = open('intents.json',encoding="utf-8").read()
intencoes = json.loads(arquivo_de_intencoes)

for intencao in intencoes['intents']:
    for padroes in intencao['patterns']:
        letras = nltk.word_tokenize(normalize('NFKD', padroes).encode('ASCII', 'ignore').decode('ASCII'),language="Portuguese")
        palavras.extend(letras)
        documentos.append((letras, intencao['tag']))
        if intencao['tag'] not in classes:
            classes.append(intencao['tag'])

palavras = sorted(list(set([Stemmer.stem(p.upper()) for p in palavras if p not in ignorar])))
classes = sorted(list(set(classes)))

pickle.dump(palavras,open("botdata\\palavras.LFT","wb"))
pickle.dump(classes,open("botdata\\classes.LFT","wb"))

saida_vazia = [0] * len(classes)
for documento in documentos:
    mochila,padrao_de_palavra, = list(),[Stemmer.stem(palavra.upper()) for palavra in documento[0]]
    for letra in palavras:
        mochila.append(1) if letra in padrao_de_palavra else mochila.append(0)

    linha_de_saida = list(saida_vazia)
    linha_de_saida[classes.index(documento[1])] = 1
    treinando.append([mochila,linha_de_saida])
random.shuffle(treinando)
treinando = np.array(treinando)
train_x = list(treinando[:,0])
train_y = list(treinando[:,1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('botdata\\LaFelicita.h5', hist)