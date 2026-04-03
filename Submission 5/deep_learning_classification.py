import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, clone_model
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPool1D, Dense
from tensorflow.keras.optimizers import RMSprop

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_class_weight

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import seaborn as sns

'''
CIS 6530 Assignment Submission 5
deep convolutional neural network for classifying opcodes
by Sabrina Sousa and Adam Orchard

Uses opcodes data in dataset.csv
usage: python3 deep_learning_classification.py

required packages:
os, sys, numpy, pandas, matplotlib, itertools, 
tensorflow, sklearn, seaborn, openpyxl
'''

# setup directories --------------------------------------------------

os.makedirs("results", exist_ok=True)
os.makedirs("results/cross_validation", exist_ok=True)

# clear metrics file at start
open("results/metrics.txt", "w").close()
open("results/cross_validation/fold_metrics.txt", "w").close()

# data extraction --------------------------------------------------

df = pd.read_csv("dataset.csv")

print("Dataset shape:", df.shape)
print(df["label"].value_counts())

if df.empty or df["label"].nunique() < 2:
    sys.exit("Error: not enough classes to train classifiers")

for count in df["label"].value_counts():
    if count == 1:
        sys.exit("Error: All classes in dataset must have more than 1 sample file")  

# creating one-hot vectors for opcodes --------------------------------------------------
# (3.2.1 Opcode Embedding Layer in paper)

X_raw = df["opcode"]
y_raw = df["label"]

X = pd.Series(X_raw)
y = pd.Series(y_raw)

# enumerate labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_encoded = y_encoded.astype(np.int32)

# enumerate opcodes
X_tokens = X.str.split()
opcodes_set = sorted(set(chain.from_iterable(X_tokens)))
opcode_to_id = {tok: i+1 for i, tok in enumerate(opcodes_set)}  # 0 reserved for padding
X_encoded = X_tokens.apply(lambda seq: [opcode_to_id[t] for t in seq])

lengths = X_tokens.apply(len)
print("Max sequence length:", lengths.max())
print("Min sequence length:", lengths.min())
print("Mean sequence length:", lengths.mean())
print(lengths.sort_values(ascending=False).head(10))

# pad to normalize length
MAX_LEN = 100000  # adjust up if memory issues occur

X_padded = pad_sequences(
    X_encoded.tolist(),
    padding='post',
    truncating='post',
    maxlen=MAX_LEN
)

print("X_padded shape:", X_padded.shape)
print("X_padded memory (MB):", X_padded.nbytes / 1024 / 1024)

# creating embedding layer --------------------------------------------------
# (3.2.1 Opcode Embedding Layer in paper)

opcodes_set_size = len(opcode_to_id) + 1 # add one for the 0 padding

# for 8-dimensional embedding k = 8 (as used in the paper)
k = 8

embedding_layer = Embedding(
    input_dim=opcodes_set_size,
    output_dim=k,
    embeddings_initializer='uniform',
    embeddings_regularizer=None,
    embeddings_constraint=None,
    mask_zero=False,
    weights=None,
    lora_rank=None
)
# matrix P = embedding_layer(X_padded)

# creating convolution layer --------------------------------------------------
# (3.2.2 Convolution Layers in paper)

# Conv1D is a 1D convolution layer
# the paper specifies 64 convolutional filters of length 8
# and linear activation function, relu (equation 2) for matrix A1
convolution_layer = Conv1D(
    filters=64,
    kernel_size=8,
    strides=1,
    padding='same',
    data_format=None,
    dilation_rate=1,
    groups=1,
    activation='relu',
    use_bias=True,
    kernel_initializer='glorot_uniform',
    bias_initializer='zeros',
    kernel_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    bias_constraint=None
)
# matrix A1 = convolution_layer(P)

# only one convolutional layer was used like the paper since our
# dataset was relatively small and we wanted to avoid over-fitting

# max pooling
# vector f = GlobalMaxPool1D()

# creating classification layer --------------------------------------------------
# (3.2.3 Classification Layers in paper)

# full connected hidden layer
# the paper specifies linear activation function relu (see equation 5)
# and 16 neuron units in this layer
hidden_layer = Dense(
    units=16, 
    activation='relu',
    use_bias=True,
    kernel_initializer='glorot_uniform',
    bias_initializer='zeros',
    kernel_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    bias_constraint=None,
    lora_rank=None
)

# full connected output layer
# the paper specifies soft-max classifier function
# and we get the number of classes as the units 
num_classes = df["label"].nunique()
output_layer = Dense(
    units=num_classes, 
    activation='softmax',
    use_bias=True,
    kernel_initializer='glorot_uniform',
    bias_initializer='zeros',
    kernel_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    bias_constraint=None,
    lora_rank=None
)

# creating and training the model --------------------------------------------------

model = Sequential([
    embedding_layer,   # creates matrix P
    convolution_layer, # creates matrix A1
    GlobalMaxPool1D(), # creates vector f
    hidden_layer,      # hidden layer z
    output_layer
])

# the paper specifies the RMSProp optomizer with a learning rate of 1e-2
model.compile(
    optimizer=RMSprop(learning_rate=1e-2),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)

print(f"\nTraining . . . \n")

# the paper specifies 10 epochs and a mini-batch size of 16 
# with class weights adapted to multiclass instead of binary class like the paper
class_weights = compute_class_weight(
            class_weight='balanced',
            classes=np.unique(y_encoded),
            y=y_encoded
        )
class_weight_dict = dict(enumerate(class_weights))
model.fit(X_padded, y_encoded, 
          epochs=10, 
          batch_size=16,
          class_weight=class_weight_dict
)

