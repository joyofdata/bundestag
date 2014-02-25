get_word_vector <- function(f,lower=FALSE,min_len=2) {
  w <- scan(file=f, sep="", what=character())
  
  if(lower) {
    w <- tolower(w)
  }
  return(w[nchar(w)>=min_len])
}

get_protocol_as_string <- function(f) {
  t <- readChar(f, file.info(f)$size)
  t <- gsub("[\r\n]"," ",t)
  t <- gsub("%%[^%]+%%","",t)
  return(t)
}

get_context_of_word_in_string <- function(str, word, char_rad = 30) {
  found <- gregexpr(sprintf(".{0,%d}[^A-ZÄÖÜa-zäöüéèáàß-]%s[^A-ZÄÖÜa-zäöüéèáàß-].{0,%d}",char_rad,word,char_rad), str)
  
  if(found[[1]][1] == -1) return("-")
  
  context <- mapply(function(i,l)(substr(str,i,i+l)),found[[1]],attributes(found[[1]])$match.length)
  
  return(context)
}

get_context_of_element_in_vector <- function(vec, w, rad = 6) {
  vec <- c(rep("",rad),vec,rep("",rad))
  
  f <- which(vec == w)
  
  get_idxs <- function(g){
    return(g+(-rad:rad))
  }
  
  idxs <- unlist(sapply(f,get_idxs,simplify=FALSE))
  
  context <- apply(matrix(vec[idxs],byrow=TRUE,ncol=(2*rad+1)),1,function(c)paste(c,collapse=" "))

  return(context)
}



get_freq_table <- function(F,lower=FALSE) {
  library(sqldf)
  FT <- 0
  for(i in 1:length(F)) {
    v <- data.frame("w" = get_word_vector(F[i],lower))
    ft <- sqldf("select w, count(*) as n from v group by w")
    colnames(ft) <- c("w",sprintf("n%03d",i))
    if(is.data.frame(FT)) {
      FT <- merge(FT,ft,all=TRUE,by="w")
    } else {
      FT <- ft
    }
  }
  FT[is.na(FT)] <- 0
  return(FT)
}

generate_markdown_for_protocol <- function(TFIDF, words, session, bt=18, top=20,rad=5,num_context=6) {
  str <- sprintf("#<a href='http://dip21.bundestag.de/dip21/btp/%d/%d%03d.pdf' target='x'>Bundestag %d-%d</a> \n",bt,bt,session,bt,session)
  top_link_id <- sprintf("bundestag-%d-%d",bt,session)
  str <- paste(str,"######(Keywords ranked by tf-idf-statistic) \n",sep="")
  
  if(colnames(TFIDF[["tfidf"]])[2] != "n001") {
    error("1st column is expected to contain words and sequentially from second on the respective statitics for the different sessions named 'n001','n002' etc.")
  }
  tfidf <- TFIDF[["tfidf"]][,c(1,session+1)]
  ft <- TFIDF[["ft"]][,c(1,session+1)]
  tf <- TFIDF[["tf"]][,c(1,session+1)]
  idf <- TFIDF[["idf"]][,c(1,session+1)]
  
  colnames(tfidf) <- c("w","n")
  colnames(ft) <- c("w","n")
  colnames(tf) <- c("w","n")
  colnames(idf) <- c("w","n")
  
  keywords <- sqldf(sprintf("select w, n from tfidf order by n desc limit %d",top))
  
  str <- paste(str, "rank | term | ft | tfidf | tf | idf", sep="\n")
  str <- paste(str, "--- | --- | ---: | ---: | ---: | ---:", sep="\n")
  
  for(i in 1:nrow(keywords)) {
    keyword <- keywords[i,"w"]
    keyword_tfidf <- tfidf[tfidf$w==keyword,"n"]
    keyword_ft <- ft[ft$w==keyword,"n"]
    keyword_tf <- tf[tf$w==keyword,"n"]
    keyword_idf <- idf[idf$w==keyword,"n"]
    
    str <- paste(str, sprintf("%d | [%s](#%s) | %d | %.5f | %.5f | %.5f",i,keyword,tolower(keyword),keyword_ft,keyword_tfidf,keyword_tf,keyword_idf), sep="\n")
  }
  
  str <- paste(str,"\n\n")
  
  for(i in 1:nrow(keywords)) {
    
    str <- paste(str, sprintf("###[%s](#%s)\n",keywords[i,"w"],top_link_id),sep="")
    
    # words is expected to be either a string containing the text or a word vector
    if(length(words) > 1) {
      # will extract context from word vector. punctuation is missing then
      context <- get_context_of_element_in_vector(words, keywords[i,"w"], rad = rad)
    } else {
      context <- get_context_of_word_in_string(words, keywords[i,"w"], char_rad = rad)
    }
    
    if(!is.na(num_context)) {
      context <- context[sample(length(context),min(num_context,length(context)))]
    }
    
    for(j in 1:length(context)) {
      str <- paste(str, sprintf("* %s", context[j]), sep="\n")
    }
    
    str <- paste(str,"\n\n")
  }
  
  return(str)
}

get_term_freq_aug <- function(FT) {
  # num of protocols covered in FT
  nc <- ncol(FT)-1
  
  d_max <- apply(FT[,-1],2,max)
  FT[,-1] <- 1/nc + (FT[,-1]/matrix(d_max,ncol=nc,nrow=nrow(FT),byrow=TRUE))
  return(FT)
}

get_inv_doc_freq <- function(FT) {
  FT[,-1] <- log(ncol(FT[,-1])/apply(FT[,-1]>0,1,sum))
  return(FT)
}

calc_tfidf <- function(F,lower=FALSE) {
  FT <- get_freq_table(F, lower)
  tf <- get_term_freq_aug(FT)
  idf <- get_inv_doc_freq(FT)
  
  tfidf <- tf
  tfidf[,-1] <- tf[,-1] * idf[,-1]
  return(list("tfidf"=tfidf,"ft"=FT,"tf"=tf,"idf"=idf))
}

generate_file_names_for_protocols <- function(I=1:1, type="pure", path="/media/raffael/Volume/git-repos/bundestag/data/protokolle/BT18/txt/") {
  F <- c()
    
  for(i in I) {
    f <- sprintf("%s180%02d.%s.txt",path,i,type)
    F <- c(F,f)
  }
  
  return(F)
}