run generate_rare_data.py to generate ner_train_rare.dat

	generate_rare_data.py

run count_freqs.py on ner_train_rare.dat  to generate ner_train_rare.dat with tag \_rare_

	python count_freqs.py ner_train_rare.dat  ner_train_rare.dat

run get_output_1.py to get the result of the first method 

run eval_ne_tagger.py ner_dev.key output_1.txt to analysis the result

	eval_ne_tagger.py ner_dev.key output_1.txt
