===============================================
              DATA DICTIONARY
===============================================

1. **dataset**
-----------------------------------------------
Description: Datasets used in the experiment.
- 'climate': Climate data
- 'emissions': Pollutant emissions data (CH4 and N2O)
- 'emissions-co2': Data on CO2 emissions
- 'fertilizers': Data on fertilizer usage (K2O, N, and P2O5)
- 'gdp': Gross Domestic Product data
- 'pesticides': Data on pesticide usage

2. **country**
-----------------------------------------------
Description: Countries included in the experiment (the ten largest economies in 2024).
- 'United States of America (USA)'
- 'China'
- 'Germany'
- 'Japan'
- 'India'
- 'United Kingdom (UK)'
- 'France'
- 'Italy'
- 'Canada'
- 'Brazil'

3. **model**
-----------------------------------------------
Description: Predictive models used in the experiment.
- 'arima': ARIMA model (AutoRegressive Integrated Moving Average).
- 'lstm-diff': LSTM model with differentiation.
- 'lstm-diff-jitter': LSTM model with differentiation and jittering (data augmentation).
- 'chronos-zeroshot': Chronos Zero-shot model.
- 'llama-zeroshot': Lag-Llama Zero-shot model.

4. **obs**
-----------------------------------------------
Description: Additional parameters related to the model used.

5. **samples**
-----------------------------------------------
Description: The size of the LLMs' prediction cloud.
- 30
- 60
- 90
- 200
- 500
- 1000

6. **test_size**
-----------------------------------------------
Description: The test period, ranging from 1 to 5.

7. **strategy**
-----------------------------------------------
Description: The strategy used to split the data in the experiment.
- 'rolling origin (ro)': A rolling origin strategy where the training window shifts over time, and predictions are made for the subsequent period.
- 'steps_ahead (sa)': A steps ahead strategy where the model produce predictions for the entire test set in a single task.

8. **true**
-----------------------------------------------
Description: Actual values from the test set.

9. **pred**
-----------------------------------------------
Description: Predicted values. For LLMs, this value is the average of the prediction distributions.

10. **pred_median**
-----------------------------------------------
Description: The median of the prediction distributions. Exclusive to LLMs.

11. **std**
-----------------------------------------------
Description: The standard deviation of the prediction distributions. Exclusive to LLMs.

12. **skewness**
-----------------------------------------------
Description: The skewness of the prediction distributions. Exclusive to LLMs.

13. **kurtosis**
-----------------------------------------------
Description: The kurtosis of the prediction distributions. Exclusive to LLMs.

14. **mse**
-----------------------------------------------
Description: Mean Squared Error (MSE) between the actual values (true) and predicted values (pred).

15. **mse_median**
-----------------------------------------------
Description: Mean Squared Error (MSE) between the actual values (true) and the values predicted by the median of the prediction distributions (pred_median).

16. **smape**
-----------------------------------------------
Description: Symmetric Mean Absolute Percentage Error (SMAPE) between the actual values (true) and the predicted values (pred).

17. **smape_median**
-----------------------------------------------
Description: Symmetric Mean Absolute Percentage Error (SMAPE) between the actual values (true) and the values predicted by the median of the prediction distributions (pred_median).

18. **r2**
-----------------------------------------------
Description: Coefficient of Determination (R²) for the predicted values (pred). Measures the quality of the model's fit.

19. **r2_median**
-----------------------------------------------
Description: Coefficient of Determination (R²) for the predicted values based on the median of the prediction distributions (pred_median).

===============================================
