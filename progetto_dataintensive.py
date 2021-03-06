# -*- coding: utf-8 -*-
"""Progetto_DataIntensive.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L_CdtG_TJsmXr7kRNAFERx3RrmobihWB

# **Determinare la potabilità dell'acqua in base alla sua confrmazione**

**Programmazione di Applicazioni Data Intensive**

Laurea in Ingegneria e Scienze informatiche

DISI - Università di Bologna campus di Cesena

Milandri Nicola

### DESCRIZIONE DEL PROBLEMA E ANALISI ESPLORATIVA

Si deve realizzare un modello che sia in grado di classificare diversi tipi di acqua, in base alle loro conformazioni per determinare se siano potabili o meno
"""

pip install seaborn

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import sklearn
import os
# %matplotlib inline

"""### **Caricamento dei dati e preprocessing**

Andiamo a scaricare i dati necessari ad addestrare i nostri modelli
"""

file_zip_name = "potability.zip"
file_csv_name = "water_potability.csv"

if not os.path.exists(file_zip_name):
    from urllib.request import urlretrieve
    urlretrieve("https://github.com/Chiefmilo/-progetto-data-intensive/raw/main/potability.zip", file_zip_name)
    from zipfile import ZipFile

!unzip "potability.zip"

data_raw = pd.read_csv(file_csv_name)

data_raw.head()

"""Di seguito sono riportate le informazioni riguardo ai dati, le features, le dimensioni in memoria e le varie istanze non nulle

"""

data_raw.info(memory_usage="deep")

"""**bold text**### **Descrizione delle feature**

Il DataFrame creato presenta le seguenti feature:


-  **Ph:** ph dell'acqua
-   **Hardness:** durezza dell'acqua, valore che esprime il contenuto totale di ioni di calcio e magnesio e di eventuali metalli pesanti.
-   **Solids:** solidi dissolti totalmente in ppm(parts per milion)
-   **CHloramines:** quantità di cloroammine presenti in ppm
-   **Sulfate:** quantità di solfati dissolti in mg/l(milligram/liter)
-   **Conductivity:** conduttività elettrica dell'acqua in  μS/cm
-   **Organic_Carbon:** quantità di carbonio organico in ppm
-   **Trihalamethanes:**quantità di Trilometani in μg/l
-   **Turbidity:**Misure della proprietà di emissione luminosa dell'acqua in NTU
-   **Potability:**indica se l'acqua è potabile o meno
  - 0 = non potabile
  - 1 = potabile

  














>

### Analisi generale dei dati

Studiamo le caratteristiche dei dati in nostro possesso in modo da poter comprendere al meglio le caratteristiche del dominio applicativo

Diverse sono le colonne che presentano valori nan al loro interno, non essendo valori deducibili tramite i dati delle altre features decidiamo di eliminare le righe contenenti valori nan
"""

data_raw.describe()

"""Dal grafico si può notare come le acque potabili presentino un più alto valore delle sue componenti rispetto a quelle non potabili, facendo risultare le non potabili più numerose rispetto alle potabili, si può notare meglio tramite il grafico delle acque potabili e non."""

data_raw.Potability.value_counts().plot.pie(autopct="%.1f%%");

"""Dal grafico possiamo notare come la maggior parte delle acque siano non potabili

Di seguito andremo a presentare le altre variabili presenti nel dataframe per andare ad analizzare la loro distibuzione
"""

plt.figure(figsize=(30, 20));
for n, value in enumerate(["ph", "Hardness", "Solids", "Chloramines",
                           "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"], start=1):
  data_raw[value].plot.hist(ax=plt.subplot(4,3,n), bins=30);
  plt.subplot(4, 3, n).set_title(value);

"""Dagli istogrammi rappresentati notiamo con le features presentino alte frequenze nei valori medi"""

plt.figure(figsize=(16,35))
data_raw.boxplot(ax=plt.subplot(6,2,1), column="ph", by="Potability", showmeans=True)
data_raw.boxplot(ax=plt.subplot(6,2,2), column="Organic_carbon", by="Potability", showmeans=True)

