library('daltoolbox')

python_src = paste(dirname(getwd()), "chronos/zero shot/ts_chronos.py", sep="/")

ts_chronos <- function() {

  obj <- ts_reg()
  class(obj) <- append("ts_chronos", class(obj))

  return(obj)
}


#'@export
fit.ts_chronos <- function(obj, x, y=NULL, ...) {
  return(obj)
}


#'@export
predict.ts_chronos <- function(obj, x, y=NULL, steps_ahead=NULL, samples=100, ...) {
  if (!exists("ts_chronos_predict"))
    reticulate::source_python(python_src)
  
  ts <- c(x, y)
  ts <- as.data.frame(ts)
  target <- colnames(ts)[ncol(ts)]
  
  predictions <- ts_chronos_predict(obj$model, ts, target, as.integer(steps_ahead), as.integer(samples), ...)

  return(predictions)
}
