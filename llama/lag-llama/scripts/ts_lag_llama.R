library('daltoolbox')

python_src = paste(dirname(getwd()), "llama/lag-llama/scripts/ts_lag_llama.py", sep="/")
python_cli_source <- paste(dirname(getwd()), "llama/lag-llama/scripts/finetune_CLI.R", sep="/")
python_cli_path <- paste(dirname(getwd()), "llama/lag-llama/scripts/finetune_CLI.py", sep="/")


call_finetune_prediction <- function(train_dataset, steps_ahead, samples, num_epochs=30, val_dataset=NULL, zero_shot=FALSE) {

	# Parâmetros obrigatórios 
	parameters <- c(
		"--train_dataset", paste("'", as.character(train_dataset), "'", sep=""),
		"--steps_ahead", as.integer(steps_ahead)
	)

	# Parâmetros Opcionais (Numero de épocas, dataset de validação, estratégia zero-shot)
	if (!is.null(val_dataset)){
		val_dataset <- paste("'", as.character(val_dataset), "'")
		parameters <- append(parameters, list("--val_dataset", val_dataset))
	}
	parameters <- append(parameters, list("--samples", as.integer(samples)))

	# Chamada do script via CLI devido a lentidão do reticulate
	status <- system2(command = "python3", args = c(python_cli_path, parameters))

}


ts_lag_llama <- function() {
  obj <- ts_reg()
  
  class(obj) <- append("ts_lag_llama", class(obj))
  return(obj)
}


#' @export
fit.ts_lag_llama <- function(object, x=NULL, y=NULL, steps_ahead=NULL, ...) {
  return(object)
}


#' @export
predict.ts_lag_llama <- function(object, x, y=NULL, steps_ahead=NULL, samples=100, zero_shot=TRUE, ...) {
  if (!exists("ts_lag_llama_predict"))
    reticulate::source_python(python_src)
  
  ts <- c(x, y)
  
  if (!is.null(y))
	ts <- ts[1:(length(ts)-steps_ahead)]
  
  predictions <- ts_lag_llama_predict(dataset=ts, steps_ahead=steps_ahead, samples=as.integer(samples), zs=TRUE)
  
  return(predictions[[1]]$samples)
}


#' @export
predict_finetune.ts_lag_llama <- function(object, x, y=NULL, steps_ahead=NULL, samples=100, zero_shot=FALSE, ...) {

	# Função que faz a chamada via linha de comando
	# source(python_cli_source)
	ts <- c(x, y)
  
	if (!is.null(y))
		ts <- ts[1:(length(ts)-steps_ahead)]

	# Formação do filename da serie temporal:
		"time_serie_{coluna/contexto}_{seed}.csv"

	# Formação do filename dos resultados :
		"/tmp/results_{coluna/contexto}.csv"
	
	context <- names(x)
	# Armazenar o x em um arquivo temporário e passar o caminho dele
	temp_file_path <- tempfile(fileext = ".csv", pattern=paste("time_serie", context, sep = "_"))
	write.csv(ts, temp_file_path, row.names=FALSE)

	call_finetune_prediction(train_dataset=temp_file_path, steps_ahead=steps_ahead, samples=samples)

	# Buscar um resultado em um arquivo específico
	# Neste ponto, o script python já deve ter salvo os resultados no local definido
	output_filename <- "/tmp/results_x.csv"
	
	print("Lendo arquivo salvo em")
	print(output_filename)
	
	predictions_csv <- read.csv("/tmp/results_x.csv")
	print(predictions_csv)
	return(predictions_csv)
}
