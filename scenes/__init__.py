""" Barebones scene handling for an isometric RPG. For game-specific data,
    either subclass the Scene or just declare whatever extra bits are needed.
"""

    # I feel like this unit isn't very Pythonic, since it's full of setters
    # and getters and various other walls to keep the user away from the
    # data.


import engine
import pathfinding
import pfov
import terrain
import viewer

class Tile( object ):
    def __init__(self, floor=None, wall=None, decor=None, visible=True):
        self.floor = floor
        self.wall = wall
        self.decor = decor
        self.visible = visible

    def get_floor( self, terrainlist ):
        try:
            return terrainlist[self.floor]
        except TypeError:
            return None
    def get_wall( self, terrainlist ):
        try:
            return terrainlist[self.wall]
        except TypeError:
            return None
    def get_decor( self, terrainlist ):
        try:
            return terrainlist[self.decor]
        except TypeError:
            return None

    def blocks_vision( self, terrainlist ):
        floor,wall,decor = self.get_floor(terrainlist),self.get_wall(terrainlist),self.get_decor(terrainlist)
        return ( floor and floor.block_vision ) or (wall and wall.block_vision ) or ( decor and decor.block_vision )

    def blocks_walking( self, terrainlist ):
        floor,wall,decor = self.get_floor(terrainlist),self.get_wall(terrainlist),self.get_decor(terrainlist)
        return (floor and floor.block_walk) or (self.wall is True) or (wall and wall.block_walk) or (decor and decor.block_walk)


class Scene( object ):
    DELTA8 = ( (-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1) )
    ANGDIR = ( (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0) )
    def __init__(self,width=128,height=128,terrainlist=[],name=""):
        self.name = name
        self.width = width
        self.height = height
        self.terrainlist = terrainlist
        self.scripts = engine.container.ContainerList()
        self.in_sight = set()

        self.last_updated = 0

        # Fill the map with empty tiles
        self._contents = engine.container.ContainerList(owner=self)
        self._map = [[ Tile()
            for y in xrange(height) ]
                for x in xrange(width) ]

    def on_the_map( self , x , y ):
        # Returns true if on the map, false otherwise
        return ( ( x >= 0 ) and ( x < self.width ) and ( y >= 0 ) and ( y < self.height ) )


    def get_floor( self, x, y ):
        """Safely return floor of tile x,y, or None if off map."""
        if self.on_the_map(x,y):
            return self._map[x][y].get_floor(self.terrainlist)
        else:
            return None

    def get_wall( self, x, y ):
        """Safely return wall of tile x,y, or None if off map."""
        if self.on_the_map(x,y):
            return self._map[x][y].get_wall(self.terrainlist)
        else:
            return None

    def get_decor( self, x, y ):
        """Safely return decor of tile x,y, or None if off map."""
        if self.on_the_map(x,y):
            return self._map[x][y].get_decor(self.terrainlist)
        else:
            return None

    def get_visible( self, x, y ):
        """Safely return visibility status of tile x,y, or None if off map."""
        if self.on_the_map(x,y):
            return self._map[x][y].visible
        else:
            return False

    def tile_blocks_vision( self, x, y ):
        if self.on_the_map(x,y):
            return self._map[x][y].blocks_vision(self.terrainlist)
        else:
            return True

    def tile_blocks_walking( self, x, y ):
        if self.on_the_map(x,y):
            return self._map[x][y].blocks_walking(self.terrainlist)
        else:
            return True

    def distance( self, pos1, pos2 ):
        return round( math.sqrt( ( pos1[0]-pos2[0] )**2 + ( pos1[1]-pos2[1] )**2 ) )

    def __str__( self ):
        if self.name:
            return self.name
        else:
            return repr( self )

    def wall_wont_block( self, x, y ):
        """Return True if a wall placed here won't block movement."""
        if self.tile_blocks_walking(x,y):
            # This is a wall now. Changing it from a wall to a wall really won't
            # change anything, as should be self-evident.
            return True
        else:
            # Adding a wall will block a passage if there are two or more spaces
		    # in the eight surrounding tiles which are separated by walls.
            was_a_space = not self.tile_blocks_walking(x-1,y)
            n = 0
            for a in self.ANGDIR:
                is_a_space = not self.tile_blocks_walking(x+a[0],y+a[1])
                if is_a_space != was_a_space:
                    # We've gone from wall to space or vice versa.
                    was_a_space = is_a_space
                    n += 1
            return n <= 2

    def check_terrain( self, terraintype ):
        """ If terraintype in the terrain list, return its index. If it is
            not yet in the list, and is valid, add it and return its index.
            Otherwise return terraintype unchanged and trust the caller."""
        # This is probably a YAGNI method, but screw it. It's done.
        if terraintype in self.terrainlist:
            return self.terrainlist.index( floor )
        elif isinstance( terraintype, terrain.Terrain ):
            self.terrainlist.append( terraintype )
            return len( self.terrainlist ) - 1
        else:
            return terraintype

    def fill( self, dest, floor=-1, wall=-1, decor=-1 ):
        # Fill the provided area with the provided terrain.
        # If we are being provided a raw tile type, 
        floor = self.check_terrain(floor)
        wall = self.check_terrain(wall)
        decor = self.check_terrain(decor)
        for x in range( dest.x, dest.x + dest.width ):
            for y in range( dest.y, dest.y + dest.height ):
                if self.on_the_map(x,y):
                    if floor != -1:
                        self._map[x][y].floor = floor
                    if wall != -1:
                        self._map[x][y].wall = wall
                    if decor != -1:
                        self._map[x][y].decor = decor