"""*   **pH:**Possiamo notare come, a livello di ph, il grafico nella parte delle acque potabibili, presenti una maggiore densità dei valori sopra ad un valore di 10, mentre per le acque non potabili presenta una maggiore densità di valori a livelli di ph inferiori a circa 3.
*   **Organic_carbon:** Dal grafico si può notare come nella maggior parte dei casi le acque potabili sono acque che presentano un basso valore di Carbonio organico nella sua composizione.

Con una operazione di pivoting possiamo osservare meglio le varie caratteristiche in base alla variabile da predire
"""

data_raw.pivot(columns="Potability")

"""Ora andremo a mostrare i grafici relativi ai valori più incisivi del dataframe pivotato"""

data_raw.pivot(columns="Potability")["ph"].plot.hist(bins=20, stacked=True);

data_raw.pivot(columns="Potability")["Turbidity"].plot.hist(bins=20, stacked=True);

"""Le normative sulla potabilità dell'acqua destinata al consumo umano stabiliscono che il valore del ph deve dell'acqua erogata da un pubblico acquedotto sia compresa tra 6.5 e 9.5, e possiamo notare come sia la fascia con la frequenza media più alta.
Per quanto riguarda la torbidità dell'acqua si potrebbero trovare tipi di acqua potabili fino a 20 NTU, ma stando alle raccomandazioni OMS il livello massimo di torbidità non dovrebbe sforare i 5 NTU, dal grafico possiamo notare come la stragrande maggioranza dell'acqua potabile presenti un livello di torbidità di circa 5 o inferiore.

Andiamo a visualizzare i valori medi delle feature in correalzione alla potabilità
"""

data_by_potability = data_raw.groupby("Potability")
data_by_potability.mean()

"""Per andare a visualizzare se le variabili sono in correlazione fra loro andiamo a calcolare la variabile di Pearson, questa variabile ci permette di capire qtramite il suo valore quanto due feature siano in correlazione fra loro, tanto più il valore si avvicinerà ad 1 tanto più saranno correlate"""

ph = data_raw["ph"]
Chloramines = data_raw["Chloramines"]
Hardness = data_raw["Hardness"]
Solids = data_raw["Solids"]
Sulfate = data_raw["Sulfate"]
Conductivity = data_raw["Conductivity"]
Organic_carbon = data_raw["Organic_carbon"]
Trihalomethanes= data_raw["Trihalomethanes"]
Turbidity = data_raw["Turbidity"]

np.mean((ph-ph.mean()) * (Sulfate-Sulfate.mean())) / (ph.std() * Sulfate.std())

np.mean((ph-ph.mean()) * (Chloramines-Chloramines.mean())) / (ph.std() * Chloramines.std())

np.mean((Trihalomethanes-Trihalomethanes.mean()) * (Chloramines-Chloramines.mean())) / (Trihalomethanes.std() * Chloramines.std())

np.mean((Trihalomethanes-Trihalomethanes.mean()) * (Turbidity-Turbidity.mean())) / (Trihalomethanes.std() * Turbidity.std())

"""Dai dati ottenuti e da altre prove fatte possiamo giungere alla conclusione che le feature non siano correlate fra di loro, il valore più alto infatti non raggiunge neanche lo 0,1

### **Normalizzazione**

Il passaggio successivo sarà quello della standardizzazione/normalizzazione dei dati

Dai dati in nostro possesso notiamo che le scale dei valori presentano valori numerici molto diversi fra loro, tramite la normalizzazione andiamo a rendere questi valori più simili fra loro rendendoli così più facili da confrontare

Di seguito verrà presentato un esempio che permetta di capire perchè sia necessaria, in questo caso, la normalizzazione dei dati.
"""

data_raw[["ph", "Solids"]]

scores = {}
f1_scores = {}
precision = {}
recall = {}
models = {}
confusion_matrice = {}

"""Prima di attuare il processi di Normalizzazione andremo ad utilizzare il metodo Hold-Out che ci permetterà di suddividere i dati che serviranno poi per l'addestramento dei modelli"""

import warnings
warnings.filterwarnings('ignore')

