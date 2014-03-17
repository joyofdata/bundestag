setwd("/media/Volume/git-repos/bundestag/data/protokolle/processing/keywords")
source("tf-idf-evaluation.R")

if(length(commandArgs(TRUE))!=1) {
  stop("argument missing")
}

max_doc_id <- as.numeric(commandArgs(TRUE)[1])

root_path <- "/media/Volume/git-repos/bundestag/"
txt_path <- paste(root_path, "data/protokolle/BT18/txt/", sep="")

# used for calculating tf-idf
F_pure <- generate_file_names_for_protocols(1:max_doc_id,type="pure",txt_path)

# needed for extracting a keywords textual context
F_dehy <- generate_file_names_for_protocols(1:max_doc_id,type="reunited",txt_path)

TFIDF <- calc_tfidf(F_pure)

create_markdown_file_for_session <- function(s, path) {
  cat(generate_markdown_for_protocol(TFIDF, get_protocol_as_string(F_dehy[s]), session=s, num_context=5, rad=40), 
    file=sprintf("%s/bt-18-%d.md",path,s))
}

create_markdown_file_for_session(max_doc_id, paste(root_path,"/insights/keywords",sep=""))