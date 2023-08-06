# Mars InSight API Client

A python client to provide easy access to NASA's InSight: Mars Weather Service API. 

![CI](https://github.com/AlbertWigmore/mars-insight/workflows/CI/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/mars-insight/badge/?version=latest)](https://mars-insight.readthedocs.io/en/latest/?badge=latest)


## Installation

```bash
pip install mars-insight
```


## Documentation

Documentation available at: [readthedocs](https://mars-insight.readthedocs.io/en/latest/index.html#mars-insight)


## Quick Start

```python
from mars_weather.api import Client

client = Client('api_key')

data = client.get_data()
```