model.summary()

# reporting metrics --------------------------------------------------

y_pred = model.predict(X_padded)
y_pred_classes = np.argmax(y_pred, axis=1)

acc = accuracy_score(y_encoded, y_pred_classes)
report = classification_report(
    y_encoded,
    y_pred_classes,
    target_names=label_encoder.classes_
)
report_dict = classification_report(
    y_encoded,
    y_pred_classes,
    target_names=label_encoder.classes_,
    output_dict=True
)
cm = confusion_matrix(
    y_encoded, 
    y_pred_classes,
    labels=list(range(num_classes))
)

print("Accuracy:", acc)
print(report)

name = "CNN"
with open("results/metrics.txt", "a") as f:
    f.write(f"\n{'-'*50}\n")
    f.write(f"\n{name}\n")
    f.write(f"\n{'-'*50}\n")
    f.write(f"Accuracy: {acc}\n")
    f.write(report + "\n")
    f.write("Confusion Matrix:\n")
    f.write(str(cm) + "\n")

filename = f"results/confusion_matrix_{name}.png"

def plot_cm(cm, labels, title, filename):
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt="d",
                xticklabels=labels,
                yticklabels=labels)
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.savefig(filename, bbox_inches="tight")
    plt.close()

plot_cm(cm, label_encoder.classes_, f"{name}", filename)

report_df = pd.DataFrame(report_dict).transpose()
with pd.ExcelWriter("results/metrics.xlsx") as writer:
    report_df.to_excel(writer, sheet_name=f"{name}")

# cross-validation --------------------------------------------------
# 5 fold instead of paper's 10 because dataset is too small for 10
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)  

all_fold_reports = []

with pd.ExcelWriter("results/cross_validation/fold_metrics.xlsx") as writer:
    for fold, (train_idx, test_idx) in enumerate(kfold.split(X_padded, y_encoded)):
        print(f"\nFold {fold+1}/5")
        
        X_train, X_test = X_padded[train_idx], X_padded[test_idx]
        y_train, y_test = y_encoded[train_idx], y_encoded[test_idx]
        
        # clone model to reset weights each fold
        fold_model = clone_model(model)
        fold_model.compile(
            optimizer=RMSprop(learning_rate=1e-2),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        fold_class_weights = compute_class_weight(
            class_weight='balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        fold_class_weight_dict = dict(enumerate(fold_class_weights))

        fold_model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=1,  # small because dataset is tiny
                    class_weight=fold_class_weight_dict,
                    verbose=0)
        
        fold_y_pred = np.argmax(fold_model.predict(X_test), axis=1)
        
        fold_acc = accuracy_score(y_test, fold_y_pred)
        fold_report = classification_report(
            y_test, 
            fold_y_pred,
            labels=list(range(num_classes)),
            target_names=label_encoder.classes_,
            zero_division=0
        )
        fold_report_dict = classification_report(
            y_test, 
            fold_y_pred,
            labels=list(range(num_classes)),
            target_names=label_encoder.classes_,
            output_dict=True,
            zero_division=0
        )
        all_fold_reports.append(fold_report_dict)
        fold_cm = confusion_matrix(
            y_test, 
            fold_y_pred,
            labels=list(range(num_classes))
        )

        with open("results/cross_validation/fold_metrics.txt", "a") as f:
            f.write(f"\n{'-'*50}\n")
            f.write(f"\nFold {fold+1}/5\n")
            f.write(f"\n{'-'*50}\n")
            f.write(f"Accuracy: {fold_acc}\n")
            f.write(fold_report + "\n")
            f.write("Confusion Matrix:\n")
            f.write(str(fold_cm) + "\n")

        filename = f"results/cross_validation/confusion_matrix_fold-{fold+1}.png"
        plot_cm(fold_cm, label_encoder.classes_, f"Fold {fold+1}/5", filename)

        fold_report_df = pd.DataFrame(fold_report_dict).transpose()
        fold_report_df.to_excel(writer, sheet_name=f"Fold {fold+1}")

# average metrics across folds
avg_accuracy = np.mean([r['accuracy'] for r in all_fold_reports])
avg_precision = np.mean([r['macro avg']['precision'] for r in all_fold_reports])
avg_recall = np.mean([r['macro avg']['recall'] for r in all_fold_reports])
avg_f1 = np.mean([r['macro avg']['f1-score'] for r in all_fold_reports])

print(f"\nMean Accuracy:  {avg_accuracy:.2f}")
print(f"Mean Precision: {avg_precision:.2f}")
print(f"Mean Recall:    {avg_recall:.2f}")
print(f"Mean F1:        {avg_f1:.2f}")

with open("results/metrics.txt", "a") as f:
    f.write(f"\n{'-'*50}\n")
    f.write(f"\nCross-Validation (average metrics across folds)\n")
    f.write(f"\n{'-'*50}\n")
    f.write(f"Mean Accuracy:  {avg_accuracy:.2f}\n")
    f.write(f"Mean Precision: {avg_precision:.2f}\n")
    f.write(f"Mean Recall:    {avg_recall:.2f}\n")
    f.write(f"Mean F1:        {avg_f1:.2f}\n")

mean_dict = {
    'accuracy': avg_accuracy,
    'precision': avg_precision,
    'recall': avg_recall,
    'f1': avg_f1
}
mean_df = pd.DataFrame(mean_dict, index=['mean'])

with pd.ExcelWriter("results/cross_validation/fold_metrics.xlsx", mode='a', if_sheet_exists='replace') as writer:
    mean_df.to_excel(writer, sheet_name="Mean")

print("\nDone. Results saved to results/")