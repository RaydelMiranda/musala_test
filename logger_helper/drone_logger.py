import logging
import sys

handler = logging.StreamHandler(sys.stdout)
musala_logger = logging.getLogger("Musala Drones")
musala_logger.addHandler(handler)

