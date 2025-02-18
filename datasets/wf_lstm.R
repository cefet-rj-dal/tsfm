source("wf_experiment.R")

datasets <- c('climate', 'emissions', 'emissions-co2', 'fertilizers', 'gdp', 'pesticides')
test_size <- 5
params_1 <- list( sw_size = 6,
				  input_size = 1:4,
                  ranges = list(),
                  preprocess = list(ts_norm_diff()),
                  augment = list(ts_aug_none()) )
params_2 <- list( sw_size = 6,
                  input_size = 1:4,
                  ranges = list(),
                  preprocess = list(ts_norm_diff()),
                  augment = list(ts_aug_jitter()) )

for (ds in datasets) {
  create_directories(sub('-.*', '', ds))
  df <- read.csv(sprintf('%s/input/%s.csv', sub('-.*','',ds), ds))
  for (j in (1:length(df))) {
    ts <- names(df)[j]
    filename <- sprintf('%s/%s_%s', sub('-.*','',ds), ts, 'lstm')
    print(filename)
    run_ml(x=df[[j]], filename, ts_lstm(), test_size=test_size, params=params_1)
    run_ml(x=df[[j]], filename, ts_lstm(), test_size=test_size, params=params_2)
  }
}