import argparse
import pandas as pd
import numpy as np
from ts_lag_llama import *


def split_time_series(dataframe, column_name, n):
    """
    Separa uma série temporal de acordo com as x últimas observações.

    Parameters:
    dataframe (pd.DataFrame): DataFrame contendo a série temporal.
    column_name (str): Nome da coluna com a série temporal.
    x (int): Número de observações para separar no final.

    Returns:
    tuple: (treino, teste) onde treino contém os dados iniciais e teste contém as x últimas observações.
    """
    if column_name not in dataframe.columns:
        raise ValueError(f"A coluna '{column_name}' não está presente no DataFrame.")

    if n <= 0:
        raise ValueError("O número de observações 'x' deve ser maior que 0.")

    # Garantir que temos dados suficientes
    if len(dataframe) < n:
        raise ValueError("O DataFrame não contém observações suficientes para separar as últimas 'x'.")

    # Separação da série temporal
    treino = dataframe[column_name].iloc[:-n].to_list()
    teste = dataframe[column_name].iloc[-n:].to_list()
    
    # Formatação para o Lag-LLama 
    treino = np.array(treino, dtype=float)
    teste = np.array(teste, dtype=float)

    return treino, teste


def generate_results_dataframe(prediction, result_dir="/tmp/"):
	pass    

    

if __name__ == "__main__":
        
	# TODO: Quais informações eu preciso retornar? Predição(Média, Mediana, Quantils?, ...), Estratégia('Finetune'), Modelo(Lag-Llama), Hiperparametros(Nº de Epocas, Passos previstos, ?), 
    # Argumentos
    parser = argparse.ArgumentParser(description="Script para configurar treinamento de modelo.")
    
    parser.add_argument("--train_dataset", type=str, required=True, help="Diretório do dataset de treinamento.")
    parser.add_argument("--steps_ahead", type=int, default=1, help="Número de predições. (Default: 1)")
    parser.add_argument("--num_epochs", type=int, default=50, help="Número de épocas para treinamento. (Default: 50)")
    parser.add_argument("--samples", type=int, default=100, help="Número de tentativas para prever. (Default: 100)")
    parser.add_argument("--val_dataset", type=str, default=None, help="Diretório do dataset de validação. (Opcional - Default: None)")
    # parser.add_argument("--result_dir", type=str, default="/tmp/", help="Diretório do dataset de validação. (Opcional - Default: None)")
    # Define se fará Zero-Shot ou Finetune
    parser.add_argument("--zero_shot", action="store_true", help="Flag para habilitar Zero-Shot. (Default: False)")
    
    args = parser.parse_args()
    
    # TODO: Fazer tratamento de erro caso não exista o dataset
    df = pd.read_csv(args.train_dataset)
    
    # Exibição para debugging
    print("\nConfiguração do Finetune:")
    print(f"- Dataset: {args.train_dataset}")
    print(f"\t Tamanho: {df.shape[0]}")
    print(f"\t Número de predições: {args.steps_ahead}")
    print(f"\t Número de épocas: {args.num_epochs}")
    print(f"\t Dataset de validação: {args.val_dataset}")
    print(f"\t Zero-Shot: {args.zero_shot}")
    
    # exportable_info = {
    #     "steps_ahead": args.steps_ahead,
    #     "n_epochs": args.num_epochs,
    #     "estrategia"
	# }
    
    # results_dataframe = pd.DataFrame()
    
    column_name = df.columns[0]
    train_dataset = np.array(df[column_name].to_list(), dtype=float)
    
    #print("Dataset carregado:")
    # print(f"\tColuna {column_name}:")
    #print(train_dataset)
    
    # train_dataset, test_dataset = split_time_series(dataframe=df, column_name=location, n=args.steps_ahead)
        
    # TODO: Ainda precisa considerar o dataset de validação
    predictions = ts_lag_llama_predict(dataset=train_dataset, steps_ahead=args.steps_ahead, samples=args.samples, epochs=args.num_epochs, val_dataset=None, zs=args.zero_shot)
	
    # BUG-ERROR: Problema de código assincrono??? - Os resultados aparecem ANTES do treinamento terminar
    #print(f"Mean Output: {predictions[0].mean}")
	
	# TODO: Depois da predição, tenho que registrar em um arquivo ou um dataframe de acordo com o contexto (USA, Brasil, México.....) e então salvar isso no RData...
    #results_dataframe[location] = predictions
    
    # TODO: Dependendo da estratégia 
    	#TODO RO -> steps_ahead = 1
    	#ou
    	#TODO SA -> steps_ahead != 1
    #TODO  o df resultado tem que ser feito de formas diferentes
    #print(predictions[0])
    
    # TODO: Quais informações e dados temos que guardar da previsão?
    results = pd.DataFrame({
		# "samples": predictions[0].samples.tolist(),
		"means": predictions[0].mean,
		"medians": predictions[0].median,
		"steps_ahead": predictions[0].prediction_length,
	})
    
    print(results)
    
    print(f"Escrevendo os resultados em /tmp/results_{column_name}.csv")
    results.to_csv(f"/tmp/results_{column_name}.csv", index=False)    
	

 
 