from sklearn.metrics import f1_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import BorderlineSMOTE
from imblearn.over_sampling import SMOTE
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
import math
from sklearn import tree
import graphviz
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import confusion_matrix

"""Andiamo a visualizzare i valori nan presenti in ciascuna delle colonne del DataFrame"""

data_raw.shape[0]-data_raw.count()

"""Notiamo che nelle colonne relative al ph, ai solfati disciolti e in quella relativa alla quantità di trilometani si trovano diversi valori nulli.

Procediamo elimimando queste righe
"""

data_raw.dropna(inplace=True)

data_raw.shape[0]-data_raw.count()

"""Estraiamo dal Dataframe la variabile che dovremo predire, rendendo il Dataframe composto solo dalle variabili necessarie per predire quella estratta."""

y = data_raw["Potability"]
X = data_raw.drop(columns=['Potability'])

X

"""Andiamo ad utilizzare il metodo **holdout** per poter dividere i dati in validation e training set"""

X_train, X_val, y_train, y_val = \
    train_test_split(X, y, test_size=1/3, random_state=42)

mod = Pipeline([
                  ("perc", Perceptron(n_jobs=-1, random_state=42))
])

mod.fit(X_train, y_train)
print("R-squared coefficient:")
mod.score(X_val, y_val)

"""Il modello presenta un tasso di accuratezza discretamente buono, 60.1%, nonostante i dati non siano normalizzati.
Ciò è dato dal fatto che gli ordini di grandezza delle varibili all'interno del DataFrame non sono eccessivamente diversi.

Ora proviamo a standardizzare le features e vediamo come ciò incide sui nostri risultati.
"""

std_mod = Pipeline([
                      ("scaler", StandardScaler()),
                      ("perc", Perceptron(n_jobs=-1, random_state=42))
])

std_mod.fit(X_train, y_train)
print("R-squared coefficient:")
std_mod.score(X_val, y_val)

"""La Standardizzazione del modello non porta miglioramenti nei risultati.
Proviamo ad aggiungere una regolarizzazione tramite la norma L1 in modo da individuare le features più rilevanti.
"""

std_l1_mod = Pipeline([
                      ("scaler", StandardScaler()),
                      ("perc", Perceptron(penalty="l1", alpha=0.0001, n_jobs=-1, random_state=42))
])

std_l1_mod.fit(X_train, y_train)
print("R-squared coefficient:")
std_l1_mod.score(X_val, y_val)

coef = pd.DataFrame(std_l1_mod.named_steps["perc"].coef_[0], columns=["coefficients"], index=X.columns)
coef

"""Sottolineamo come la precisione dei modelli sopracitati non siano da considerare poichè all'interno del DataFrame sono presenti alcune classi sbilanciate che portano a generare un modello anch'esso sbilanciato

### **Modellizazione**

Avendo un DataFrame che presenta uno sbilanciamento delle classi ricorriamo al metodo BorderlineSMOTE, strategia di oversampling che permetterà di compensare lo sbilanciamento.
"""

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=1/3, random_state=42)

sm = BorderlineSMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)
X_train_res = pd.DataFrame(X_train_res, columns=X_train.columns)

"""Andiamo a creare delle librerie nelle quali andremo a salvare i dati ottenuti dall'analisi dei modelli"""

scores = {}
f1_scores = {}
precision = {}
recall = {}
model = {}
confusion_matrice = {}

"""Addestriamo un metodo Perceptron utilizzando GridSearch in modo da trovare i parametri più consoni al nostro scopo.

Andiamo a prendere in analisi i seguenti iperparametri:

*   **Normalizzazione delle features**
*   **Regolarizzazione del modello**
*   **Peso della regolarizzazione**
*   **Stima dell'intercetta**


"""

kfold = KFold(n_splits=5, shuffle=True, random_state=42)

perc_model = Pipeline([
    ("scaler", StandardScaler()),
    ("perc", Perceptron(n_jobs=-1, random_state=42))
])

