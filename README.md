# Classical-Chinese-Segmentation
Class project for CSCI 544 Natural Language Processing

## Introduction
Classical Chinese is the language of Chinese classic literature from approximately the 3rd century BC until the early 1900s. This language was used by many famous Chinese historians and philosophers whose thoughts and writings, preserved only in Classical Chinese, are increasingly inaccessible due to the evolution of the Chinese language.

Due to the difference in vocabulary, word order, and sentence structure, Classical Chinese is very different from Modern Chinese. Even for native speakers from Modern China, Classical Chinese is difficult to read and understand. If effective machine translation is accomplished, it will give the approximately 1.2 billion speakers of Modern Chinese access to many previously untranslated Classical Chinese texts.

Currently, there are few Classical Chinese machine translation tools, and they are very inaccurate. Translation programs for translating Modern Chinese into other languages performs quite poorly on Classical Chinese text.

Although ample research has been conducted into the area of Modern Chinese translation, Classical Chinese lags behind. Since Chinese does not include any word markers, effective translation relies on accurate word segmentation. The Stanford Word Segmenter is effective for the segmentation of Modern Chinese, but from cursory testing it does not perform well on Classical Chinese.

We developed a word Segmenter for Classical Chinese using conditional random fields and CRFSuite on two different corpora. Then, we used this Segmenter to preprocess text for machine translation from Classical Chinese to Modern Chinese using seq2seq.

## Materials

For this project we used data from three corpora. The first two, the Sheffield Corpus and Sinica Corpus, provided data for training and testing the word segmenter. The last, documents from Guwen Guanzhi, was used for training and testing our translator.

The Sheffield Corpus2 comprises of three documents from the Song (960-1279), Ming (1366-1644) and Qing (1644-1911) eras. This was the smallest corpus we used, at a total of about 18,000 words. Each document was provided in an XML file, with sentence and simple part of speech tags consisting of six categories.

The Sinica Corpus3 is a much larger collection of Classical Chinese. It consists of nearly 6 million Chinese characters, split into sentences with part of speech tagged words. This corpus consists of very old text, from pre-Qin to the Western Han Dynasty (~200 BC-200 AD), and the Wei, Jin and Southern and Northern Dynasties (200-500 AD). It also has more recent Classical text from after the Tang Dynasty (800+ AD). The part of speech tags provided by this corpus are much more detailed, consisting of 58 different tags.

For translation, we used documents from the Guwen Guanzhi anthology, consisting of over 200 essays first published during the Qing dynasty. They were written from approximately 1000 BC to 1644 AD, during which time the language was constantly evolving. Because of the historical importance of these documents, they have been manually translated into Modern Chinese, providing a parallel corpus to train a machine translator. Each document is available in Classical and Modern Chinese on gushiwen.org4​ ​. All together, the documents are over 500,000 characters in both Classical and Modern Chinese. They consist of just raw text, without segmentation or POS tags.

## Procedure

We began by converting the Sheffield and Sinica data into the appropriate format for the segmenter. To do this, we wrote two python scripts, one for each corpus. These scripts read XML and JSON data respectively, and output a tuple of the Chinese character, POS tag, and either “I” or “N”. “I” stands for “Initial” marking that this character is the initial character of a word, “N” stands for “Non-initial” and marks any characters which do not begin a word.

For example, the XML data representing the word ​垂楊柳​:

`<noun ​type​="​polysyllabic​" ​pinyin​="​chuiyangliu​">​垂楊柳​</noun>`

Our converted format:

```
垂 noun I
楊 noun N
柳 noun N
```

In both corpora, each word has a POS tag and is therefore already segmented. To create the “I” and “N” tags, we simply split each word into its individual characters, and mark each character with the appropriate tags. We add “I” and “N” tags so that we can create a tagger to perform segmentation. Instead of inserting spaces, our segmenter simply tags each character with “I” if it thinks it is the first character, and “N” otherwise. Once each character is tagged, it is easy to convert these to words with spaces if necessary.

We built our segmenter using CRFSuite5​ ​, an implementation of conditional random fields, as a tagger. For each corpus we trained two separate models. The first was trained to tag each character with “I” or “N” using only the raw text. The second did the same, but with the POS tags as additional input.

For translation, we first scraped from Gushiwen6​ ​ websites to get data for Classical Chinese articles and their corresponding original Chinese translation. Then we used tf-seq2seq7​ ​ library and trained a machine translation model from Classical Chinese to Modern Chinese. Before training, we preprocessed our data. First, we generated data in parallel text format from our scraped json files. Then we segmented the Classical Chinese documents. Finally, we created fixed vocabularies for sources and targets data. We fed our data to the library with a default small model configuration and 5000 steps and began training.

