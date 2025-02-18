source("wf_experiment.R")
source(paste(dirname(getwd()), "chronos/zero shot/ts_chronos.R", sep="/"))

datasets <- c('climate', 'emissions', 'emissions-co2', 'fertilizers', 'gdp', 'pesticides')
test_size <- 5
samples <- c(30, 60, 90, 200, 500, 1000)
base_model <- c( 'amazon/chronos-t5-tiny',
                 'amazon/chronos-t5-small',
                 'amazon/chronos-t5-base',
                 'amazon/chronos-t5-large' )

for (ds in datasets) {
  create_directories(sub('-.*', '', ds))
  df <- read.csv(sprintf('%s/input/%s.csv', sub('-.*','',ds), ds))
  for (j in (1:length(df))) {
    ts <- names(df)[j]
    filename <- sprintf('%s/%s_%s', sub('-.*','',ds), ts, 'chronos-zeroshot')
    print(filename)
    run_llm(x=df[[j]], filename, ts_chronos(), test_size=test_size, samples=samples, params=base_model)
  }
}