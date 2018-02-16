# SpellingCorrections
<b> Aim:</b>
To detect incorrect words and use one or more models to find suitable corrections for incorrect words

### main 
<b>Tasks:</b> <br />
[1] Coordinates the creation of the word dictionary <br />
[2] Creates training and test sets <br />
[3] Executes training and builds up all the models <br />
[4] Compares performance of all models on the test set <br />

### Noisy Channel Model
Contains all the functions for training according to the [Kernighan, Church, Gale](https://dl.acm.org/citation.cfm?id=997975) probabilistic Noisy Channel

### Unsupervised Rules Model
Contains all the functions for training according to Unsupervised rules in  [Soo and Frieder](http://ir.cs.georgetown.edu/downloads/jsoo-jasist.pdf)

### N gram characters Model
Contains all the functions for training according to the Ngram model

### UnsupervisedNgram Model
(Combination of Unsupervised Rules and N gram characters)

## How to run?
python3 main.py