perc_grid = {
    "scaler": [None, StandardScaler()],
    "perc__penalty": ["l2", "l1", "elasticnet"],
    "perc__alpha": np.logspace(-3, 3, 10),
    "perc__fit_intercept": [False, True]
}

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# perc_gv = GridSearchCV(perc_model, perc_grid, cv=kfold, n_jobs=-1)
# perc_gv.fit(X_train_res, y_train_res)

print("Punteggio migliore: {score}".format(score=perc_gv.score(X_val, y_val)));
print("F1 score: {score}".format(score=f1_score(y_val, perc_gv.predict(X_val), average="binary")));
print("Precision score: {score}".format(score=precision_score(y_val, perc_gv.predict(X_val))))
print("Recall score: {score}".format(score=recall_score(y_val, perc_gv.predict(X_val))))
print("Parametri migliori: {params}".format(params=perc_gv.best_params_))

scores["perc"] = perc_gv.score(X_val, y_val);
f1_scores["perc"] = f1_score(y_val, perc_gv.predict(X_val), average="binary")
precision["perc"] = precision_score(y_val, perc_gv.predict(X_val))
recall["perc"] = recall_score(y_val, perc_gv.predict(X_val))
models["perc"] = perc_gv.best_estimator_
confusion_matrice["perc"] = pd.DataFrame(confusion_matrix(y_val, perc_gv.predict(X_val)), columns= perc_gv.classes_, index=perc_gv.classes_)

"""Andiamo ad utilizzare la matrice di confusione per poter avere una migliore visualizzazione dei dati analizzati"""

confusion_matrice["perc"]

"""L'accuratezza del modello ottenuto tramite BorderlineSMOTE non è molto elevata, tramite la matrice di confusione, si può notare come il modello sia sbilanciato.

Per provare ad aggirare questo problema andiamo ad utilizzare il metodo della regressione logicstica

### **Regressione Logistica**

La regressione logistica è un modello di classificazione binaria che sfrutta il concetto di regressione lineare.

Per trovare i parametri più adatti al nostro scopo riutilizzeremo la GridSearch
"""

from sklearn.linear_model import LogisticRegression

log_modello = Pipeline ([
    ("scaler", StandardScaler()),
    ("log", LogisticRegression(solver="saga", random_state=42))
])

log_grid = {
    "scaler": [None,StandardScaler()],
    "log__penalty": ["l2", "l1"],
    "log__C": np.logspace(-3,3,10),
    "log__fit_intercept": [False, True]
}

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# log_gv = GridSearchCV(log_modello, log_grid, cv=kfold, n_jobs=-1)
# log_gv.fit(X_train_res, y_train_res)

print("Punteggio migliore: {score}".format(score=log_gv.score(X_val, y_val)));
print("F1 score: {score}".format(score=f1_score(y_val, log_gv.predict(X_val), average="binary")));
print("Precision score: {score}".format(score=precision_score(y_val, log_gv.predict(X_val))))
print("Recall score: {score}".format(score=recall_score(y_val, log_gv.predict(X_val))))
print("Parametri migliori: {params}".format(params=log_gv.best_params_))

scores["log"] = log_gv.score(X_val, y_val);
f1_scores["log"] = f1_score(y_val, log_gv.predict(X_val), average="binary")
precision["log"] = precision_score(y_val, log_gv.predict(X_val))
recall["log"] = recall_score(y_val, log_gv.predict(X_val))
models["log"] = log_gv.best_estimator_
confusion_matrice["log"] = pd.DataFrame(confusion_matrix(y_val, log_gv.predict(X_val)), columns= log_gv.classes_, index=log_gv.classes_)

confusion_matrice["log"]

"""Come la matrice di confusione ci fa notare abbiamo avuto un netto miglioramento nella corretta predizione del modello rispetto al metodo Perceptron.

Proveremo in seguito a modellare la nostra tabella tramite Support Vector Machine

### **SVM**
"""

svc_modello = Pipeline([
    ("scaler", StandardScaler()),
    ("svc", LinearSVC(dual=False, random_state=42))
])

