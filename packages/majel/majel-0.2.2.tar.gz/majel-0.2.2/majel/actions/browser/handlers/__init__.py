# We have to import these here so they're loaded at start time and recognised
# as subclasses of Handler.  They shouldn't be imported from here.

from .amazon import AmazonHandler
from .basic import BasicHandler
from .netflix import NetflixHandler
from .selector import SelectionHandler
from .youtube import YoutubeHandler
