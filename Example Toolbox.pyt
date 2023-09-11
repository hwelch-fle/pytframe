from importlib import reload
import traceback

import utils.dev
reload(utils.dev)
from utils.dev import build_dev_error

import utils.arcpy_tools
reload(utils.arcpy_tools)

# TODO make this process a function
try:
    import tools.project.ExampleTool
    reload(tools.project.ExampleTool)
    from tools.project.ExampleTool import ExampleTool
except Exception as e:
    ExampleTool = build_dev_error("Example Tool", traceback.format_exc())
    
try:
    import tools.project.FailingTool
    reload(tools.project.FailingTool)
    from tools.project.FailingTool import FailingTool
except Exception as e:
    FailingTool = build_dev_error("Failing Tool (check my description)", traceback.format_exc())

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        
        self.label = "Example Toolbox"
        self.alias = "ExampleToolbox"
        
        # List of tool classes associated with this toolbox
        self.tools = [ExampleTool, FailingTool]