svc_grid = {
    "scaler": [None, StandardScaler()],
    "svc__penalty": ["l2", "l1"],
    "svc__loss": ["hinge", "squared_hinge"],
    "svc__fit_intercept": [False, True],
    "svc__class_weight": [None, "balanced"],
    "svc__C": np.logspace(-3, 3, 10)
}

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# svc_gv = GridSearchCV(svc_modello, svc_grid, cv=kfold, n_jobs=-1)
# svc_gv.fit(X_train_res, y_train_res)

print("Punteggio migliore: {score}".format(score=svc_gv.score(X_val, y_val)));
print("F1 score: {score}".format(score=f1_score(y_val, svc_gv.predict(X_val), average="binary")));
print("Precision score: {score}".format(score=precision_score(y_val, svc_gv.predict(X_val))))
print("Recall score: {score}".format(score=recall_score(y_val, svc_gv.predict(X_val))))
print("Parametri migliori: {params}".format(params=svc_gv.best_params_))

scores["svc"] = svc_gv.score(X_val, y_val);
f1_scores["svc"] = f1_score(y_val, svc_gv.predict(X_val), average="binary")
precision["svc"] = precision_score(y_val, svc_gv.predict(X_val))
recall["svc"] = recall_score(y_val, svc_gv.predict(X_val))
models["svc"] = svc_gv.best_estimator_
confusion_matrice["svc"] = pd.DataFrame(confusion_matrix(y_val, svc_gv.predict(X_val)), columns= svc_gv.classes_, index=svc_gv.classes_)

confusion_matrice["svc"]

"""Analizzando il modello ottenuto tramite il metodo SVM notiamo come la precisione della predizione dei dati sia aumentata, senza però ottenere buoni risultati.

### **Albero Decisionale**

Il prossimo metodo che andremo ad utilizzare per generare il modello da analizzare sarò quello dell'Albero Decisionale, o Decision Tree.

E' una funzione di regressione dove:

*   **Ogni nodo interno rappresenta una variabile**
*   **Un arco verso un nodo figlio rappresenta un possibile valore per quella proprietà**
*   **Una foglia, il valore predetto per la classe dalle altre proprietà, che nell'albero è rappresentato dal cammino(path), dal nodo radice(root), e dal nodo foglia**
"""

from sklearn.tree import DecisionTreeClassifier

features_num = X.columns.size

dtree_mod = Pipeline ([
     ("scaler", StandardScaler()),
     ("dtree", DecisionTreeClassifier(class_weight="balanced", random_state=42))                  
])

dtree_grid = {'scaler': [None, StandardScaler()],
             'dtree__min_samples_split': range(2, 6),
             'dtree__min_samples_leaf': range(1, 6), 
             'dtree__max_depth': range(2,6),
             'dtree__max_features': range(2, features_num)}

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# dtree_gv = GridSearchCV(dtree_mod, dtree_grid, cv=kfold, n_jobs=-1)
# dtree_gv.fit(X_train_res, y_train_res)

print("Punteggio migliore: {score}".format(score=dtree_gv.score(X_val, y_val)));
print("F1 score: {score}".format(score=f1_score(y_val, dtree_gv.predict(X_val), average="binary")));
print("Precision score: {score}".format(score=precision_score(y_val, dtree_gv.predict(X_val))))
print("Recall score: {score}".format(score=recall_score(y_val, dtree_gv.predict(X_val))))
print("Parametri migliori: {params}".format(params=dtree_gv.best_params_))

scores["dtree"] = dtree_gv.score(X_val, y_val);
f1_scores["dtree"] = f1_score(y_val, dtree_gv.predict(X_val), average="binary")
precision["dtree"] = precision_score(y_val, dtree_gv.predict(X_val))
recall["dtree"] = recall_score(y_val, dtree_gv.predict(X_val))
models["dtree"] = dtree_gv.best_estimator_
confusion_matrice["dtree"] = pd.DataFrame(confusion_matrix(y_val, dtree_gv.predict(X_val)), columns=dtree_gv.classes_, index=dtree_gv.classes_)

confusion_matrice["dtree"]

"""### **Random Forest**"""

