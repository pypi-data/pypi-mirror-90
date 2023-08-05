# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wasm_spec_kernel']

package_data = \
{'': ['*']}

install_requires = \
['pexpect>=4.8.0,<5.0.0']

setup_kwargs = {
    'name': 'wasm-spec-kernel',
    'version': '0.1.0',
    'description': 'A wasm kernel for Jupyter',
    'long_description': "# Wasm Spec Kernel\n\nA Jupyter kernel for the WebAssembly reference interpreter (see [webassembly/spec](https://github.com/WebAssembly/spec)).\n\n## Installation\n\n### Wasm Reference Interpreter\n\nThis kernel requires a [Wasm reference interpreter](https://github.com/WebAssembly/spec/tree/master/interpreter) to be available in the environment (e.g. the Wasm interpreter is not distributed with this Python package).\n\nYou can clone a WebAssembly spec repo and build the interpreter yourself using the OCaml toolchain.\n\n@awendland provides a pre-compiled variant of the Wasm reference interpreter with language extensions for abstract types at [awendland/webassembly-spec-abstypes](https://github.com/awendland/webassembly-spec-abstypes).\n\n#### Configuration\n\nEither:\n\n* Place the interpreter in your `$PATH` with the name `wasm`, or\n* Specify the interpreter's location when installing the kernel with `python -m wasm_spec_kernel.install --interpreter wherever_you_stored_the/interpreter`\n\n### Jupyter Kernel\n\nTo install:\n\n```shell\npip install wasm_spec_kernel\npython -m wasm_spec_kernel.install\n```\n\nTo use it, open up a new Jupyter notebook. For example, via:\n\n```shell\njupyter notebook\n# In the notebook interface, select Wasm from the 'New' menu\njupyter qtconsole --kernel wasm_spec\njupyter console --kernel wasm_spec\n```\n\n# Purpose\n\nThis exists because the WebAssembly reference interpreter is written in OCaml and OCaml is difficult to compile to WebAssembly (otherwise the latest reference interpreter could be hosted via v1 WebAssembly already available in evergreen web browsers). A Jupyter kernel should assist with sharing WebAssembly code samples leveraging features from the various forks of the WebAssembly specification.\n\n## How This Works\n\nFor details of how this works, see the Jupyter docs on [wrapper kernels](http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html), and Pexpect's docs on the [replwrap module](http://pexpect.readthedocs.org/en/latest/api/replwrap.html). Note that this kernel reimplements the `pexpect.replwrap.REPLWrapper` class so that it works better with the Wasm reference interpreter.\n\n## Acknowledgements\n\nThis was based on [bash_kernel](https://github.com/takluyver/bash_kernel) by Thomas Kluyver. Tests were adapted from [jupyter/jupyter_client](https://github.com/jupyter/jupyter_client) and [ipython/ipykernel](https://github.com/ipython/ipykernel)\n",
    'author': 'Alex Wendland',
    'author_email': 'me@alexwendland.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/awendland/wasm_spec_kernel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
