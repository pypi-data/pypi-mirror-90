"""
    Copyright 2020 LXPER Inc.
    REFERENCE: Engine(공통함수)
    DESIGNER: LXPER Development Team
    TECHNICAL WRITER: LXPER Development Team
    VERSION: 2.0

    ATM v2 API Protocol Compliant Client
    
    This script is designed to communicate with 
    the ATM Code Standard(Chan Woo Kim, Jung Jung Ho) compliant ATM v2 API
    Developers can use this module to conveniently utilize the various engines 
    and shared functions in the LXPER Kubernetes on-premises environment.

    >>> from atmclient import client
    >>> client.<tab>
    
"""

__version__ = "0.1.3"


__LOGO__ = \
"""
     _  _____ __  __    ____ _     ___ _____ _   _ _____ 
    / \|_   _|  \/  |  / ___| |   |_ _| ____| \ | |_   _|
   / _ \ | | | |\/| | | |   | |    | ||  _| |  \| | | |  
  / ___ \| | | |  | | | |___| |___ | || |___| |\  | | |  
 /_/   \_|_| |_|  |_|  \____|_____|___|_____|_| \_| |_|  
                                                         
pip install atmclient=={__version__}
""".format(__version__=__version__)

# python standard libraries
import os
import warnings
import time
import traceback
import subprocess
import json

from typing import Dict, List
from collections import defaultdict

# third party libraries
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pydantic import BaseSettings
from easydict import EasyDict

################################################################################
# Section A. Helper Classes and functions
################################################################################

def _get_exception_message(exc):
    return exc.args[0] if len(exc.args) > 0 else ""

def _get_exception_type(exc):
    return type(exc).__name__

def _get_exception(exc):
    return f"{_get_exception_type(exc)}: {_get_exception_message(exc)}"

def _get_nvidia_smi():
    try:
        stdout = subprocess.check_output(["nvidia-smi"], timeout=3, universal_newlines=True)
        return stdout
    except:
        return ""

class ATMError(Exception):
    """Base exception for the project"""

class ATMServerError(ATMError):
    """Exception to indicate server misbehaved."""
    
class ATMClientError(ATMError):
    """Exception to indicate client wrongly send the request."""

class ATMUnsuitablePassageError(ATMError):
    """Exception to indicate the given passage is not fit with the task"""

class ATMInvalidOptionError(ATMError):
    """Exception to indicate the given option is not valid"""

class ATMUnexpectedError(ATMError):
    """Exception to indicate the current error is not expected by developers"""
    def __init__(self, exc):
        message = "{exc_type}: {exc_msg}\n{exc_traceback}".format(
            exc_type=_get_exception_type(exc),
            exc_msg=_get_exception_message(exc),
            exc_traceback=traceback.format_exc()
        )
        super().__init__(message)
        
class ATMResult(EasyDict):
    """Result container for server responses"""
    pass


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 15
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

################################################################################
# Section B. Client related Classes
################################################################################
    
class ClientArgs(BaseSettings):
    gateway_route_discovery_url: str = "http://atm-api-gateway.atm.svc.cluster.local:8080/{endpoint_id}/"
    gateway_route_generate_url: str = "http://atm-api-gateway.atm.svc.cluster.local:8080/{endpoint_id}/generate"
    gateway_route_list_url: str = "http://atm-api-gateway.atm.svc.cluster.local:8080/actuator/gateway/routes"
    timeout: int = 60
    max_retry: int = 3
    backoff_factor: float = 1
    status_forcelist: List[int] = [429, 502, 503, 504]
    method_whitelist: List[str] = ["HEAD", "GET", "POST", "OPTIONS"]
    class Config:
        env_prefix="ATM_CLIENT_"


