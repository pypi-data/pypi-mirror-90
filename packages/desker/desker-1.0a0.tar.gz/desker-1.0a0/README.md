![desker](assets/desker.png)

Desktop Elements Recognition

- [Installation](#installation)
- [API documentation](#api-documentation)
- [Development guide](#development-guide)
    - [IDE](#ide)
    - [Architecture](#architecture)
    - [Code documentation](#code-documentation)
    - [Tests](#tests)
- [Models](#models)
    - [Managing trained models](#managing-trained-models)
    - [KNN model for login detection](#knn-model-for-login-detection)

## Installation

If you have access to this README, it means that you are a **developer**. To get the latest `desker` package, you should download
the artifacts from the latest successful build (see https://gitlab.com/d3sker/desker/-/pipelines).

It is an archive containing a single wheel file. You have to extract and install it:
```bash
pip3 install desker-1.0a0-py3-none-any.whl
```

## Basic usage

`desker` gathers several independent components. Depending on your task, 

### Desktop elements recognition

You can invoke the `faster_rcnn` module to detect
some elements from desktop screenshots. The internal
model is mainly trained on Linux screenshots so it is 
very likely to fail on other environment.

```python
from desker.faster_rcnn import load_model, predict_elements_demo
from PIL import Image

# import the model
load_model()

# load a test image
img = Image.open("tests/resources/icon_images/test_img/0056_screenshot.png").convert("RGB")

# run the model
ann_img = predict_elements_demo(img)

# show
ann_img.show()
```

The output may be like:
![faster_rcnn output](assets/0056_screenshot_annotated.png)

You can also get the raw results (bounding boxes, labels and confidence) by calling `predict_elements`.

### 

## Desker As A Service

Experimental feature

## API documentation

The API documentation is now automatically built by the CI. You can either download it with the CI artifacts or you can also build it locally

```bash
# install build deps
pip3 install sphinx sphinx-rtd-theme numpydoc
# build
python3 setup.py prepare_sphinx build_sphinx
```

The docs are built in the HTML format and are located to `docs/build/html/`.


## Development guide

### IDE

We recommend to use [Visual Studio Code](https://code.visualstudio.com/) with the main python plugin (`ms-python.python`).

To ensure a good code quality, you must use (at least) the following settings (file `.vscode/settings.json`):

```javascript
{
    "python.sortImports.path": "isort",
    "python.sortImports.args": [
        "--line-width",
        "79",
        "--project",
        "desker"
    ],
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "editor.formatOnSave": true,
    "python.formatting.provider": "autopep8",
    "python.formatting.autopep8Args": [
        "-a",
        "-a",
        "-a",
        "--max-line-length",
        "79"
    ],
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--max-line-length",
        "79",
        "--per-file-ignores",
        "__init__.py:F401",
        "--ignore",
        "ANN101,ANN204"
    ],
    "python.pythonPath": "/usr/bin/python3"
}
```

To make these settings work, you must have up-to-date versions of `flake8`, `autopep8` and `isort`.

```bash
pip3 install flake8 autopep8 isort --upgrade
```

### Architecture


#### Project layout

The `desker` library is composed of several sub-libraries: `ocr`, `faster_rcnn` and `login` currently. A sub-library can be defined once a new *task* (detect icons, work on text, detect login page...) has to be implemented in `desker`.
The term *task* is rather hazy, so you should first think about integrating your code in existing sub-libraries. 

These sub-packages are independent and **must not call each other**.


#### Code patterns

##### Public API

Sub-packages contain a `__init__.py` file which must gather *public* functions, i.e. functions you want to expose to end-users.

As an example, consider the following structure:
```console
desker/
    __init__.py
    my_task/
        __init__.py
        train.py
        predict.py
        utils.py
```

The sub-package `my_task` has several files with several functions (and classes maybe) but in practice you may want the user to use only few of them. 
These public objects must be imported in the `__init__.py` file.
In addition, we do declare the API with the `__all__` variable. The public objects must then be added to this list. Finally, the `desker/my_task/__init__.py` may look like this:
```python
# import public stuff
from .predict import predict_everything 
from .predict import predict_single 

# declare public stuff (it is very important
# for the documentation right now)
__all__ = [predict_everything.__name__,
           predict_single.__name__]
```


Finally, these functions can be imported as below.
```python
from desker.my_task import predict_everything
from desker.my_task import predict_single
# you can also import everything, but this is
# not advised.
# from desker.my_task import *
```

Currently sub-packages expose **functions only** (no class). This choice is not immutable but developers should try to follow this paradigm and limit the numbers of classes.

##### Global variables

However, some code uses global variable (ML model generally). 
When the model is quite heavy (like Faster-R-CNN), the model cannot be loaded at import time. 
The library must then implement a `load` (or `init`) function which imports it on demand.
Currently, the following pattern is used:

```python
# ML model as global variable
# not defined at import time
__model__ = None

def load_model(file: str):
    global __model__
    __model__ = get_model(file)
```

Inside the functions requiring the model, we can use the global model by default. For this purpose, two patterns exist:

* Replace `None`: the model to use is optional and the function use the global model if it is not provided.

```python
def predict_everything(img: ImageType, model : Optional[Model] = None):
    model = model if model else __model__
    if model is None:
        raise ValueError("Default model is not loaded, you must either load it or provide a custom one")
```

* Decorate: the default model is given as default parameters but since default parameters are evaluated once, a decorator must be used to re-evaluate `__model__` when the function is called (at the very beginning `__model__ = None`).

```python
def use_global_model_if_not_provided(f: Callable) -> Callable:
    """
    Basic decorator to set the model as the default model
    if the latter is not provided (i.e. 'model = None')
    """
    @wraps(f)
    def new(*args, **kwargs):
        # the parameter 'model' is set to __model__
        # by default (i.e. if it is not provided)
        kwargs.setdefault("model", __model__)
        return f(*args, **kwargs)
    return new

@use_global_model_if_not_provided
def predict_everything(img: ImageType, model : Model = __model__):
    if model is None:
        raise ValueError("Default model is not loaded, you must either load it or provide a custom one")
        
```

Obviously the last way is to create a class (with a kind of singleton pattern) which loads the model when instantiated.

```python
class MyModel:
    def __init__(self):
        # loads the model here
        self.__model__ = 

    def predict_everything(self, img: ImageType):
        # use the model
        self.__model__...
```

### Code documentation

#### Docstring

Documenting the code is paramount. In particular, functions of the public API must be documented (with the `numpy` docstring, see https://numpydoc.readthedocs.io/en/latest/format.html).

```python
def public_function(param_1 : type, param_2 : type) -> return_type:
    """
    This function is public and does the job

    Parameters
    ----------

    param_1 : type
        the value of the first parameter
    param_2 : type
        the value of the second parameter

    Returns
    -------
    dict
        Result of the function with the following structure:
        {
            "value" : int, # main value
            ...
        }

    Notes
    -----
    Additional notes about this function

    """
```

#### Python types

Python is not statically typed, but providing types in the function prototypes really helps the developers. So an effort must be made to provide them (parameters and returned values).

Do not hesitate to import a class even though it is used for type annotation only.
```python
from PIL.Image import Image as ImageType

def function(img : ImageType) -> float:
    ...
```

---
**Notes**

Be careful with library `PIL`. The object `PIL.Image` is a submodule which contains the functions `PIL.Image.open` and `PIL.Image.fromarray` for instance. It must not be confused with `PIL.Image.Image` which is the real image object.
Thus we advise to do as below:

```python
from PIL import Image
from PIL.Image import Image as ImageType

# Now you can open an image with
# img = Image.open(...)
# If you want to annotate functions, you use the ImageType
# def function(img: ImageType):
#   ...
```

---

Also, you should have a look to the `typing` package that provides richer types (see https://docs.python.org/3/library/typing.html).

```python
from typing import Dict
from typing import Union
from typing import List
from typing import Optional

# The input argument is a dictionnary with string 
# keys and integer values
def function(d : Dict[str, int]) -> int:
    ...

# The input argument is a list of numbers 
# (integers or float) and returns nothing
def function_2(l : List[Union[int, float]]) -> None:
    ...

# The input argument is a string which is optional
# (it may not be defined) and returns two integers
def function_3(o : Optional[str] = "default") -> (int, int):
    ...
```

### Tests

You should **test your functions**. For this purpose, `desker` uses `pytest`, so first you must ensure that it is up-to-date:

```bash
pip3 install pytest --upgrade
```

Tests must be put inside the `tests/` directory. They consist of files `test_xxx.py` gathering several functions `test_xxx()`. These functions are executed when you run the following command:

```bash
python3 -m pytest
```

The folder `tests/resources` gathers test materials (images, configuration files ...). Only these elements must be used to test your functions (do not use data from the outside).

## Models

### Managing trained models

Models can be rather heavy, so it is hard to track these file through `git`. However, we can use `git-lfs` to handle them (LFS: Large File Storage).

First you must install the `git-lfs` command
```bash
sudo apt install git-lfs
```

When you pull the repository, you have a `.gitattributes` file which stores information about tracked files. Currently, it looks like:
```txt
*.cnn filter=lfs diff=lfs merge=lfs -text
*.knn filter=lfs diff=lfs merge=lfs -text
*.nn filter=lfs diff=lfs merge=lfs -text
*.frcnn filter=lfs diff=lfs merge=lfs -text
```

Briefly, the ML models are tracked (so be careful with the file extensions). You can track a new file through
```bash
git lfs track <regexp>
```

By default, heavy files are not fetched when you clone or pull. You must use the `git-lfs` command to *force* the models update.
```bash
git lfs fetch origin master
```

### KNN model for login detection

`desker` embeds a simple `k`-nearest-neighbors (KNN) algorithm to detect OS from login page.
This model is purely supervised and the training dataset is located in [tests/resources/login](https://gitlab.com/d3sker/desker/-/tree/master/tests/resources/login). 
This folder contains about 20 screenshots and a csv file which stores labels:

```csv
img,vm,label
0000_screenshot.png,4,ubuntu-kde
0001_screenshot.png,4,ubuntu-kde
0002_screenshot.png,1,ubuntu-gnome
0003_screenshot.png,1,ubuntu-gnome
...
```

**Adding new screenshots**. You may need to detect more systems or to make the prediction more robust. So you can add new screenshots before re-training the model.
To add a new screenshot, you just have to put it on [tests/resources/login](https://gitlab.com/d3sker/desker/-/tree/master/tests/resources/login) and update the `labels.csv` file located in the same folder.
The two important columns are `img` (the name of the file) and `label` (the system to detect). The `vm` attribute is 
an artifact which behaves like a label. Therefore, two cases raise:

* The label you add already exists: you have to use the same `vm` value
* You add a new label: you must define a new `vm` value (you merely increment the greatest one)

**Training the model**. Once you have added new screenshots you must re-train the model. 
Usually, we train a new model and we test that this model is ok. Actually, `pytest` can train and test (with your new data) before putting it into production.

```bash
python3 -m pytest -xvs tests/test_login.py
```

If these are passed, it means that the model can be trained and saved at the default location.
For this, you only have to invoke the `train.py` command:
```bash
python3 desker/login/knn/train.py -o desker/login/knn/model.knn -l tests/resources/login/labels.csv tests/resources/login/
```

It trains a new KNN model based on files located at `tests/resources/login/` with label file `tests/resources/login/labels.csv`. The output model is saved at `desker/login/knn/model.knn` (the default model location).

