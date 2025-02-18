source("wf_experiment.R")
source(paste(dirname(getwd()), "chronos/zero shot/ts_chronos.R", sep="/"))

datasets <- c('climate', 'emissions', 'emissions-co2', 'fertilizers', 'gdp', 'pesticides')
test_size <- 5
samples <- c(30, 60, 90, 200, 500, 1000)
base_model <- c( 'amazon/chronos-t5-tiny',
				 'amazon/chronos-t5-small',
				 'amazon/chronos-t5-base',
				 'amazon/chronos-t5-large' )

for (i in 1:length(datasets)) {
  train <- read.csv(paste(data_path, sprintf('%s-train.csv', datasets[i]), sep=''), header=TRUE, row.names=1)
  train <- as.data.frame(t(train))
  test <- read.csv(paste(data_path, sprintf('%s-test.csv', datasets[i]), sep=''), header=TRUE, row.names=1)
  test <- as.data.frame(t(test))
  
  create_directories(datasets[i])
  
  for (j in colnames(train)) {
    ts_train <- na.omit(train[[j]])
    ts_test <- na.omit(test[[j]])
    ts <- c(ts_train, ts_test)
    filename <- sprintf('%s/%s_%s', datasets[i], j, 'chronos-zeroshot')
    run_llm(x=ts, filename, ts_chronos(), test_size=length(ts_test), samples=samples, params=base_model)
  }
}