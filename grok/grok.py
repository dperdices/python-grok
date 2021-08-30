""" 
Python package to handle Grok expressions

Author: Daniel Perdices <daniel.perdices@uam.es>
"""
import regex as re
import os
from typing import Dict

class GrokPattern(object):
    """
    A grok pattern class that supports re syntax

    Examples:
    ```
    r = GrokPattern("%{NUMBER:mynumber}")
    r.match("1.2").groupdict()
    ```
    """
    patterns : Dict[str, re.Pattern] = {}
    _var_counter : int = 0
    _ADD_VAR_NAME : bool = False

    def __init__(self, pattern : str):
        self.pattern = pattern
        self.regex = re.compile(GrokPattern._grok2regex(pattern))


    def __getattr__(self, attr):
        if attr in dir(self.regex):
            return self.regex.__getattribute__(attr)

    @classmethod
    def _grok2regex(self, expr : str) -> str:
        """
        Computes the regex expression from a grok pattern
        """
        res = expr
        while True:
            matches = re.findall(r"%{(\w+)(:(\w+)(:(\w+))?)?}", res)
            if len(matches) == 0:
                return res
            for match in matches:
                name, var_name, typing = match[0], match[2], match[4]
                if not (name in self.patterns):
                    raise ValueError (f"Pattern not found in templates: {name}.")
                subs = f"(?P<{var_name}>{self.patterns[name]})"
                if len(var_name) == 0:
                    if self._ADD_VAR_NAME:
                        var_name = f"var_{self._var_counter}"
                        self._var_counter += 1
                        subs = f"(?P<{var_name}>{self.patterns[name]})"
                    else:
                        subs = f"({self.patterns[name]})"

                res = re.sub(r"%{[^}]+}", subs, res)


    @classmethod
    def load_patterns_from_dir(self, dir : str) -> None:
        """
        Load all Grok patterns in the directory
        """
        for filename in os.listdir(dir):
            self.load_patterns_from_file(dir + "/" + filename)

    @classmethod
    def load_patterns_from_file(self, filename : str) -> None:
        """
        Load all Grok patterns in the file
        """
        with open(filename, "r") as f:
            for line in f:
                line = re.sub(r"#.*", "", line)
                line = line.strip()
                if len(line) == 0:
                    continue

                key = line[:line.find(" ")]
                value = line[line.find(" ")+1:]

                self.patterns[key] = value

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

with pkg_resources.path("grok", "patterns") as patterns_path:
    GrokPattern.load_patterns_from_dir(patterns_path)
