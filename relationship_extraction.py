import os
import networkx as nx
import spacy
from pyvis.network import Network
from lib.utils.functions import *

#names of the files
book_files =  [entry for entry in os.listdir('/Books') if '.pdf' in entry]
book_files.sort()

#getting a list of directories containing the pdf files in order
book_dir = []

for filename in book_files:
  for book in os.scandir('/Books'):
    if filename == book.name:
     book_dir.append(book)

#Trimming unnecessary parts of the pdf: Acknowledgements, Author's Notes
Trim_pages =[[8,378],[8,1058],[4,1235],[13,1326],[14,1657],[14,1681],[21,1413],[17,1238]]

#creating a dictionary containing the file directories with a list of start and end trim values
Book_trim = dict.fromkeys(book_dir)
i=0
for key in Book_trim.keys():
    Book_trim[key] = Trim_pages[i]
    i+=1

print(Book_trim)
    
Pdf_convert(Book_trim)

all_books = []
for filename in book_files:
  for book in os.scandir('/data'):
    if filename.rstrip('.pdf') in book.name:
     all_books.append(book)

character_df = pd.read_csv('characters_csv')

#creating a firstname column but retaining the honorifics
character_df['Char_firstname'] = character_df['Character'].apply(
								lambda x: x.split(' ', 1)[0] if not 'Mr' in x 
								else x ) 


for book in all_books:
	#running the ner function
	book_doc = ner(book)
	#named entity per list
	sent_entity_df = get_ne_list_per_sentence(book_doc)
	##filtering out non-character entities using filter_entity function
	sent_entity_df['character_entities'] = sent_entity_df['entities'].apply(
											lambda x: filter_entity(x,character_df))
	##filtering out empty entities
	sent_entity_df_filt = sent_entity_df[sent_entity_df['character_entities'].map(len) > 0]
	#Taking only the first name of the characters
	sent_entity_df_filt['character_entities'] = sent_entity_df_filt['character_entities'].apply(
											lambda x: [item.split()[0] for item in x])
	#creating relationships
	relationships_df = pd.DataFrame(columns =['source', 'target', 'value'])
  	result_rlshp= create_relationships(sent_entity_df_filt, 5)
  	relationships_df = pd.concat([result_rlshp, relationships_df], ignore_index=True)


##Network Analysis and Visualization
#create a network graph from relationships_df
G = nx.from_pandas_edgelist(relationships_df, source='source',
                           target='target',
                           edge_attr= 'value', create_using = nx.Graph())

pos = nx.kamada_kawai_layout(G)
nx.draw(G, with_labels=True, node_color='#36f25e', edge_cmap=plt.cm.Blues, pos=pos)
plt.show()

#Visualization with Pyvis
net = Network(width='900px', height='600px', bgcolor ='#222222',
            font_color = '#abeb34')

#setting up a node size attribute using node degrees
node_degree=dict(G.degree)
nx.set_node_attributes(G, node_degree, 'size')
net.from_nx(G)
net.show('Outlander.html')

#character importance using centrality measures
degree_dict = nx.degree_centrality(G)
nx.set_node_attributes(G, degree_dict, 'degree_centrality')
betweenness_dict = nx.betweenness_centrality(G)
nx.set_node_attributes(G, betweenness_dict, 'betweenness_centrality')
closeness_dict = nx.closeness_centrality(G)
nx.set_node_attributes(G, closeness_dict, 'closeness_centrality')

#Top 10 characters plot
Centrality_plot(degree_dict, 'degree_centrality')
Centrality_plot(betweenness_dict, 'betweenness_centrality')
Centrality_plot(closeness_dict, 'closeness_centrality')