# Definir os argumentos para o script Python
# train_dataset <- "/home/rodrigo_parracho/tema3-llama-chronos/datasets/climate/input/climate.csv"
# script_name <- "~/tema3-llama-chronos/llama/lag-llama/scripts/finetune_CLI.py"
# num_epochs <- 50
# num_predicts <- 1
# valid_dataset <- ""

# ...

# # Executar o comando via system2
# status <- system2(command = "python3", args = a)

# # Verificar o status de saída
# if (status == 0) {
#   message("O comando foi executado com sucesso.")
# } else {
#   message("Houve um erro ao executar o comando.")
# }

fine_predict <- function(train_dataset, steps_ahead, num_epochs=50, val_dataset=NULL, samples=100, zero_shot=FALSE) {

	script_path <- "~/llama/lag-llama/scripts/finetune_CLI.py"

	train_dataset <- paste("'", as.character(train_dataset), "'")

	# Parâmetros obrigatórios 
	parameters <- c(
		"--train_dataset", train_dataset,
		"--steps_ahead", as.integer(steps_ahead)
	)

	# Parâmetros Opcionais (Numero de épocas, dataset de validação, estratégia zero-shot)

	#if (num_epochs != 10){
	parameters <- append(parameters, list("--num_epochs", as.integer(num_epochs)))
	#}
	if (!is.null(val_dataset)){
		val_dataset <- paste("'", as.character(val_dataset), "'")
		parameters <- append(parameters, list("--val_dataset", val_dataset))
	}
	if (zero_shot){
		# Adiciona a flag para fazer zero-shot
		parameters <- append(parameters, "--zero_shot")
	}
	parameters <- append(parameters, list("--samples", as.integer(samples)))

	# Chamada do script via CLI devido a lentidão do reticulate
	status <- system2(command = "python3", args = c(script_path, parameters))
}

# fine_predict(train_dataset, steps_ahead=num_predicts, num_epochs=num_epochs)