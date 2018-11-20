Using hidden markov model (HMM) to construct a Chinese NER tagging program, and test the accuracy of our tagging method on the test set.

### Core Idea and Algorithm Description
In the first experiment of this system, we adopt the unigram.  First, we count the number of times that the word appears under different labels in the training data as maximum likelihood estimation. Then, for the x_i in the observation sequence, we find the label with the most number of times as its label in the statistical data. For the label with less occurrence in the training set, the label with the largest number of times is used as its label. For words that appear less or not appear, we will put it all in _rare_, so as to improve the accuracy of recognition. Through HMM's unigram model, we can get the labeled test set, and then compare with the original label of the test set to get the analysis results.

In project 2, we use trigram HMM to identify NER. 
The joint distribution is:

Among them * denotes the beginning of a sentence. There are four types of words: person name (PER), organization name (ORG), place name (LOC) and misused name (MISC). Normally, we label words with I-type. When two adjacent words are of the same type, we label the first word with B-type. For training data, we first use maximum likelihood estimation to get the value of parameters, and then use Veterbi search to find the tagging sequence with the greatest posterior probability. We still use the _rare_ classification to improve accuracy.

### Results
The result below is the unigram model. We could see the result is not well. 
<div align=center>
<img src="https://img-blog.csdnimg.cn/2018112010554159.jpg" width=100% height=100% div align=center/> 
</div align>
But the result for trigram is much better than unigram, results are below:
<div align=center>
<img src="https://img-blog.csdnimg.cn/20181120105557671.jpg" width=100% height=100% div align=center/> 
</div align>
Compared with the results of experiment 1, the recognition accuracy of Experiment 2 has been greatly improved, from 22% to 76%. Although the recall rate has not been greatly improved, the F1-Score has been doubled.

Specifically, the number of named entities correctly identified in Experiment 1 and Experiment 2 is basically the same, so the recall rate is similar, but experiment 1 mistook a large number of non-named entities for named entities, resulting in low recognition accuracy, which also reflects the defects of the model used in experiment 1.

In fact, the one-dimensional model used in Experiment 1 only considers the transmission probability of hidden Markov model, does not consider the transition probability between tags, ignores the correlation between the front and back tags in the tag sequence, so the experiment results are poor.

In experiment 2, a trigram hidden Markov model was used to improve the model defects in experiment 1, thus achieving a leap in recognition accuracy.

However, it was noted that the improvement of Experiment 2 did not improve the recall rate, which is the deficiency of the model and needs further study.

### Main Modules and Echnological Processes
Data Description: our original data is ner_train.dat. The data form is two columns per row. The first column is a word in a sentence, and the second column is the annotation of the word. We selected some data from training data as test data and saved it into ner_dev.key.

#### (1) count_freqs.py module:
Used for word count and transfer count.The method parameter is ner_train_rare.dat. The result is saved into ner_rare.counts.
		The results are as follows:
		a. the second mark is WORDTAG:
		13 WORDTAG I-ORG University
		This shows that in training data, University appears 13 times with I-ORG tag.
		b. the second mark is n-GRAM:
		This row data is used to record Count (y), Count (yn-1, yn) and Count (yn-2, yn-1, yn).
		For example:
		3792 2-GRAM O I-ORG
		This is used to record the number of I-ORG after the O tag: 3792
		1586 3-GRAM O I-ORG I-ORG
		The above record shows that the number of combinations of O, I-ORG and I-ORG is 1586.


#### (2) get_output_2.py 
It is our core module, get_output_1.py is simpler than 2, so we only introduce get_output_2.py.
TagRatio method: computing conditional probabilities

TagRatio first reads the previous generated ner_multiTag. counts file and traverses the rows labeled "1-GRAM" and "WORDTAG". tagRecord is used to record the number of occurrences of each tag in the unary grammar, and wordRecord is used to count the number of occurrences of words under a tag. WordCal records the conditional probability of word occurrence when a label is known: WordCal [word] [tag]

Handle method: dividing data into sentences and passing them into Viterbi functions.

Handle reads the data in the verification set ner_dev.dat and adds sentences list in the form of sentences. At the same time, two empty lists of dp_tag and dp_prob equal to sentences are formed to load tags and probabilities respectively. We pass sentences, empty dp_tag and dp_prob in corresponding positions into Viterbi method. Eventually, our sentences, and the corresponding tags and probability will be sent back as return.
Viterbi function: Viterbi algorithm is used to calculate the maximum likelihood labels of each observation sentence.

When the last word in the clause appears in dic, we first determine whether it has recursively reached the starting point. For clauses that are already at the starting point of recursion, we call the CalculateQ method. We find the largest label in all the labels directly. For clauses that are not from the starting point of recursion, we calculate the probability of combination and go down. First level recursion.

When the end of a clause is used to train words that do not appear in our expectations, we use the _rara_set to process them. The following process is exactly similar to the above process.

Run method: control process

First call tagRatio to generate DIC for recording conditional probability, and then call handle to split the test set into sentences and label and probability. Go through sentences again and write the result to the file.

#### （3）multi_tag.py
In the ner_dat, ner_countin the content in ner_train_multiTag.dat, and the example to the data to the data, the change, the name to the number, the number, the name, and the name.

#### （4）eval_ne_tagger.py 
Method for analyzing the  accuracy of experimence. The parameters are the real labels of the test set, and the labels we predict.



