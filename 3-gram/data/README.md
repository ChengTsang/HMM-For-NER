

run generate_rare_data.py to generate ner_train_rare.dat

	generate_rare_data.py

run count_freqs.py on ner_train_rare.dat to generate data with tag \_rare_

	python count_freqs.py ner_train_rare.dat  ner_train_rare.dat

run generate_Q_value.py to generate Q_value.txt file

run get_output_2.py to get the tag from first method

run eval_ne_tagger.py ner_dev.key output_2.txt to analysis the result

	eval_ne_tagger.py ner_dev.key output_2.txt
