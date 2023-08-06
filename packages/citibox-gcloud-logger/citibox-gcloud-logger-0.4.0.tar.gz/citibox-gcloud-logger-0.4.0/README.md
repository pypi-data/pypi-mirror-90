# gcloud-logger
Python log wrapper for gcloud logging format

## How to use it?

Create your filter classes as needed, extending BaseContextFilter i.e.
````python
from citibox.gcloudlogger import BaseContextFilter


class MyTestFilter(BaseContextFilter):
    def __init__(self):
        super().__init__()
        self.some_attribute = "Some Value"
    
    @staticmethod
    def filter_name():
        return "my_test_filter"


    def to_dict(self) -> dict:
        return {
            "some_attribute": self.some_attribute
        }
````

Get logger from generated dict:
1. Import logging required
    ```python
    import logging
    from logging.config import dictConfig
    ```
2. Import GCloudLogConfig:
    ```python
    from citibox.gcloudlogger import GCloudLogConfig
    ```

3. Instance the library with your custom filters and set the logger config:
    ```python
    my_log_config = GCloudLogConfig(MyTestFilter)
    dictConfig(my_log_config.config)
    ```
4. Use the logger as normally:
    ```python
   logger = logging.getLogger()
   
   logger.info("something good is happening")
    ```
   
 Also, you can add more loggers if needed:
 ```python
    import logging
    from logging.config import dictConfig
    from citibox.gcloudlogger import GCloudLogConfig

    my_log_config = GCloudLogConfig(AnyFilter)
    my_log_config.add_logger("new_logger", level=logging.INFO)
    dictConfig(my_log_config.config) 
```

And, add filters after the creation of the log config class:
```python
    import logging
    from logging.config import dictConfig
    from citibox.gcloudlogger import GCloudLogConfig

    my_log_config = GCloudLogConfig(AnyFilter)
    my_log_config.add_filter(AnotherFilterClass)
```

### Using Middlewares
#### Falcon
There is a Falcon middleware ready for logging Request and Response.
Use [Falcon middlewares](https://falcon.readthedocs.io/en/stable/api/middleware.html) adding the included class:
```python
import falcon
from citibox.gcloudlogger.contrib.falcon import FalconMiddleware

app = falcon.API(middleware=[FalconMiddleware()])
```

#### Django
in your config file add:
```python
MIDDLEWARE = [
    'citibox.gcloudlogger.contrib.django.DjangoMiddleware',
    ...
]
```
