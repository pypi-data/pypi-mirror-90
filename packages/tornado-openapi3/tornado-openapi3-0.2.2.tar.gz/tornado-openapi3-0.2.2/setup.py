# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tornado_openapi3']

package_data = \
{'': ['*']}

install_requires = \
['openapi-core>=0.13.4,<0.14.0', 'tornado>=4,<7']

setup_kwargs = {
    'name': 'tornado-openapi3',
    'version': '0.2.2',
    'description': 'Tornado OpenAPI 3 request and response validation library',
    'long_description': '===================\n Tornado OpenAPI 3\n===================\n\n.. image:: https://travis-ci.com/correl/tornado-openapi3.svg?branch=master\n    :target: https://travis-ci.com/correl/tornado-openapi3\n.. image:: https://codecov.io/gh/correl/tornado-openapi3/branch/master/graph/badge.svg?token=CTYWWDXTL9\n    :target: https://codecov.io/gh/correl/tornado-openapi3\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n\nTornado OpenAPI 3 request and response validation library.\n\nProvides integration between the `Tornado`_ web framework and `Openapi-core`_\nlibrary for validating request and response objects against an `OpenAPI 3`_\nspecification.\n\nUsage\n=====\n\nAdding validation to request handlers\n-------------------------------------\n\n.. code:: python\n\n    from openapi_core import create_spec  # type: ignore\n    from openapi_core.exceptions import OpenAPIError  # type: ignore\n    from openapi_core.deserializing.exceptions import DeserializeError  # type: ignore\n    from openapi_core.schema.media_types.exceptions import (  # type: ignore\n        InvalidContentType,\n    )\n    from openapi_core.unmarshalling.schemas.exceptions import ValidateError  # type: ignore\n    from tornado.web import RequestHandler\n    from tornado_openapi3 import RequestValidator\n    import yaml\n\n\n    class OpenAPIRequestHandler(RequestHandler):\n        async def prepare(self) -> None:\n            maybe_coro = super().prepare()\n            if maybe_coro and asyncio.iscoroutine(maybe_coro):  # pragma: no cover\n                await maybe_coro\n\n            spec = create_spec(yaml.safe_load(self.render_string("openapi.yaml")))\n            validator = RequestValidator(spec)\n            result = validator.validate(self.request)\n            try:\n                result.raise_for_errors()\n            except InvalidContentType:\n                self.set_status(415)\n                self.finish()\n            except (DeserializeError, ValidateError) as e:\n                self.set_status(400)\n                self.finish()\n            except OpenAPIError:\n                raise\n\nValidating a response\n---------------------\n\n.. code:: python\n\n    from tornado.testing import AsyncHTTPTestCase\n    from tornado_openapi3 import ResponseValidator\n\n    from myapplication import create_app, spec\n\n\n    class TestResponses(AsyncHTTPTestCase):\n        def get_app(self) -> Application:\n            return create_app()\n\n        def test_status(self) -> None:\n            validator = ResponseValidator(spec)\n            response = self.fetch("/status")\n            result = validator.validate(response)\n            result.raise_for_errors()\n\nContributing\n============\n\nGetting Started\n---------------\n\nThis project uses `Poetry`_ to manage its dependencies. To set up a local\ndevelopment environment, just run:\n\n.. code:: sh\n\n    poetry install\n\nFormatting Code\n---------------\n\nThe `Black`_ tool is used by this project to format Python code. It is included\nas a development dependency, and should be run on all committed code. To format\ncode prior to committing it and submitting a PR, run:\n\n.. code:: sh\n\n    poetry run black .\n\nRunning Tests\n-------------\n\n`pytest`_ is the preferred test runner for this project. It is included as a\ndevelopment dependency, and is configured to track code coverage, `Flake8`_\nstyle compliance, and `Black`_ code formatting. Tests can be run in your\ndevelopment environment by running:\n\n.. code:: sh\n\n    poetry run pytest\n\nAdditionally, tests can be run using `tox`_, which will run the tests using\nmultiple versions of both Python and Tornado to ensure broad compatibility.\n\nConfiguring Hypothesis\n^^^^^^^^^^^^^^^^^^^^^^\n\nMany of the tests make use of `Hypothesis`_ to specify their expectations and\ngenerate a large volume of randomized test input. Because of this, the tests may\ntake a long time to run on slower computers. Two profiles are defined for\nHypothesis to use which can be selected by setting the ``HYPOTHESIS_PROFILE``\nenvironment variable to one of the following values:\n\n``default``\n  Runs tests using the default Hypothesis settings (100 examples per test) and\n  no completion deadline.\n\n``dev``\n  The fastest profile, meant for local development only. Uses only 10 examples\n  per test with no completion deadline.\n\n\n.. _Black: https://github.com/psf/black\n.. _Flake8: https://flake8.pycqa.org/\n.. _Hypothesis: https://hypothesis.readthedocs.io/\n.. _OpenAPI 3: https://swagger.io/specification/\n.. _Openapi-core: https://github.com/p1c2u/openapi-core\n.. _Poetry: https://python-poetry.org/\n.. _Tornado: https://www.tornadoweb.org/\n.. _pytest: https://pytest.org/\n.. _tox: https://tox.readthedocs.io/\n',
    'author': 'Correl Roush',
    'author_email': 'correl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/correl/tornado-openapi3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