## Evaluation

To evaluate our segmenter, we rely mostly on the tools built into CRFSuite. The evaluation of test data results in precision, recall, and F1 scores. This is broken down into scores per tag and averaged over both tags, as well as item accuracy and instance accuracy. As a baseline, we found that tagging every character with “I” results in about 75% accuracy in the Sheffield corpus and 78% in the Sinica corpus. We also evaluate two models, one using POS tags and the other not, against each other to determine how much of an advantage access to POS tags gives a segmentation tagger. Depending on the results, this allows us to gain insight into the question of whether POS tags and segmentation are more accurate when done in parallel, or if segmentation should be done before POS tagging occurs.

Both the Sheffield and Sinica Corpora have data from a range of years, but since there is much less text from the Sheffield Corpus, there is less variety in the characters. This provides the Sheffield tagger an advantage. The Sinica corpus has more variety of characters, but it also has much more data available for training the model. Comparing the results of these two allows us to determine if separate models are needed for each era of Chinese history, or if the character sets are similar enough that one model can effectively segment Classical Chinese documents from any era.

To evaluate the machine translation, we use BLEU8​ ​ scores. We calculate the score of the translation of segmented Classical Chinese data on a model trained with segmented data. The baseline is the score of unsegmented data translated with a model trained on unsegmented data. As we our calculating BLEU scores with just one reference translation the scores are expected to be low, however we hope to compare the two scores to each other to gain insight into the benefit of segmenting data before translation.

## Results

For the full results of our segmentation models see Table 1 of Final_Report.pdf. 

For the Sheffield corpus the baseline accuracy is 74.9%. In both cases our segmenter does better than this. The model without POS tags has an item accuracy of 95.2%, and with the POS tags it is 99.2% accurate. This shows a clear improvement over just treating every character as its own word.

For the Sinica corpus, the baseline accuracy is 78.7%, and our segmenter does better, but only slightly. The model without POS gets 83.3% accuracy. The model with tags is excellent, with an accuracy of 98.0%.

In both cases, the model with tags is better than the one without in accuracy, precision, recall, and F1. This makes intuitive sense, as the tags provide more data which can be used for segmentation. While it would be impractical to tag raw text before segmenting it, these results suggest that a POS tagger which does segmentation simultaneously would be more accurate than doing isolated segmentation before tagging. A combined POS tagger/segmenter could maximize the expected result of different tag and segmentation combinations, instead of segmenting with just raw characters then tagging based on a single proposed segmentation.

The Sheffield corpus is much smaller than the Sinica corpus, and it is initially surprising that our raw text Sheffield tagger does much better, since it is trained on less data. However, the documents making up the Sheffield corpus come from just three eras of Chinese history, while the Sinica corpus spans many eras over nearly 2000 years. We believe that the lower accuracy of the Sinica tagger is a result of changes in the Chinese language over this time, which results in a less accurate model.

Unfortunately, we were unable to get adequate translation results. The BLEU scores of our translations of segmented and unsegmented data came out to < .01. Logs of training the model are shown in figure 2. Due to the computing power required by tf-seq2seq, we were forced to train on a smaller model using fewer steps, and this resulted in poor translations.


## Followup

The difference between the Sinica and Sheffield accuracy shows that it is very difficult to train a single model to handle segmentation of all eras of Classical Chinese. The characters and style of Chinese sentences has changed dramatically throughout different periods of Ancient Chinese history. Dynasties like Ming, Yuan and Qing shared very similar format and word usage. In comparison, eras such as Song and Tang have very different word usage. Predictions can be made more accurate if multiple segmenters are used, and each is trained on data from a single era.

When we applied the CRF model to Classical Chinese Segmentation we achieved relatively high accuracy in prediction. This result shows that the accurate large scale segmentation of Classical Chinese is achievable with the effective use of training data.

During our research, we realized that Classical Chinese corpora are scarce, and there is no standardization between existing corpora. We collected Classical Chinese corpora from multiple sources and standardized their formats for our segmenter, but we could only do so much to combine them. The POS tagged corpora we were able to access used very different tags, and there was no easy way to consolidate the tags so that they could be used to train a single model.

For large scale future research to occur, standardized corpora are needed, so that models can be trained on significant amounts of data. There also needs to be data that is both POS tagged and translated from Classical Chinese to Modern Chinese, so that effective machine translation models can be created using POS tags and segmentation.
