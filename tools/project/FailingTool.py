import arcpy

import utils.arcpy_tools as archelp
from utils.tool import Tool

class FailingTool(Tool):
    """An Example of a failing modularized tool"""
    
    def __init__(self) -> None:
        """
        Example Failing Tool Description

        @self.project: arcpy project object
        @self.project_location: path to the project
        @self.project_name: name of the project
        @self.default_gdb: path to the default gdb
        @self.params: tool parameters (set with archelp.get_parameters())
        """
        # Initialize the parent class
        super().__init__()
                
        # Overrides
        self.category = "Example Category"
        self.description = "Example tool description"
        self.label = "Example Tool"
        
        # Parameters
        self.params = {}
        self.my_number = 3.14159
        
        syntax error here
        
        return
    
    def getParameterInfo(self) -> list[arcpy.Parameter]:
        """Define parameter definitions"""
        
        # Define parameters here
        
        number = arcpy.Parameter(
            displayName="Number",
            name="number",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        number.value = 42
        
        params = [number]
        # Write params to self.params for use in execute()
        self.params = archelp.get_params(params)
        return params
    
    def execute(self, parameters:list[arcpy.Parameter], messages:list) -> None:
        """The source code of the tool."""
        
        self.params = archelp.get_params(parameters)
        
        archelp.msg(f"{self.default_gdb}")
        archelp.msg(f"{self.project_name}")
        archelp.msg(f"self.my_num: {self.my_number}")
        archelp.msg(f"self.params['number']: {self.params['number'].value}")
        return