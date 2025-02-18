import torch, os, sys

file_path = os.path.dirname(__file__)
folder_path = os.path.join(file_path, '..')
normalized_path = os.path.realpath(folder_path)

sys.path.append(normalized_path)

# # lib imports
import numpy as np

# # gluonts and lag-llama imports
from lag_llama.gluon.estimator import LagLlamaEstimator
from gluonts.dataset.common import ListDataset

MODEL_PATH = os.path.join(normalized_path, 'models/lag-llama.ckpt')

def ts_lag_llama_predict(
  dataset:np.ndarray,
  steps_ahead:int=1,
  samples:int=100,
  epochs:int =50,
  dataset_info = {"start":"1970-01-01 00:00:00", "frequency": "A"},
  val_dataset=None,
  zs=False,
):
    
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = torch.load(MODEL_PATH, map_location=device)

    estimator_args = model["hyper_parameters"]["model_kwargs"]
    
    estimator = LagLlamaEstimator(
      ckpt_path=MODEL_PATH,
      prediction_length=steps_ahead, # Quantos elementos seguidos eu vou prever
      context_length=len(dataset), # Quantos elementos anteriores vou utilizar para prever o atual
      
      trainer_kwargs = {"max_epochs": epochs,}, # lightning trainer arguments
      num_batches_per_epoch=50,
      
      # Hiperparams do modelo
      input_size=estimator_args["input_size"],
      n_layer=estimator_args["n_layer"],
      n_embd_per_head=estimator_args["n_embd_per_head"],
      n_head=estimator_args["n_head"],
      scaling=estimator_args["scaling"],
      time_feat=estimator_args["time_feat"],
    )
    
    dataset = __format_ts(dataset, dataset_info)
    
    if zs:
        # zero-shot
        predictor = estimator.create_predictor( # PyTorchPredictor
            transformation=estimator.create_transformation(), # Chain
            module=estimator.create_lightning_module() # LagLLamaLightningModule
        )
    else:
        # fine-tuning
        predictor = estimator.train(training_data=dataset,validation_data=val_dataset)
    
    forecasts = predictor.predict(
        dataset=dataset,
	    num_samples=samples
	)
    
    return list(forecasts)


def __format_ts(x, dataset_info:dict):
    
    if len(np.array(x).shape) != 1:
      x = np.array(x).reshape(-1).tolist()
    
    dataset = ListDataset(
      data_iter=[{
        "start": dataset_info.get("start"),
        "target": x
      }], freq=dataset_info.get("frequency")
    )
    
    return dataset
