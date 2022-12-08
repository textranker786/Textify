import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq  import nlargest 

text="""Robert Hooke's father was John Hooke who was a curate at All Saints Church in Freshwater on the Isle of Wight. Although formally a curate, since the minister was also Dean of Gloucester Cathedral and of Wells, John Hooke was left in charge of All Saints. It was a well off church being in the patronage of St John's College, Cambridge. As well as his duties in the church, John Hooke also ran a small school attached to the church and acted as a private tutor. Robert had a brother who was five years older, named John, the same name as his father.

Relatively few details of Robert's childhood are known. What we record here is information which he mentioned to his friends later in his life. Robert, like many children of his day, had poor health and was not expected to reach adulthood. His father was from a family in which it was expected that all the boys joined the Church (John Hooke's three brothers were all ministers) so had Robert enjoyed good health as a child there is no doubt that he would have followed the family tradition. As it was Robert's parents did begin to set up his education with this in mind but he continually suffered from headaches which made studying hard. Lacking confidence that he would reach adulthood, Robert's parents gave up on his education, leaving him much to his own devices.

Robert's own ideas involved his observational skills and his mechanical skills. He observed the plants, the animals, the farms, the rocks, the cliffs, the sea, and the beaches around him. He was fascinated by mechanical toys and clocks, making many things from wood from a working clock to a model of a fully rigged ship with working guns. Waller, in the Preface to Hooke's Posthumous Works published in 1705, dates his belief in mechanics, in particular his belief that nature was a complicated machine, from the time that he let his imagination and his talents run riot at about age ten."""
def summer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)
    nlp= spacy.load("en_core_web_sm")
    doc=nlp(rawdocs)
    #print(doc)
    token=[token.text for token in doc]
    #print(token)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
           if word.text not in word_freq.keys():
              word_freq[word.text]=1
           else:
              word_freq[word.text]+=1
    #print(word_freq)

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    #print(word_freq)

    sent_tokens= [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
               if sent not in sent_scores.keys():
                  sent_scores[sent] = word_freq[word.text]
               else:
                  sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)        
      
    select_len = int(len(sent_tokens)*0.3)
    #print(select_len)

    summary= nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)
    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    #print(text)
    #print(summary)
    #print("length of original text :",len(text.split(' ')))
    #print("length of summary text :",len(summary.split(' ')))
    
    return summary, doc, len(rawdocs.split(' ')),len(summary.split(' '))
    
