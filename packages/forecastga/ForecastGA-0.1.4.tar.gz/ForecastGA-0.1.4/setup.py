# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['forecastga',
 'forecastga.ga',
 'forecastga.ga.auth',
 'forecastga.ga.utils',
 'forecastga.helpers',
 'forecastga.models']

package_data = \
{'': ['*'], 'forecastga': ['stan/unix/*', 'stan/win/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'Werkzeug>=1.0.1,<2.0.0',
 'addressable>=1.4.2,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'fbprophet>=0.7.1,<0.8.0',
 'gluonts>=0.6.4,<0.7.0',
 'google-api-core>=1.24.1,<2.0.0',
 'google-api-python-client>=1.12.8,<2.0.0',
 'google-auth-httplib2>=0.0.4,<0.0.5',
 'google-auth>=1.24.0,<2.0.0',
 'holidays>=0.10.4,<0.11.0',
 'httplib2>=0.18.1,<0.19.0',
 'inspect-it>=0.3.2,<0.4.0',
 'keyring>=21.8.0,<22.0.0',
 'lightgbm>=3.1.1,<4.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'mxnet>=1.7.0,<2.0.0',
 'nbeats-pytorch>=1.3.1,<2.0.0',
 'numpy==1.19.3',
 'oauth2client>=4.1.3,<5.0.0',
 'pandas==1.1.0',
 'pmdarima>=1.8.0,<2.0.0',
 'prettytable>=2.0.0,<3.0.0',
 'pylev>=1.3.0,<2.0.0',
 'pystan>=2.19.1,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'rsa>=4.6,<5.0',
 'scikit-learn>=0.24.0,<0.25.0',
 'scipy==1.5.0',
 'seasonal>=0.3.1,<0.4.0',
 'snakify>=1.1.1,<2.0.0',
 'statsmodels>=0.12.1,<0.13.0',
 'tbats>=1.1.0,<2.0.0',
 'torch>=1.7.1,<2.0.0',
 'tqdm>=4.55.1,<5.0.0',
 'tsfresh>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'forecastga',
    'version': '0.1.4',
    'description': 'A Python tool to forecast GA data using several popular timeseries models',
    'long_description': '# ForecastGA\nA Python tool to forecast GA data using several popular timeseries models.\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1nmcu37MY02dfMdUbinrwwg7gA9ya3eud?usp=sharing)\n\n\n## About\n\n### Welcome to ForecastGA\n\nForecastGA is a tool that combines a couple of popular libraries, [Atspy](https://github.com/firmai/atspy) and [googleanalytics](https://github.com/debrouwere/google-analytics), with a few enhancements.\n\n* The models are made more intuitive to upgrade and add by having the tool logic separate from the model training and prediction.\n* When calling `am.forecast_insample()`, any kwargs included (e.g. `learning_rate`) are passed to the train method of the model.\n* Google Analytics profiles are specified by simply passing the URL (e.g. https://analytics.google.com/analytics/web/?authuser=2#/report-home/aXXXXXwXXXXXpXXXXXX).\n* You can provide a `data` dict with GA config options or a Pandas Series as the input data.\n* Multiple log levels.\n* Auto GPU detection (via Torch).\n* List all available models, with descriptions, by calling `forecastga.print_model_info()`.\n* Google API info can be passed in the `data` dict or uploaded as a JSON file named `identity.json`.\n* Created a companion Google Colab notebook to easily run on GPU.\n* A handy plot function for Colab, `forecastga.plot_colab(forecast_in, title="Insample FOrecast", dark_mode=True)` that formats nicely and also handles Dark Mode!\n\nTo use:\n\n#### Find Model Info:\n`forecastga.print_model_info()`\n\n#### Initialize Model:\n\n##### Google Analytics:\n\n```\ndata = { \'client_id\': \'<google api client_id>\',\n         \'client_secret\': \'<google api client_secret>\',\n         \'identity\': \'<google api identity>\',\n         \'ga_start_date\': \'2018-01-01\',\n         \'ga_end_date\': \'2019-12-31\',\n         \'ga_metric\': \'sessions\',\n         \'ga_segment\': \'organic traffic\',\n         \'ga_url\': \'https://analytics.google.com/analytics/web/?authuser=2#/report-home/aXXXXXwXXXXXpXXXXXX\',\n         \'omit_values_over\': 2000000\n        }\n\nmodel_list = ["TATS", "TBATS1", "TBATP1", "TBATS2", "ARIMA"]\nam = forecastga.AutomatedModel(data , model_list=model_list, forecast_len=30 )\n```\n\n##### Pandas DataFrame:\n\n```\ndata = pd.read_csv(\'ts.csv\').sessions\n\nmodel_list = ["TATS", "TBATS1", "TBATP1", "TBATS2", "ARIMA"]\nam = forecastga.AutomatedModel(data , model_list=model_list, forecast_len=30 )\n```\n\n#### Forecast Insample:\n`forecast_in, performance = am.forecast_insample()`\n\n#### Forecast Outsample:\n`forecast_out = am.forecast_outsample()`\n\n#### Ensemble Performance:\n`all_ensemble_in, all_ensemble_out, all_performance = am.ensemble(forecast_in, forecast_out)`\n\n#### Pretty Plot in Google Colab\n`forecastga.plot_colab(forecast_in, title="Insample FOrecast", dark_mode=True)`\n\n\n# Installation\nWindows users may need to manually install the two items below via conda :\n1. `conda install pystan`\n1. `conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch`\n1. `!pip install --upgrade git+https://github.com/jroakes/ForecastGA.git`\n\notherwise,\n`!pip install --upgrade git+https://github.com/jroakes/ForecastGA.git`\n\nThis repo support GPU training. Below are a few libraries that may have to be manually installed to support.\n`pip install --upgrade mxnet-cu101==1.7.0`\n\n\n## Acknowledgements\n\n1. Majority of forecasting code taken from https://github.com/firmai/atspy and refactored heavily.\n1. Google Analytics based off of: https://github.com/debrouwere/google-analytics\n\n## Contribute\nThe goal of this repo is to grow the list of available models to test.  If you would like to contribute one please read on.  Feel free to have fun naming your models.\n\n1. Fork the repo.\n2. In the `/src/forecastga/models` folder there is a model called `template.py`.  You can use this as a template for creating your new model.  All available variables are there. Forecastga ensures each model has the right data and calls only the `train` and `forecast` methods for each model. Feel free to add additional methods that your model requires.\n3. Edit the `/src/forecastga/models/__init__.py` file to add your model\'s information.  Follow the format of the other entries.  Forecastga relies on `loc` to find the model and `class` to find the class to use.\n4. Edit `requirments.txt` with any additional libraries needed to run your model.  Keep in mind that this repo should support GPU training if available and some libraries have separate GPU-enabled versions.\n5. Issue a pull request.\n\nIf you enjoyed this tool consider buying me some beer at: [Paypalme](https://www.paypal.com/paypalme/codeseo)\n',
    'author': 'JR Oakes',
    'author_email': 'jroakes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jroakes/ForecastGA',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
