
F_pure <- generate_file_names_for_protocols(1:18,type="pure")
F_dehy <- generate_file_names_for_protocols(1:18,type="reunited")
TFIDF <- calc_tfidf(F_pure)
#cat(generate_markdown_for_protocol(TFIDF, get_word_vector(F_pure[3]), session=3))

create_markdown_file_for_session <- function(s) {
  cat(generate_markdown_for_protocol(TFIDF, get_protocol_as_string(F_dehy[s]), session=s, num_context=5, rad=40), 
    file=sprintf("/media/raffael/Volume/git-repos/bundestag/insights/keywords/bt-18-%d.md",s))
}