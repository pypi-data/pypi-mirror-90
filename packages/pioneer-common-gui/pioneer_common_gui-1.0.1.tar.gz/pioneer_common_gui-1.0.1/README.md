# pioneer.common.gui

pioneer.common.ui is a python gui library regrouping all graphical utilities needed by pioneer.das.view and other applications.


## Installation

Before installing, you should add to your pip.conf file the gitlab pypi server urls as extra index url, and also trust the gitlab host.

```conf
[global]
extra-index-url =   https://pioneer:yK6RUkhUCNHg3e1yxGT4@svleddar-gitlab.leddartech.local/api/v4/projects/481/packages/pypi/simple
                    https://pioneer:yK6RUkhUCNHg3e1yxGT4@svleddar-gitlab.leddartech.local/api/v4/projects/488/packages/pypi/simple
trusted-host = svleddar-gitlab.leddartech.local
```

Use the package manager [pip](https://pioneer:yK6RUkhUCNHg3e1yxGT4@svleddar-gitlab.leddartech.local/api/v4/projects/488/packages/pypi/simple/pioneer-common-gui) to install pioneer.common.gui

```bash
pip install pioneer-common-gui
```
** Prerequisites **
To setup pioneer.common.gui in develop mode, you need to have installed **cmake** beforehand.

When developing, you can link the repository to your python site-packages and enable hot-reloading of the package
```bash
python3 setup.py develop --user
```

If you don't want to install all the dependencies on your computer, you can run it in a virtual environment as well.
```bash
pipenv install --skip-lock

pipenv shell
```

## Usage

To run the dasview in the virtual environment, you can use the run command
```python
from pioneer.common.gui import Actors

```
