Index Format :
  Created multiple indices which stores docid along with its wighted
  score (combiation of different types of scores for different type of field indices)
  Used Algo for weights are Tf,Tf-Idf and combination of both.
  Tf score = 1 + log(termFrequency in that doc)
  Idf score = log(totalDocs/docs_Having_that_Word)
  Tf-Idf = Tf*Idf

Searching :
  For each word score = weight of field*(Tf-Idf score)
  Score of a doc is sum of socre of each query word in that doc
  Select the K best docs

Fast Searching ;
  Stored offset value of each posting list to access in O(1) using file seek