class Client:
    __doc__ = """ATM V2 API Compliant Client
    
    Keyword Arguments:

        gateway_route_discovery_url (str): defaults to {default_gateway_route_discovery_url}

        gateway_route_generate_url (str): defaults to {default_gateway_route_generate_url}

        gateway_route_list_url (str): defaults to {default_gateway_route_list_url}

        timeout (int): defaults to {default_timeout}

        max_retry (int): The total number of retry attempts to make. 
            If the number of failed requests or redirects exceeds this number the client will throw the urllib3.exceptions.MaxRetryError exception. 
            I vary this parameter based on the API I'm working with, but I usually set it to lower than 10, usually 3 retries is enough.
            defaults to {default_max_retry}

        backoff_factor (float): It allows you to change how long the processes will sleep between failed requests. 
            The algorithm is as follows:
            >>> {{backoff factor}} * (2 ** ({{number of total retries}} - 1))
            For example, if the backoff factor is set to:

            1 second - the successive sleeps will be 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256.
            2 seconds - 1, 2, 4, 8, 16, 32, 64, 128, 256, 512
            10 seconds - 5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560
            defaults to {default_backoff_factor}

        status_forcelist (List[int]): The HTTP response codes to retry on. 
            You likely want to retry on the common server errors (502, 503, 504) because servers and reverse proxies don't always adhere to the HTTP spec. 
            Always retry on 429 rate limit exceeded because the urllib library should by default incrementally backoff on failed requests.
            defaults to {default_status_forcelist}

        method_whitelist (List[str]): The HTTP methods to retry on. 
            Modify this parameter to include HTTP method when have problem to perform the action again. 
            defaults to {default_method_whitelist}

    Note:
        The priorty of settings
            Highest <<< Overrided via Initialization fed with **kwargs <<< Overrided via Environment variables <<< Default values <<< Lowest


    References:

        see `https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/`

    """.format(**{f"default_{k}": v for k, v in dict(ClientArgs.construct()).items()})
    
    def __init__(self, **kwargs):
    
        self._args = ClientArgs(**kwargs)
        
        retry_strategy = Retry(
            total=self._args.max_retry,
            backoff_factor=self._args.backoff_factor,
            status_forcelist=self._args.status_forcelist,
            method_whitelist=self._args.method_whitelist,
        )
        
        adapter = TimeoutHTTPAdapter(max_retries=retry_strategy, 
                                     timeout=self._args.timeout)
        sess = requests.Session()
        sess.mount("https://", adapter)
        sess.mount("http://", adapter)
        
        self._sess = sess
        
        self._logs_on_success = defaultdict(list) # mode:endpoint_id -> [elapsed, ... ]
        self._logs_on_failure = defaultdict(list) # mode:endpoint_id -> [err, ...]
        
        self._funcs = {} # endpoint_id -> ATMFunction() mappings
        self._endpoints = {'endpoints': []}
        self._endpoints = self.proc_list()
        
    def __repr__(self) -> str:
        """Support visual repretation in the IDE
        
        Returns:
            str: <Client(...)>
        """
        repr_param = f"endpoints={len(self._endpoints['endpoints'])}"
        repr_clsname = type(self).__name__
        return f"<{repr_clsname}({repr_param})>"
        
    def __dir__(self) -> List[str]:
        """Discovered endpoints as well as the original possible attributes 
        are presented here.
        
        It is intended for supporting IPython, jupyter notebook tab completion
        """
        possible_attrs = [endpoint_id.replace("-", "_") 
                          for endpoint_id in self._endpoints['endpoints']] + \
                          object.__dir__(self)
        return possible_attrs
        
        
    def __getattr__(self, attr):
        """__getattr__ is called when the given attribute is not found in the object.
        
        This method allows us to access custom functions dynamically.
        When a user tries accessing attributes, for instance, 
        'client.engine_xxx_xxx', 
        this method is called with positional argument 'attr' as 'engine_xxx_xxx'. 
        """
        # This line ensures the attribute the user is looking for is converted to
        # dash-style conforming. e.g. 'engine_xxx' -> 'engine-xxx'
        endpoint_id = attr.replace("_", "-")
        
        
        func = self._funcs.get(endpoint_id, None)
        
        if func is None:
            # func is not found, we create new func and set.
            func = ATMFunction(endpoint_id, self)
            self._funcs[endpoint_id] = func
        
        return func
        
    def _request(self, mode, endpoint_id, payload=None):
        """All requests is made via this method. 
        
        Logs all the information here.
        
        Exception propagates to the caller.
        """
        try:
            started_at = time.time()
            if mode == "discovery":
                resp = self._sess.get(self._args.gateway_route_discovery_url.format(endpoint_id=endpoint_id))
            elif mode == 'generate':
                resp = self._sess.post(self._args.gateway_route_generate_url.format(endpoint_id=endpoint_id), json=payload)
            elif mode == 'list':
                resp = self._sess.get(self._args.gateway_route_list_url)
            resp.raise_for_status()
            data = resp.json()
            finished_at = time.time()
            elapsed = finished_at - started_at
            self._log_on_success(endpoint_id, mode, elapsed)
            # running this block means the endpoint is available
            self._add_endpoint_if_not_exist(endpoint_id)
            return data
        except (json.JSONDecodeError, requests.exceptions.HTTPError) as exc:
            msg = (f"[{resp.status_code}]: {endpoint_id} {mode} failed. \n"
                   f"({_get_exception(exc)})\n"
                   "response from server:\n"
                   f"{resp.content!r}")
            if resp.status_code >= 400 and resp.status_code < 500:
                err = ATMClientError(msg)
            elif resp.status_code >= 500:
                err = ATMServerError(msg)
            else:
                err = ATMClientError(msg)
        except requests.exceptions.ConnectionError as exc:
            msg = (f"[-] Unable to reach server for {endpoint_id}. ({_get_exception(exc)})")
            err = ATMServerError(msg)
        except requests.exceptions.Timeout as exc:
            msg = (f"[-] Unable to reach server for {endpoint_id}. ({_get_exception(exc)})")
            err = ATMServerError(msg)
        except requests.exceptions.RequestException as exc:
            msg = (f"[-] Unexpected request exception for {endpoint_id}. ({_get_exception(exc)})")
            err = ATMServerError(msg)
        self._log_on_failure(endpoint_id, mode, err)
        raise err
    
    def info(self, mode="generate", endpoint_id=None):
        """Show the information of requests sent by client
        
        Keyword Arguments:
            mode (str): filter with mode. if None is set, retrieve all modes. defaults to 'generate'
                {discovery, list, generate}
            endpoint_id (str): filter with endpoint_id, if None is set, retries all endpoints. defaults to None
        """
        
        # show logo
        print(__LOGO__)
        # nvidia-smi information (if applicable)
        print(_get_nvidia_smi())
        # number of endpoints
        print(f"Endpoints: {len(self._endpoints['endpoints'])} ")
        
        data = defaultdict(dict)
        for request_name, elapseds in self._logs_on_success.items():
            n_success = len(elapseds)
            if n_success:
                avg_time = round(1000 * sum(elapseds) / n_success, 1) # ms conversion
                min_time = round(1000 * min(elapseds), 1)
                max_time = round(1000 * max(elapseds), 1)
            else:
                avg_time, min_time, max_time = None, None, None
            
            data[request_name]["n_success"] = n_success
            data[request_name]["avg_time"] = avg_time
            data[request_name]["min_time"] = min_time
            data[request_name]["max_time"] = max_time
            
        for request_name, errs in self._logs_on_failure.items():
            n_failure = len(errs)
            data[request_name]["n_failure"] = n_failure
        
        for request_name, metrics in data.items():
            current_mode, current_endpoint_id = request_name.split(":")
            n_success = data[request_name].get("n_success", 0)
            n_failure = data[request_name].get("n_failure", 0)
            avg_time =  data[request_name].get("avg_time", 0) 
            min_time =  data[request_name].get("min_time", 0) 
            max_time =  data[request_name].get("max_time", 0) 
            n_total = n_success + n_failure
            
            if not current_endpoint_id.startswith("task") and \
               not current_endpoint_id.startswith("engine") and \
               not current_endpoint_id.startswith("proc"):
                continue
            
            if mode is not None and mode not in current_mode:
                continue
            
            if endpoint_id is not None and endpoint_id not in current_endpoint_id:
                continue
            
            print(f"[{current_mode:10}:{current_endpoint_id:40}] [S{n_success:>5}/F{n_failure:>5}] [{min_time:>7}~{avg_time:>7}~{max_time:>7}] ms")
        
    
    def _log_on_success(self, endpoint_id, mode, elapsed):
        request_name = mode + ":" + endpoint_id
        self._logs_on_success[request_name].append(elapsed)
    
    def _log_on_failure(self, endpoint_id, mode, err):
        request_name = mode + ":" + endpoint_id
        self._logs_on_failure[request_name].append(err)

    def _discovery_request(self, endpoint_id):
        """Discovery requests are made in here.
        
        Catches exceptions, and warns instead.
        
        Note:
            
            data : Response json from the engine/task/proc which implements 
                   the LXPER code-standard interface.
                  (Other keys are omitted for the brevity.) 

                            { 
                                ...
                            "request_json":{
                                            "title":"requestJSON",
                                            "type":"object",
                                            "properties":{
                                                "passage":{
                                                    "title":"Passage",
                                                    "type":"string"
                                                }
                                            },
                                            "required":[
                                                "passage"
                                            ]
                                            }
                            }

        Returns:
            params: List[Dict]

                [
                    {"name": "passage", "type": "string", "description": "", "required": True}
                ]
        """
        try:
            data = self._request("discovery", endpoint_id)
            params_properties = data['request_json']['properties']
            params_required = data['request_json'].get('required', [])
            params = []
            for param_name, param_info in params_properties.items():
                # In the example above, 'param_name' is 'passage' 
                # while 'param_info' is {'title': 'x', 'type': 'x'}
                param = {'name': param_name, 
                         'type': param_info.get("type", ""), 
                         'description': param_info.get("description", ""),
                         'required': param_name in params_required}
                params.append(param)
                
            return params
        except Exception as exc:
            warnings.warn(_get_exception(exc))
            return []
            

    def _generate_request(self, endpoint_id, payload):
        """Job requests are made in here.
        
        Exception propagates to the caller(ATMFunction)
        """
        data = self._request("generate", endpoint_id, payload=payload)
        return data
    
    def proc_list(self):
        """List requests are made in here.
        
        Catches exceptions, and warns instead.
        
        
        Note:
        
            data is as follows:
            [
                {
                    "predicate":"Paths: [/engine-blank-finder/**], match trailing slash: true",
                    "metadata":{
                        "type":"atm-library",
                        "kubectl.kubernetes.io/last-applied-configuration":"{"apiVersi...,
                        "port.web":"8000"
                    },
                    "route_id":"ReactiveCompositeDiscoveryClient_atm-engine-blank-finder",
                    "filters":[
                        "[[RewritePath /proc(?<segment>[^/]*)(/)?(?<remaining>.*)? = '/proc${segment}/${remaining}'], order = 1]",
                        "[[RewritePath /task(?<segment>[^/]*)(/)?(?<remaining>.*)? = '/${remaining}'], order = 2]",
                        "[[RewritePath /engine(?<segment>[^/]*)(/)?(?<remaining>.*)? = '/${remaining}'], order = 3]"
                    ],
                    "uri":"http://atm-engine-blank-finder:8000",
                    "order":0
                }, ...
            ]

        """
        try:
            endpoint_id = "proc-list"
            data = self._request("list", endpoint_id)

            endpoint_ids = []
            for route in data:
                predicate = route['predicate']
                start_position = predicate.find("/") + 1
                end_position = predicate.find("/**")
                endpoint_id = predicate[start_position:end_position]

                if '-' not in endpoint_id:
                    continue
                endpoint_ids.append(endpoint_id)

            endpoints = {'endpoints': endpoint_ids}
        except Exception as exc:
            warnings.warn(_get_exception(exc))
            endpoints = {'endpoints': []}
        finally:
            return endpoints

    def _add_endpoint_if_not_exist(self, endpoint_id):
        if endpoint_id not in self._endpoints['endpoints']:
            self._endpoints['endpoints'].append(endpoint_id)
        
        

