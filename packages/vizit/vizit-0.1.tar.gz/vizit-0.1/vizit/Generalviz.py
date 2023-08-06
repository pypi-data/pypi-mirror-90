class Visualization():
    
    """ Generic class for creating a visualization.
        
    Attributes:
        title (string): title of the visualization
        data (DataFrame): dataset containing the variable(s) to visualize
    """
    
    def __init__(self, title, data):
        
        self.title = title
        self.data = data