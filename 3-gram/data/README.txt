运行 generate_rare_data.py 产生 ner_train_rare.dat

命令：generate_rare_data.py

在产生的ner_train_rare.dat 基础上运行count_freqs.py 产生带有_rare_标记的
数据：ner_train_rare.dat

命令：python count_freqs.py ner_train_rare.dat  ner_train_rare.dat

运行generate_Q_value.py产生Q_value.txt文件

运行 get_output_2.py得到用第一种方法标记得结果

运行eval_ne_tagger.py ner_dev.key output_2.txt进行结果分析

命令：eval_ne_tagger.py ner_dev.key output_2.txt

