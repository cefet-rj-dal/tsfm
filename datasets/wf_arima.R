source("wf_experiment.R")

datasets <- c('climate', 'emissions', 'emissions-co2', 'fertilizers', 'gdp', 'pesticides')
test_size <- 5

for (ds in datasets) {
  create_directories(sub('-.*', '', ds))
  df <- read.csv(sprintf('%s/input/%s.csv', sub('-.*','',ds), ds))
  for (j in (1:length(df))) {
    ts <- names(df)[j]
    filename <- sprintf('%s/%s_%s', sub('-.*','',ds), ts, 'arima')
    print(filename)
    run_ml(x=df[[j]], filename, ts_arima(), test_size=test_size)
  }
}