import torch
import pandas as pd
import numpy as np
from typing import Literal, Optional
from chronos import ChronosPipeline

class TsChronosNet:
    def __init__(
        self,
        df_test: pd.DataFrame,
        data_target: str,
        model: Literal[
            "amazon/chronos-t5-tiny", "amazon/chronos-t5-small", "amazon/chronos-t5-base", "amazon/chronos-t5-large"
        ] = "amazon/chronos-t5-small",
        device_map: Literal["cuda", "cpu", "mps"] = "cpu",
        torch_dtype: torch.dtype = torch.bfloat16,
        # Chronos parameters with default values
        prediction_length: Optional[int] = 12,
        num_samples: Optional[int] = 20,
        temperature: Optional[float] = 1.0,
        top_k: Optional[int] = 50,
        top_p: Optional[float] = 1.0,
        limit_prediction_length: bool = True,
    ):
        """
        Initialize the TsChronosNet model and prepare data.

        Parameters:
        - df_test (pd.DataFrame): DataFrame containing the time series data.
        - data_target (str): Name of the target column in df_test.
        - model (str): Name of the pre-trained Chronos model to use.
          Must be one of:
            "amazon/chronos-t5-tiny",
            "amazon/chronos-t5-small",
            "amazon/chronos-t5-base",
            "amazon/chronos-t5-large"
        - device_map (str): Device to run the model on.
          Must be one of: "cuda", "cpu", "mps"
        - torch_dtype (torch.dtype): Data type for torch tensors.
        - prediction_length (int): Number of future time steps to predict.
        - num_samples (int): Number of samples to draw for each prediction.
        - temperature (float): Sampling temperature.
        - top_k (int): Top-K sampling.
        - top_p (float): Nucleus sampling probability.
        - limit_prediction_length (bool): Whether to limit the prediction length.
        """
        # Optional runtime validation
        allowed_models = [
            "amazon/chronos-t5-tiny",
            "amazon/chronos-t5-small",
            "amazon/chronos-t5-base",
            "amazon/chronos-t5-large",
        ]
        allowed_devices = ["cuda", "cpu", "mps"]

        if model not in allowed_models:
            raise ValueError(f"Invalid model '{model}'. Allowed models are: {allowed_models}")

        if device_map not in allowed_devices:
            raise ValueError(f"Invalid device_map '{device_map}'. Allowed devices are: {allowed_devices}")

        self.model_name = model
        self.device_map = device_map
        self.torch_dtype = torch_dtype
        self.prediction_length = prediction_length
        self.num_samples = num_samples
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.limit_prediction_length = limit_prediction_length

        # Store the data and target column
        self.df_test = df_test
        self.data_target = data_target

        # Initialize the pipeline
        self.pipeline = ChronosPipeline.from_pretrained(
            self.model_name,
            device_map=self.device_map,
            torch_dtype=self.torch_dtype,
        )

        # Prepare the context data
        data = self.df_test.iloc[: -self.prediction_length]
        self.context_series = torch.tensor(
            data[self.data_target].values, dtype=torch.float32
        )


def ts_chronos_create(df=pd.DataFrame(), target=[], pred_length=0, samples=100, base="amazon/chronos-t5-small"):
    """
    """
    model = TsChronosNet(
        df_test=df,
        data_target=target,
        model=base,                       # Choose from the allowed options
        device_map="cpu",                 # Choose from "cuda", "cpu", or "mps"
        prediction_length=pred_length,    # Default prediction length
        num_samples=samples,              # Number of samples for prediction
        temperature=0.8,                  # Sampling temperature
        top_k=100,                        # Top-K sampling
        top_p=0.9,                        # Nucleus sampling probability
        limit_prediction_length=True      # Whether to limit the prediction length
    )
    return model


def ts_chronos_fit(model, df_train):
    pass
    return model


def ts_chronos_predict(model, df_test, target, pred_length=1, samples=100, base="amazon/chronos-t5-small") -> pd.DataFrame:
    """
    Generate predictions using the Chronos model.
    """
    model = ts_chronos_create(df_test, target, pred_length, samples, base)
    
    # Generate the forecast
    forecast = model.pipeline.predict(
        context=model.context_series,
        prediction_length=model.prediction_length,
        num_samples=model.num_samples,
        temperature=model.temperature,
        top_k=model.top_k,
        top_p=model.top_p,
        limit_prediction_length=model.limit_prediction_length,
    )

    # Store the forecast
    forecast_median = pd.DataFrame(
        np.quantile(forecast[0].numpy(), 0.5, axis=0),
        columns=[model.data_target]
    )
    
    prediction = forecast[0].numpy()
  
    return pd.DataFrame(prediction)
