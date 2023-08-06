"""
A set of simple tools to build a configuration system with

The first set are 'sources':
  - OSEnvConfigSource: which parses config values from os.environ into hierarchical dictionaries
  - YamlConfigFile: which parses a yaml file into hierarchical dictionaires
The second tool is:
  - MergedConfiguration: which merges multiple configuration sources into a coherent whole

Yes, much more could be done:
    - required keys
    - value validation
    - default parsers
    - default default values (that .get() without a default would default to)
    - more file types (json, ini, env, ... xml?)


Much inspration - and the .get() signature - is taken from everett, but the implementation is all mine.
"""

import os
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, List, Union, Optional

import yaml

logger = logging.getLogger(__name__)


class ConfigSource(ABC):

    @abstractmethod
    def as_dict(self) -> Dict[str, str]:
        '''
        return a dict containing configuration information from this source.

        NOTE: Errors _MUST_ _NOT_ be raised; in case of error, return as much configuration information as possible.
        An empty dict is acceptable (and expected, in cases where, for instance, the supplied configuration file
        doesn't exist)
        '''
        raise NotImplementedError


class DictSource(ConfigSource):
    '''
    Uses the supplied dict as a config source.  Useful for defaults.
    '''
    def __init__(self, cfg_dict: Dict):
        self.cfg = cfg_dict

    def as_dict(self) -> Dict[str, str]:
        return self.cfg


class OSEnvironSource(ConfigSource):
    '''
    Uses os.environ as a config source, by parsing PREFIXd keys into hierarchical dictionaries, splitting on _
    '''
    def __init__(self, prefix: str):
        self.prefix = prefix.strip('_').upper() + '_'

    def as_dict(self) -> Dict[str, str]:
        result = dict()
        for env_key in os.environ:
            if not env_key.startswith(self.prefix):
                continue
            key_path = env_key.split('_')[1:]
            if not key_path:
                continue
            *ns_list, key = key_path
            namespace = result
            for subns in ns_list:
                namespace = namespace.setdefault(subns, dict())
            namespace[key] = os.environ[env_key]
        return result


class YamlFileSource(ConfigSource):
    '''
    A YAML file source of configuration information
    '''
    def __init__(self, filename: Union[Path, str]):
        self.path = Path(filename)

    def as_dict(self) -> Dict[str, str]:
        if not self.path.exists():
            return dict()
        if not self.path.is_file():
            return dict()
        with self.path.open() as f:
            return yaml.safe_load(f)


def _recursive_dict_update(main: Dict, update: Dict):
    '''
    like dict.update(), modifies the 'main' by applying 'update'
    UNLIKE dict.update(), normalizes all keys to lowercase
    '''
    for k, v in update.items():
        lk = k.lower()
        if isinstance(v, dict) and isinstance(main.get(lk), dict):
            _recursive_dict_update(main[lk], v)
        else:
            main[lk] = v

class MergedConfiguration:
    '''
    Merges configuration sources, with later overriding earlier
    '''
    def __init__(self, sources: Optional[List[ConfigSource]] = None):
        self.sources: List[ConfigSource] = [] if sources is None else sources
        self._loaded: Optional[Dict] = None

    def add_source(self, source: ConfigSource):
        self.sources.append(source)

    def load(self):
        '''
        cause the config to be loaded; note that this need not be called directly, as it is lazily loaded.
        Subsequent calls _will_ re-load from the config sources.
        '''
        loaded = dict()
        for source in self.sources:
            updates = source.as_dict()
            _recursive_dict_update(loaded, updates)
        self._loaded = loaded


    def as_dict(self) -> Dict[str, str]:
        if self._loaded is None:
            self.load()
        return self._loaded

    def get(self, key: str, namespace: Optional[List[str]]=None, default=None, parser=str, raise_error=True, doc=None):
        '''
        get a single config key
        a namespace is the 'path' in the config to the namespace to look the key up in
        default is the value to use if the key is not found
        parser is how to cast the result
        raise_error is whether to raise an error if the key is not found (note: supplying a default negates
            raise_error, as a (presumably) valid value is always available)
        doc is extra information to supply with the error message
        '''
        k = key.lower()
        ns = namespace or []
        in_ns = self.as_dict()
        for subns in ns:
            in_ns = in_ns[subns]
        if raise_error and default is None and k not in in_ns:
            msg = f"Missing config key {'.'.join(ns + [k])}"
            if doc:
                msg += f": {doc}"
            raise KeyError(msg)
        return parser(in_ns.get(k, default))

    def as_ns(self, namespace: List[str]) -> SimpleNamespace:
        '''
        return the config, or a namespace within it, as a SimpleNamespace
        '''
        in_ns = self.as_dict()
        for subns in namespace:
            in_ns = in_ns[subns]
        if not isinstance(in_ns, dict):
            raise ValueError("Need a sub-namespace (dict) to make a namespace")
        return SimpleNamespace(**in_ns)

