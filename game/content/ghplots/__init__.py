import inspect

from . import actionscenes
from . import dd_combatmission
from . import dd_customobjectives
from . import dd_distanttown
from . import dd_homebase
from . import dd_intro
from . import dd_lancedev
from . import dd_main
from . import dd_misc
from . import dd_roadedge
from . import dd_roadedge_etc
from . import dd_roadedge_propp
from . import dd_roadstops
from . import dungeons
from . import encounters
from . import lancemates
from . import missionbuilder
from . import mission_conversations
from . import mission_stubs
from . import mission_teamups
from . import mocha
from . import recovery
from . import setpiece
from . import tarot_cards
from . import tarot_reveal
from . import tarot_sockets
from . import thingplacers
from . import treasures
from . import utility
from game.content import mechtarot, PLOT_LIST, UNSORTED_PLOT_LIST, CARDS_BY_NAME
from pbge.plots import Plot


def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , Plot ) and o is not Plot and o is not mechtarot.TarotCard:
            PLOT_LIST[ o.LABEL ].append( o )
            UNSORTED_PLOT_LIST.append( o )
            # print o.__name__
            if issubclass(o,mechtarot.TarotCard):
                CARDS_BY_NAME[o.__name__] = o


harvest(actionscenes)
harvest(dd_combatmission)
harvest(dd_customobjectives)
harvest(dd_distanttown)
harvest(dd_homebase)
harvest(dd_intro)
harvest(dd_lancedev)
harvest(dd_main)
harvest(dd_misc)
harvest(dd_roadedge)
harvest(dd_roadedge_etc)
harvest(dd_roadedge_propp)
harvest(dd_roadstops)
harvest(dungeons)
harvest(encounters)
harvest(lancemates)
harvest(missionbuilder)
harvest(mission_conversations)
harvest(mission_stubs)
harvest(mission_teamups)
harvest(mocha)
harvest(recovery)
harvest(setpiece)
harvest(tarot_cards)
harvest(tarot_reveal)
harvest(tarot_sockets)
harvest(thingplacers)
harvest(treasures)
harvest(utility)