forest_mod = Pipeline([
    ("scaler", StandardScaler()),
    ("forest", RandomForestClassifier(n_jobs=-1, random_state=42))
])
forest_grid = {"scaler": [None, StandardScaler()],
             'forest__n_estimators': range(5, 10),
             'forest__min_samples_split': range(2, 5), 
             'forest__max_depth': [None] + [i for i in range(1, 3)],
             'forest__max_features': [int(math.sqrt(features_num)), features_num - 1]}

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# rforest_gv = GridSearchCV(forest_mod, forest_grid, cv=kfold, n_jobs=-1)
# rforest_gv.fit(X_train_res, y_train_res)

print("Punteggio migliore: {score}".format(score=rforest_gv.score(X_val, y_val)));
print("F1 score: {score}".format(score=f1_score(y_val, rforest_gv.predict(X_val), average="binary")));
print("Precision score: {score}".format(score=precision_score(y_val, rforest_gv.predict(X_val))))
print("Recall score: {score}".format(score=recall_score(y_val, rforest_gv.predict(X_val))))
print("Parametri migliori: {params}".format(params=rforest_gv.best_params_))

scores["forest"] = rforest_gv.score(X_val, y_val);
f1_scores["forest"] = f1_score(y_val, rforest_gv.predict(X_val), average="binary")
precision["forest"] = precision_score(y_val, rforest_gv.predict(X_val))
recall["forest"] = recall_score(y_val, rforest_gv.predict(X_val))
models["forest"] = rforest_gv.best_estimator_
confusion_matrice["forest"] = pd.DataFrame(confusion_matrix(y_val, rforest_gv.predict(X_val)), columns=rforest_gv.classes_, index=rforest_gv.classes_)

confusion_matrice["forest"]

"""Il modello della Random Forest è un'insieme di Decision Tree, come possiamo notare, in particolar modo guardando la matrice di confusione sopra riportata, è il modello che ci restituisce la miglior predizione, aumentando notevolmente il tasso di precisione rispetto al Decision Tree (risultato il miglior modello di quelli presi in analisi),

### **Valutazione dei vari modelli**
"""

print(models)

from sklearn.model_selection import cross_val_score

name_model = {
    'perc': 'Perceptron',
    'log': 'LogisticRegression',
    'svc': 'Support Vector Machines',
    'dtree': 'Decision Tree',
    'forest': 'Random Forest'
}

for model in models.values():
  print(name_model[list(model.named_steps.keys())[1]] +
        ": %0.6f di accuratezza con deviazione standard di %0.6f" % 
        (cross_val_score(models[list(model.named_steps.keys())[1]],X_val, y_val,cv=kfold).mean(), 
         cross_val_score(models[list(model.named_steps.keys())[1]],X_val, y_val,cv=kfold).std()))
  print('\n')

"""Andiamo a confrontare i vari modelli che sono stati generati durante l'analisi del DataSet.

Valutiamo i modelli attraverso il calcolo di:

*  **(R$^2$)**
*  **F1 Score**
*  **Precision**
*  **Recall score**







"""

pd.DataFrame.from_dict(scores, orient="index", columns=["R^2 Score"])

pd.DataFrame.from_dict(f1_scores, orient="index", columns=["F1 score"])

pd.DataFrame.from_dict(precision, orient="index", columns=["Precision"])

pd.DataFrame.from_dict(recall, orient="index", columns=["Recall score"])

"""Come abbiamo notato dalle matrici di confusione prese in analisi precedentemente e riproposte qui sotto, il DecisionTreeClassifier e, in particolar modo, il RandomTreeClassifier sono quelli che presentano generalmente i valori migliori."""

print("Perceptron")
print(confusion_matrice["perc"])
print("\n")
print("Logistic Regression")
print(confusion_matrice["log"])
print("\n")
print("Support Vector Machines")
print(confusion_matrice["svc"])
print("\n")
print("Decision Tree")
print(confusion_matrice["dtree"])
print("\n")
print("Random Forest")
print(confusion_matrice["forest"])

"""### **Valutazione dei modelli tramite l'utilizzo dell'Intervallo di confidenza**

In questa fase andremo a valutare l'intervallo di confidenza dei nostri modelli per vedere quale risulti il migliore fra quelli utilizzati.
"""

