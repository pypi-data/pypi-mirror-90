# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grpc_interceptor',
 'grpc_interceptor.testing',
 'grpc_interceptor.testing.protos']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.8.0,<2.0.0']

extras_require = \
{'testing': ['protobuf>=3.6.0']}

setup_kwargs = {
    'name': 'grpc-interceptor',
    'version': '0.13.0',
    'description': 'Simplifies gRPC interceptors',
    'long_description': '[![Tests](https://github.com/d5h-foss/grpc-interceptor/workflows/Tests/badge.svg)](https://github.com/d5h-foss/grpc-interceptor/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/d5h-foss/grpc-interceptor/branch/master/graph/badge.svg)](https://codecov.io/gh/d5h-foss/grpc-interceptor)\n[![Read the Docs](https://readthedocs.org/projects/grpc-interceptor/badge/)](https://grpc-interceptor.readthedocs.io/)\n[![PyPI](https://img.shields.io/pypi/v/grpc-interceptor.svg)](https://pypi.org/project/grpc-interceptor/)\n\n# Summary\n\nSimplified Python gRPC interceptors.\n\nThe Python `grpc` package provides service interceptors, but they\'re a bit hard to\nuse because of their flexibility. The `grpc` interceptors don\'t have direct access\nto the request and response objects, or the service context. Access to these are often\ndesired, to be able to log data in the request or response, or set status codes on the\ncontext.\n\n# Installation\n\nTo just get the interceptors (and probably not write your own):\n\n```console\n$ pip install grpc-interceptor\n```\n\nTo also get the testing framework, which is good if you\'re writing your own interceptors:\n\n```console\n$ pip install grpc-interceptor[testing]\n```\n\n# Usage\n\n## Server Interceptor\n\nTo define your own interceptor (we can use `ExceptionToStatusInterceptor` as an example):\n\n```python\nfrom grpc_interceptor import ServerInterceptor\nfrom grpc_interceptor.exceptions import GrpcException\n\nclass ExceptionToStatusInterceptor(ServerInterceptor):\n    def intercept(\n        self,\n        method: Callable,\n        request: Any,\n        context: grpc.ServicerContext,\n        method_name: str,\n    ) -> Any:\n        """Override this method to implement a custom interceptor.\n         You should call method(request, context) to invoke the\n         next handler (either the RPC method implementation, or the\n         next interceptor in the list).\n         Args:\n             method: The next interceptor, or method implementation.\n             request: The RPC request, as a protobuf message.\n             context: The ServicerContext pass by gRPC to the service.\n             method_name: A string of the form\n                 "/protobuf.package.Service/Method"\n         Returns:\n             This should generally return the result of\n             method(request, context), which is typically the RPC\n             method response, as a protobuf message. The interceptor\n             is free to modify this in some way, however.\n         """\n        try:\n            return method(request, context)\n        except GrpcException as e:\n            context.set_code(e.status_code)\n            context.set_details(e.details)\n            raise\n```\n\nThen inject your interceptor when you create the `grpc` server:\n\n```python\ninterceptors = [ExceptionToStatusInterceptor()]\nserver = grpc.server(\n    futures.ThreadPoolExecutor(max_workers=10),\n    interceptors=interceptors\n)\n```\n\nTo use `ExceptionToStatusInterceptor`:\n\n```python\nfrom grpc_interceptor.exceptions import NotFound\n\nclass MyService(my_pb2_grpc.MyServiceServicer):\n    def MyRpcMethod(\n        self, request: MyRequest, context: grpc.ServicerContext\n    ) -> MyResponse:\n        thing = lookup_thing()\n        if not thing:\n            raise NotFound("Sorry, your thing is missing")\n        ...\n```\n\nThis results in the gRPC status status code being set to `NOT_FOUND`,\nand the details `"Sorry, your thing is missing"`. This saves you the hassle of\ncatching exceptions in your service handler, or passing the context down into\nhelper functions so they can call `context.abort` or `context.set_code`. It allows\nthe more Pythonic approach of just raising an exception from anywhere in the code,\nand having it be handled automatically.\n\n## Client Interceptor\n\nWe will use an invocation metadata injecting interceptor as an example of defining\na client interceptor:\n\n```python\nfrom grpc_interceptor import ClientCallDetails, ClientInterceptor\n\nclass MetadataClientInterceptor(ClientInterceptor):\n\n    def intercept(\n        self,\n        method: Callable,\n        request_or_iterator: Any,\n        call_details: grpc.ClientCallDetails,\n    ):\n        """Override this method to implement a custom interceptor.\n\n        This method is called for all unary and streaming RPCs. The interceptor\n        implementation should call `method` using a `grpc.ClientCallDetails` and the\n        `request_or_iterator` object as parameters. The `request_or_iterator`\n        parameter may be type checked to determine if this is a singluar request\n        for unary RPCs or an iterator for client-streaming or client-server streaming\n        RPCs.\n\n        Args:\n            method: A function that proceeds with the invocation by executing the next\n                interceptor in the chain or invoking the actual RPC on the underlying\n                channel.\n            request_or_iterator: RPC request message or iterator of request messages\n                for streaming requests.\n            call_details: Describes an RPC to be invoked.\n\n        Returns:\n            The type of the return should match the type of the return value received\n            by calling `method`. This is an object that is both a\n            `Call <https://grpc.github.io/grpc/python/grpc.html#grpc.Call>`_ for the\n            RPC and a `Future <https://grpc.github.io/grpc/python/grpc.html#grpc.Future>`_.\n\n            The actual result from the RPC can be got by calling `.result()` on the\n            value returned from `method`.\n        """\n        new_details = ClientCallDetails(\n            call_details.method,\n            call_details.timeout,\n            [("authorization", "Bearer mysecrettoken")],\n            call_details.credentials,\n            call_details.wait_for_ready,\n            call_details.compression,\n        )\n\n        return method(request_or_iterator, new_details)\n```\n\nNow inject your interceptor when you create the ``grpc`` channel:\n\n```python\ninterceptors = [MetadataClientInterceptor()]\nwith grpc.insecure_channel("grpc-server:50051") as channel:\n    channel = grpc.intercept_channel(channel, *interceptors)\n    ...\n```\n\nClient interceptors can also be used to retry RPCs that fail due to specific errors, or\na host of other use cases. There are some basic approaches in the tests to get you\nstarted.\n\n# Documentation\n\nRead the [complete documentation here](https://grpc-interceptor.readthedocs.io/).\n',
    'author': 'Dan Hipschman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d5h-foss/grpc-interceptor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
