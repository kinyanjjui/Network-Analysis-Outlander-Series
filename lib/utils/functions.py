import pandas as pd
import numpy as np
import os
import PyPDF2
import spacy
import networkx as nx
import matplotlib.pyplot as plt

def Pdf_convert(pdf_dict):
    """
    Function to convert a pdf file into a text file and write into the data dir 

    Params:
    pdf_dict -- a dictionary with key values of file directories and values of trim pages.
    
    Returns: None
    
    """
    for key in pdf_dict.keys():
        open_pdf = open(key.path,'rb')
        read_pdf= PyPDF2.PdfReader(open_pdf)#reading pdf using the filereader
        values = pdf_dict.get(key)
        # Page_count = read_pdf.numPages #getting number of pages in the pdf
        
        for i in range(values[0], values[1]):
            pageobj =read_pdf.pages[i]
            pagecontent = pageobj.extract_text()
            file_name = key.name.rstrip('.pdf')
            txt_file= open(f'data/{file_name}.txt',"a",encoding='utf-8')
            txt_file.writelines(pagecontent)
            txt_file.close() #closing the created text file
        
        open_pdf.close()


def ner(file_name):
    """
    Function to process text from a text file (.txt) using Spacy.
    
    Params:
    file_name -- name of a txt file as string
    
    Returns:
    a processed doc file using Spacy English language model
    
    """
    # Load spacy English languague model
    nlp = spacy.load("en_core_web_sm")
    book_text = open(file_name, 'r', encoding='utf-8').read()
    nlp.max_length = len(book_text) + 50
    book_doc = nlp(book_text)
    
    return book_doc

def get_ne_list_per_sentence(spacy_doc):
    """
    Get a list of entites per sentence of a Spacy document and store in a dataframe.
    
    Params:
    spacy_doc -- a Spacy processed document
    
    Returns:
    a dataframe containing the sentences and corresponding list of recognised named entities       in the sentences
    """
    
    sent_entity_df = []

    # Loop through sentences, store named entity list for each sentence
    for sent in spacy_doc.sents:
        entity_list = [ent.text for ent in sent.ents]
        sent_entity_df.append({"sentence": sent, "entities": entity_list})

    sent_entity_df = pd.DataFrame(sent_entity_df)
    
    return sent_entity_df


def filter_entity(ent_list, character_df):
    """
    Function to filter out non-character entities.
    
    Params:
    ent_list -- list of entities to be filtered
    character_df -- a dataframe contain characters' names and characters' first names
    
    Returns:
    a list of entities that are characters (matching by names or first names).
    
    """
    return [ent for ent in ent_list 
            if ent in list(character_df.Character) 
            or ent in list(character_df.Char_firstname)]


def create_relationships(df, window_size):
    
    """
    Create a dataframe of relationships based on the df dataframe (containing lists of chracters per sentence) and the window size of n sentences.
    
    Params:
    df -- a dataframe containing a column called character_entities with the list of chracters for each sentence of a document.
    window_size -- size of the windows (number of sentences) for creating relationships between two adjacent characters in the text.
    
    Returns:
    a relationship dataframe containing 3 columns: source, target, value.
    
    """
    
    relationships = []

    for i in range(df.index[-1]):
        end_i = min(i+5, df.index[-1])
        char_list = sum((df.loc[i: end_i].character_entities), [])

        # Remove duplicated characters that are next to each other
        char_unique = [char_list[i] for i in range(len(char_list)) 
                       if (i==0) or char_list[i] != char_list[i-1]]

        if len(char_unique) > 1:
            for idx, a in enumerate(char_unique[:-1]):
                b = char_unique[idx + 1]
                relationships.append({"source": a, "target": b})
           
    relationship_df = pd.DataFrame(relationships)
    # Sort the cases with a->b and b->a
    relationship_df = pd.DataFrame(np.sort(relationship_df.values, axis = 1), 
                                   columns = relationship_df.columns)
    relationship_df["value"] = 1
    relationship_df = relationship_df.groupby(["source","target"], 
                                              sort=False, 
                                              as_index=False).sum()
                
    return relationship_df

def Centrality_plot(cent_dict, title):
    """
    Plots the 10 most important characters acc. to centrality

    Params
    cent_dict -- a dict of the character centrality
    title -- str, name of centrality

    Returns
    A bar chart of the 10 characters
    """
    cent_df =  pd.DataFrame.from_dict(cent, orient='index', columns=[title])
    cent_df.sort_values(title, ascending=False)[0:10].plot(kind='bar')
    plt.show()
