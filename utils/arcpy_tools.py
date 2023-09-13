import arcpy
import os

"""
Use this module for any helper functions that you want to use between tools
If you find yourself re-impelementing the same function in multiple tools,
consider moving it here
"""

def row_to_dict(cursor:arcpy.da.SearchCursor) -> dict[object]:
    """Converts a arcpy.da Cursor row to a dictionary
    @cursor: The cursor to convert
    >>> cursor = arcpy.da.SearchCursor(<features>, <headers>, <sql_clause>)
    >>> for row in row_to_dict(cursor):
    >>>     print(row['fieldName'])
    >>> del cursor
    """
    for row in cursor:
        yield dict(zip(cursor.fields, row))

def get_databases(location:str, database_name:str="None") -> list:
    """Gets all the databases in the location
    @location: The location to search for databases
    @database_name: The name of the database to search for (default is None)
    @return: A list of databases
    """
    
    databases = []
    for root, dirs, files in os.walk(location):
        for dir in dirs:
            if dir.endswith(".gdb"):
                databases.append(os.path.join(root, dir))
    if database_name != "None":
        databases = [x for x in databases if x.lower().endswith(database_name)]
    return databases

def walk_database(database:str, datatype:str=None, 
                  dataset:str=None) -> dict[str]:
    """Walks the database and returns a list of all the feature classes
    @database: The database to walk (path to the database)
    @datatype: The datatype to search for (all, table, featureclass)
    @dataset: The dataset to search for
    @return: A dictionary of feature classes (in the format {<feature class name>:<feature class path>})
    """
    feature_classes = []
    arcpy.env.workspace = database
    feature_classes = [os.path.join(database, dataset, fc) 
                       for fc in arcpy.ListFeatureClasses(feature_dataset=dataset, 
                                                          feature_type=datatype)
                       ]
    return {os.path.basename(path):path for path in feature_classes}

def get_tables(database: str) -> dict[str]:
    """Gets all the tables in the database
    @database: The database to search
    @return: A dictionary of tables (in the format {<table name>:<table path>})
    """
    tables = []
    arcpy.env.workspace = database
    tables = [os.path.join(database, table) for table in arcpy.ListTables()]
    return {os.path.basename(path):path for path in tables}

def get_project(project_location:str) -> str:
    """Gets the project from the project path
    @project: The project path
    @raises Exception: If the project is not an ArcGIS Pro project file
    @return: The project
    """
    if not project_location.endswith(".aprx"):
        raise Exception("Project must be an ArcGIS Pro project")
    return arcpy.mp.ArcGISProject(project_location)
    
def msg(message:str="", level:str="message") -> None:
    """
    Prints a message to the console and adds a message to ArcGIS Pro
    @message: The message to print
    @level: The level of the message (message, warning, error)
    """
    
    message = str(message)
    level = str(level).lower()
    level = ("message" if level not in ["message", "warning", "error"] else level)
    # Message
    if level == "message":
        print(message)
        arcpy.AddMessage(message)
    # Warning
    elif level == "warning":
        print(f"WARNING: {message}")
        arcpy.AddWarning(message)
    # Error
    elif level == "error":
        print(f"ERROR: {message}")
        arcpy.AddError(message)
    return

    
def get_params(parameters:list) -> dict:
    """
    Converts the parameters to a dictionary
    @parameters: The parameters to convert
    @return: The parameters as a dictionary
    """
    return {p.name:p for p in parameters}

def get_rows(features:str, fields:list[str], query:str=None)-> dict:
    """
    Gets the rows from the feature class
    @features: The feature class to get the rows from
    @fields: The fields to get from the feature class
    @query: The query to filter the rows by (optional)
    @yield: A Search cursor and a dictionary of rows (in the format {<field>:<value>})
    
    Usage:
    >>> for cursor, row in get_rows(<features>, <fields>, <query>):
    >>>     print(row['fieldName'])
    """
    
    with arcpy.da.SearchCursor(features, fields, query) as cursor:
        for row in row_to_dict(cursor):
            yield cursor, row
                
def update_rows(features:str, fields:list[str], query:str=None) -> dict:
    """
    Updates the rows in the feature class
    @features: The feature class to update the rows in
    @fields: The fields to update
    @query: The query to filter the rows by (optional)
    @yield: An update cursor and a dictionary of rows (in the format {<field>:<value>})
    
    Usage:
    >>> for cursor, row in update_rows(<features>, <fields>, <query>):
    >>>     row['fieldName'] = <value>
    >>>     cursor.updateRow(list(row.values()))
    """
    with arcpy.da.UpdateCursor(features, fields, query) as cursor:
        for row in row_to_dict(cursor):
            yield cursor, row
            
def insert_row(features:str, fields:list[str], query:str, row:list[list]) -> int:
    """
    Inserts the rows into the feature class
    @features: The feature class to insert the rows into
    @fields: The fields to insert
    @query: The query to filter the rows by (optional)
    @row: The row to insert
    @return: count of rows inserted
    
    Usage:
    >>> rows = [[<value>, <value>], [<value>, <value>]]
    >>> insert_rows(<features>, <fields>, <query>, rows)
    """
    with arcpy.da.InsertCursor(features, fields, query) as cursor:
        cursor.insertRow(row)
    return

def print_layout(layout=None, quality:str="BEST", resolution:int=300, is_mapseries=False, page_name:str="LAYOUT"):
    """
    Prints the layout to a PDF
    @layout: The layout to print
    @quality: The quality of the PDF (BEST, NORMAL, FASTEST)
    @resolution: The resolution of the PDF (DPI)
    @is_mapseries: Is the layout part of a map series (default is False)
    @return: The PDF document
    """
    temp = tempfile.mkdtemp()
    if is_mapseries:
        mapseries = layout
        pdf = os.path.join(temp, f"{page_name}.pdf")
        return mapseries.exportToPDF(pdf, resolution=resolution, image_quality=quality, page_range_type="CURRENT")
    else:
        pdf = os.path.join(temp, f"{layout.name}.pdf")
        return layout.exportToPDF(pdf, resolution=resolution, image_quality=quality)
        
def print_mapseries(mapseries=None, quality:str="BEST", resolution:int=300):
    """
    Iterates over a map series and prints to a list of PDFs
    @mapseries: The map series to print
    @quality: The quality of the PDF (BEST, NORMAL, FASTEST)
    @resolution: The resolution of the PDF (DPI)
    @return: A list of PDF documents
    """
    for page_num in range(1, mapseries.pageCount+1):
        mapseries.currentPageNumber = page_num
        yield print_layout(mapseries, quality, resolution, is_mapseries=True)
