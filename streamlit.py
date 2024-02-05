import streamlit as st
import joblib
from transformers import BertTokenizer, BertModel
import torch

# Function to classify the text
def classify_text(text):
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    bert_model = BertModel.from_pretrained('bert-base-multilingual-cased')
    tokens = bert_tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = bert_model(**tokens)
    embeddings = model_output['last_hidden_state'].mean(dim=1).squeeze().numpy()
    input_embedding = embeddings.reshape(1, -1)  

    binary_model=joblib.load('decision_tree_model.joblib')
    result= binary_model.predict(input_embedding)
    return result

# Function to classify offensive comments into subcategories
def classify_offensive(text):
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    bert_model = BertModel.from_pretrained('bert-base-multilingual-cased')
    tokens = bert_tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = bert_model(**tokens)
    embeddings = model_output['last_hidden_state'].mean(dim=1).squeeze().numpy()
    input_embedding = embeddings.reshape(1, -1)  

    multi_model=joblib.load('decision_model.joblib')
    res=multi_model.predict(input_embedding)
    return res

# Streamlit app
def main():
    st.title("Comment Classification App")

    # Text boxes for user input
    text_input_1 = st.text_area("Enter comment:", height=100)

    # Classification on button click
    if st.button("Submit"):
        if text_input_1:
            classification = classify_text(text_input_1)
            if classification == 1:
                st.write("The comment is offensive")
            else:
                st.write("The comment is not offensive")
        if classification==1:         
            multimodel_classification=classify_offensive(text_input_1)    
            if multimodel_classification == 0:
                st.write("The comment is offensive targeting a group")
            elif multimodel_classification == 1:
                st.write("The comment is offensive targeting an individual")
            else:
                st.write("The comment is offensive untargeted")
                



if __name__ == "__main__":
    main()                
                  
