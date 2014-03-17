#!/bin/bash

docUrl=dip21.bundestag.de/dip21/btp/18/
pathPdf=../BT18/pdf
pathTxt=../BT18/txt
pathScripts=.
pathInsights=../../../insights/keywords

# if no argument is provided then the first to be downloaded
# and processed document is inferred from the already
# present pdf-files:w
if [ $# = 0 ]; then
  # looks up most recent downloaded PDF
  x=$(ls $pathPdf | sort -nr | head -1 | tr -cd "[:digit:]")

  # number of first to be processed protocol
  lowest=$(($x+1))
else
  lowest=$1
fi


n=$lowest

# check if protocol is already available (sequentially)
while wget -q --spider $docUrl$n.pdf
do
  # download protocol and convert to txt
  #wget $docUrl$n.pdf -P $pathPdf
  #pdftotext $pathPdf/$n.pdf $pathTxt/$n.txt

  # process the text file 
  # (delayout.py is computationally ineffecient and very slow)
  #python3 $pathScripts/text/delayout.py $pathTxt/$n.txt
  #python3 $pathScripts/text/dehyphenate.py $pathTxt/$n.long.txt
  #python3 $pathScripts/text/purify.py $pathTxt/$n.reunited.txt

  # extracts session number from protocol number
  m=$(echo $n | grep -oP "[1-9]{1}[0-9]{0,2}$")
  
  # the R script calculates the tf-idf ranking
  #Rscript $pathScripts/keywords/run-tf-idf-evaluation.R $m

  # version and publish
  git pull origin master
  git add $pathInsights/bt-18-$m.md
  git commit -m "top keywords for new session"
  git push origin master

  # next one
  n=$(($n+1))
done
highest=$(($n-1))
