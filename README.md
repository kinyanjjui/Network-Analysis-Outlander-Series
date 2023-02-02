### Network Character Analysis Using Named Entity Recognition
/comm_detection.png
This project analyses all the characters of 'The Outlander' book series, containing eight titles, by Diana Gabaldon using named entity recognition from the spaCy library for NLP. The main steps utilized in this project are as follows:

i. Character Scraping From WikiWebsite
The character names for each book in the series were obtained using the Selenium library and minimal cleaning. The distribution of name occurences across the titles was also visualized.

ii. Book Conversion to Text format
Converting the PDF book files into a txt files for input into the spaCy language model.

iii. Named Entity Recognition
Loaded the language model and carried out NER for each book, extracting the character name entities in each sentence.

iv. Obtaining Relationships
Using a 5 sentence window, we extracted realtionships for all the characters appearing within this window as source and target pairs, assigning each pair a unit value.

v. Network Analysis and Visualization
Using the NetworkX library, the extracted relationships were used to map network graphs, which we further used to determine the most important characters using various centrality measures. We also used Pyvis visualization library to render the network graphs as html output.
