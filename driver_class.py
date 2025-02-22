class Driver:
    def __init__( self, path, name ):
        self.name = name
        self.path = path[ :1 ] if path[ len( path ) - 1: ] == "\\" else path
        
        file = open( "{}\\{}".format( path, name ), "r", encoding="ANSI" )
        self.content = file.read( )
        file.close( )

        self.severity = 0
        self.have_device = "IoCreateDevice" in self.content
    
    def increase_severity( self, i ):
        self.severity += i
