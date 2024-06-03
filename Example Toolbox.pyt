from importlib import reload, invalidate_caches
invalidate_caches()

import utils.dev
reload(utils.dev)
from utils.dev import import_tools

import utils.arcpy_tools
reload(utils.arcpy_tools)

import utils.constants
reload(utils.constants)

import utils.excel_tools
reload(utils.excel_tools)

import utils.tool
reload(utils.tool)

TOOLS = \
{
    "tools.project":
        [
            "ExampleTool",
            "FailingTool",
        ],
}

IMPORTS = import_tools(TOOLS)
globals().update({tool.__name__: tool for tool in IMPORTS})

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        
        self.label = "Example Toolbox"
        self.alias = "ExampleToolbox"
        
        # List of tool classes associated with this toolbox
        self.tools = [ExampleTool, FailingTool]
