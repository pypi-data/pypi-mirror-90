<h1 align="center">
    <img width="100" src="https://www.visualone.tech/images/logo.png" alt="Visual One">
    <br>
Visual One
</h1>

Visual One's few shot learning framework allows you to easily train models for complex computer vision tasks using only a few samples in two lines of code. <br>
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Train%20a%20computer%20vision%20model%20using%20only%20a%20few%20samples%20with%20two%20lines%20of%20code%21&url=https://www.visualone.tech&hashtags=ai,ml,machine_learning,deep_learning,computer_vision,few_shot_learning)

To see some examples, visit the [examples page of our website.](https://visualone.tech/examples)

## Quickstart
- Install the package: `pip install visualone`

- Submit your email [here](https://getvisualone.com/access) to receive your public and private keys via email.

- Train a model by providing some positive samples and some negative samples:
```python
from visualone import vedx

client = vedx.client(public_key, private_key)

model = client.train(positive_samples, negative_samples)
```
- Apply the trained model to a new image to do prediction:
```python
client.predict(model['task_id'], image_file)
```

## Description of inputs & outputs
#### Training
```python
model = client.train(positive_samples, negative_samples)
```

`positive_samples` and `negative_samples` must be either:
- `str`: The path to a directory containing image files representing all of the positive/negative samples.<br>
Or<br>
- `list[str]`: The name of the individual files corresponding to the positive/negative samples. 

Returns a `dict` with the following keys:<br>
`task_id`: A unique task id generated for this task. You need to pass this to `client.predict` to do prediction.<br>
`n_positive_samples`: The number of positive samples used for training the model.<br>
`n_negative_samples`: The number of negative samples used for training the model.<br>
`success`: `1` if the training was done successfully. `0` if an error occured.<br>
`message`: A brief message describing the error if an error occurs.

#### Prediction
```python
client.predict(task_id, image_file)
```

`task_id`: The unique task id corresponding to the trained model returned by `vedx.train` <br>
`image_file`: The path to the file for which you want to do inference.

Returns a `dict` with the following keys:<br>
`task_id`: The task id corresponding to the model.<br>
`prediction`: A boolean representing the model prediction. `True` means the model predicted a positive label for the given image. `False` means the model predicted a negative label for the given image. <br>
`confidence`: A number between 0 and 100 representing the confidence of the model for this prediction. <br>
`latency`: The time it took to do the prediction in millisecond.


### Report Bugs/Issues & Feature Request
Please, help us improve our product by [reporting any bugs or issues](mailto:contact@visualone.tech?subject=[visualone%PyPI]%20Bug%20Report) while using visualone. Also, feel free to [let us know any feature requests.](mailto:contact@visualone.tech?subject=[visualone%PyPI]%20Feature%20Request)