def confidence(acc, N, Z):
    den = (2*(N+Z**2))
    var = (Z*np.sqrt(Z**2+4*N*acc-4*N*acc**2)) / den
    a = (2*N*acc+Z**2) / den
    inf = a - var
    sup = a + var
    return (inf, sup)

def calculate_accuracy(conf_matrix):
    return np.diag(conf_matrix).sum() / conf_matrix.sum().sum()

pd.DataFrame([confidence(calculate_accuracy(confusion_matrice["perc"]), len(X_val), 1.96),
              confidence(calculate_accuracy(confusion_matrice["log"]), len(X_val), 1.96),
              confidence(calculate_accuracy(confusion_matrice["svc"]), len(X_val), 1.96),
              confidence(calculate_accuracy(confusion_matrice["dtree"]), len(X_val), 1.96),
              confidence(calculate_accuracy(confusion_matrice["forest"]), len(X_val), 1.96)],
                 index=["perceptron", "logistic reg", "SVM", "decision tree", "random forest"], columns=["inf", "sup"])

"""Come si poteva già in precedenza notare il metodo random forest risulta quello che ci ha fornito l'analisi del modello più accurata

### **Valutazione tramite il confronto con un modello casuale**

Addestriamo un modello casuale e lo valutiamo in base a come performa sui dati del DataSet preso in analisi
"""

from sklearn.dummy import DummyClassifier

random_model = DummyClassifier(strategy="uniform", random_state=42)
random_model.fit(X_train_res, y_train_res)

random_score = random_model.score(X_val, y_val)

print("Score: {score}".format(score=random_score));
print("F1 score: {score}".format(score=f1_score(y_val, random_model.predict(X_val))));
print("Precision score: {score}".format(score=precision_score(y_val, random_model.predict(X_val))))
print("Recall score: {score}".format(score=recall_score(y_val, random_model.predict(X_val))))

scores["random"] = random_model.score(X_val, y_val);
f1_scores["random"] = f1_score(y_val, random_model.predict(X_val), average="binary")
precision["random"] = precision_score(y_val, random_model.predict(X_val))
recall["random"] = recall_score(y_val, random_model.predict(X_val))

confusion_matrice["random"] = pd.DataFrame(confusion_matrix(y_val, random_model.predict(X_val)), columns=random_model.classes_, index = random_model.classes_)

confusion_matrice["random"]

"""I dati ottenuti da questo modello risultano migliori rispetto ad alcuni modelli, ma non paragonabili rispetto ad altri.

Ora andiamo a confrontare il modello ottenuto tramite un metodo casuale con qullo ottenuto tramite l'utilizzo della Random Forest.
"""

from scipy import stats

def difference_between_two_models(error1, error2, confidence):
    z_half_alfa = stats.norm.ppf(confidence)
    variance = (((1 - error1) * error1) / len(y_val)) + (((1 - error2) * error2) / len(y_val))
    d_minus = abs(error1 - error2) - z_half_alfa * (pow(variance, 0.5))
    d_plus = abs(error1 - error2) + z_half_alfa * (pow(variance, 0.5))
    print("Valore minimo: {}\nValore massimo: {}\n".format(d_minus, d_plus))

for model in models.values():
  print(name_model[list(model.named_steps.keys())[1]] + " VS Modello Random")
  print("\n")
  difference_between_two_models(1 - f1_scores[list(model.named_steps.keys())[1]], 1 - f1_scores["random"], 0.99)

"""### **Conclusioni**

Andando ad analizzare i vari valori ottenuti non mi sento molto soddisfatto dei modelli ottenuti con i metodi: Perceptron, Logistic Regression e SVM in quanto restituiscono risultati peggiori rispetto a quello di un modello creato tramite un metodo randomico.
Viceversa mi ritengo soddisfatto dal modello ottenuto con il metodi RandomTreeClassifier, presenta score di determinazione e precision buoni, migliori di tutti gli altri modelli, presentando anche ottimi valori nell'intervallodi confidenza.
"""