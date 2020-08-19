This project is called interJournal, an interactive journal for tkinter.
It is an interactive journal run in Tkinter where you can, essentially, design your own journal (like a bullet journal),
or use preset features that you can fill in (like a planner). You can insert text boxes and text, insert preset designs,
insert images, draw in the journal, and analyze your writing to see overused words, most common words, 
and sentimentality of the words. You can also automatically sort tasks/notes you’ve entered into categories
using natural language processing.

To run the project, run the file called journalMainTP. Make sure the files pageTP, sideMenuTP, optionsTP, 
textboxEntryTP, imageTP, saveTP, and nltkTP are all in the same folder as journalMainTP, or else the program will not
run correctly.

Libraries that need to be installed:
-nltk	(read note below)
-PIL
-matplotlib
-numpy

When installing nltk using pip install, follow these directions:
>>> pip install nltk
>>> import nltk
>>> nltk.download()
This should open up the NLTK Downloader. You should only need to download "book" but if you have space,
you should download "all."

Libraries that should already be included with pyzo and should not need to be installed:
-tkinter
-string
-datetime


There are no shortcuts, but if you would like to test the analyze button, here is some text
you can copy paste easily into your journal: 

Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. They were the last people you'd expect to be involved in anything strange or mysterious, because they just didn't hold with such nonsense. 

Mr. Dursley was the director of a firm called Grunnings, which made drills. He was a big, beefy man with hardly any neck, although he did have a very large mustache. Mrs. Dursley was thin and blonde and had nearly twice the usual amount of neck, which came in very useful as she spent so much of her time craning over garden fences, spying on the neighbors. The Dursleys had a small son called Dudley and in their opinion there was no finer boy anywhere. 

The Dursleys had everything they wanted, but they also had a secret, and their greatest fear was that somebody would discover it. They didn't think they could bear it if anyone found out about the Potters. Mrs. Potter was Mrs. Dursley's sister, but they hadn't met for several years; in fact, Mrs. Dursley pretended she didn't have a sister, because her sister and her good-for-nothing husband were as unDursleyish as it was possible to be. The Dursleys shuddered to think what the neighbors would say if the Potters arrived in the street. The Dursleys knew that the Potters had a small son, too, but they had never even seen him. This boy was another good reason for keeping the Potters away; they didn't want Dudley mixing with a child like that. 

When Mr. and Mrs. Dursley woke up on the dull, gray Tuesday our story starts, there was nothing about the cloudy sky outside to suggest that strange and mysterious things would soon be happening all over the country. Mr. Dursley hummed as he picked out his most boring tie for work, and Mrs. Dursley gossiped away happily as she wrestled a screaming Dudley into his high chair. 

None of them noticed a large, tawny owl flutter past the window. 