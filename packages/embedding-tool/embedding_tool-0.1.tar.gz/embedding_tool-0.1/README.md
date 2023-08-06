# Dimension Reduction
> The function performs dimensionality reduction, pre-processing the data and comparing the reconstruction error via PCA and autoencoder.


## Install

`pip install embedding-tools`

## How to use

```python
from short_text_analyzer.core import *
```

**Input data:**
The input matrix has a size of 863 $\times$ 768.

```python
print ("Data's size: ", testing_data.shape)
print ("Dimension:   ", testing_data.shape[1])
```

    Data's size:  (863, 768)
    Dimension:    768
    

**Performing dimension reduction:** we will reduce the number of dimension from 768 to 2. 

```python
dim_reducer = dimensionReducer(analyzer.embeddingRaw, 2, 0.002)
dim_reducer.fit()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-5-6ee2cf251bab> in <module>
    ----> 1 dim_reducer = dimensionReducer(analyzer.embeddingRaw, 2, 0.002)
          2 dim_reducer.fit()
    

    NameError: name 'dimensionReducer' is not defined


**Calculating the MSE of the reconstructed vectors**

```python
dim_reducer.rmse_result
```