class ATMFunction:
    """Callable which executes the request to the API
    
    This class also performs parameter discovery when __doc__ is called.
    """
    def __init__(self,
                 endpoint_id: str,
                 client: Client):
        
        
        self._endpoint_id = endpoint_id
        self._client = client
        
        # Initially, _discovered_params is None 
        # When the property 'self.params' is called,
        # and 'self._discovered_params' found to be None,
        # the _discovery_request is fired to set 'self._discovered_params'
        self._discovered_params = None

    def _discovery_request(self):
        return self._client._discovery_request(self._endpoint_id)
    
    def _generate_request(self, payload):
        return self._client._generate_request(self._endpoint_id, payload)
        
    @property
    def params(self) -> List[Dict]:
        """list parameters that API accepts.
        
        If the self._discovered_params is not set, _discovery_request is called
        to get the parameter information from the API

        This property will raise the error when the API side does not respond.
        """
        if self._discovered_params is None:
            params = self._discovery_request()
            
            if len(params) == 0:
                warnings.warn(f"{self._endpoint_id} may have trouble.")
            
            self._discovered_params = params
        return self._discovered_params

    def __repr__(self) -> str:
        """Support visual repretation in the IDE
        
        Returns:
            str: <ATMFunction(parameter_name: parameter_type, ...)>
        """
        repr_param = ", ".join(f"{param['name']}: {param['type']}" 
                               for param in self.params)
        repr_clsname = type(self).__name__
        return f"<{repr_clsname}({repr_param})>"

    @property
    def __doc__(self) -> str:
        # to check this function is in work 
        self._test()
        
        # TODO: Support for `Returns:` section
        docstring_args = "Args:"
        docstring_kwargs = "Keyword Arguments:"
        docstring_param_tpl = "{name}({type}): {description}"
        
        params_args, params_kwargs = [], []

        for param in self.params:
            if param['required']:
                params_args.append(param)
            else:
                params_kwargs.append(param)
        
        docstring = f"Calls API for {self._endpoint_id}"
        docstring += "\n"
        docstring += "\n"
        
        if params_args:
            docstring += docstring_args + "\n"

            for param in params_args:
                docstring_param = \
                docstring_param_tpl.format(name=param['name'], 
                                           type=param['type'], 
                                           description=param["description"])
                docstring += "\t" + docstring_param + "\n"

        if params_kwargs:
            docstring += docstring_kwargs + "\n"

            for param in params_kwargs:
                docstring_param = \
                docstring_param_tpl.format(name=param['name'], 
                                           type=param['type'], 
                                           description=param["description"])
                docstring += "\t" + docstring_param + "\n"

        return docstring
       
    def __call__(self, *args, **kwargs):
        # This builds the payload from the given args and kwargs, 
        # and the params that ATM API supports
        payload = {}

        # When kwargs is set twice, we will raise error.
        param_name_set = set()

        # In PEP8, 'if args' is completely acceptable and the recommended way, 
        # because the empty sequence is evaluated as False.
        # However, explicitly stating the comparison with zero
        # makes the another technical writers infer the data type easily.
        if len(args) > 0:
            # user gave args. this means we need to fill the parameters in order.
            for param, value in zip(self.params, args):
                param_name = param['name']
                payload[param_name] = value
                # occupied parameters are inserted into the set 'param_name_set'
                param_name_set.add(param_name)
            
        if len(kwargs) > 0:
            for param_name, value in kwargs.items():
                if param_name in param_name_set:
                    # This line is executed when the keyword argument is
                    # provided for the same position argument which is
                    # already occupied. 
                    raise TypeError("got multiple valus for argument"
                                    f"'{param_name}'")
                payload[param_name] = value
                param_name_set.add(param_name)

        data = self._generate_request(payload)
        
        # we can support dot notation for easier access for data
        try:
            data = ATMResult(data)
            return data
        except:
            # if the data isn't dictionary type, it may raise exception.
            return data
    
    

################################################################################
# Section C. Initialize Client Class
################################################################################

client = Client()