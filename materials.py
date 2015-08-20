class Material( object ):
    def __init__( self , name , mass_scale , damage_scale , cost_scale ):
        self.name = name
        self.mass_scale = mass_scale
        self.damage_scale = damage_scale
        self.cost_scale = cost_scale

    def __reduce__( self ):
        # When pickling, we want to save the reference to the global constant
        # rather than having the pickler create new instances all the time.
        return self.name.upper()


METAL   = Material( "Metal" , 10 , 5 , 10 )
ADVANCED = Material( "Advanced" , 8 , 5 , 50 )
MEAT    = Material( "Meat" , 16 , 4 ,  7 )
BIOTECH = Material( "Biotech" , 9 , 6 , 120 )

