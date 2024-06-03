Use the following code as a template when creating new tools

```python
import arcpy

import utils.arcpy_tools as archelp
from utils.tool import Tool

class MyTool(Tool):
    """Tool Definition"""
    
    def __init__(self) -> None:
        """
        Tool Description
        """
        # Initialize the parent class
        super().__init__()
                
        # Overrides
        self.category = "Default"
        self.description = "Default tool description"
        self.label = "Default Tool"
        
        # Parameters
        self.params = {}
        self.my_number = 3
        
        return
    
    def execute(self, parameters:list[arcpy.Parameter], messages:list) -> None:
        """The source code of the tool."""

        # Allows reference to parameters by name instead of index
        self.params = archelp.get_params(parameters)

        return
```
