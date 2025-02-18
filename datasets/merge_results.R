library(purrr)
library(dplyr)


merge_results <- function(){
  
  current_path <- getwd()
  datasets <- c('climate', 'emissions', 'fertilizers', 'gdp', 'pesticides')
  results_path <- 'results/'
  consolidated_data <- list()
  
  for (ds in datasets) {
    
    merge_path <- paste(current_path, ds, results_path, sep="/")
    filename <- sprintf("%s/%s/%s_combined_results.rdata", current_path, ds, ds)
    print(filename)
    
    # Deleta o arquivo se existir
    if (file.exists(filename)) {
      file.remove(filename)
    }
    
    # Combine todos os arquivos
    all_files <- list.files(merge_path, full.names=TRUE, recursive=TRUE, pattern='.rdata') %>%
      map_df(~ get(load(file=.x)))
    
    # Adiciona os resultados ao arquivo consolidado
    consolidated_data[[ds]] <- all_files
    
    # Salva os arquivos individuais
    save(all_files, file = filename)
    write.csv(all_files, file = gsub("rdata", "csv", filename), row.names=FALSE)
  }
  
  # Consolidar os dados de todos os datasets
  consolidated_data <- bind_rows(consolidated_data)
  
  # Salva o arquivo consolidado
  filename <- paste(current_path, 'combined_results.rdata', sep="/")
  save(consolidated_data, file = filename)
  write.csv(consolidated_data, file = gsub("rdata", "csv", filename), row.names=FALSE)
}


merge_results()