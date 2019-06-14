from hamming import *
import random
import logging
import daiquiri 
import daiquiri.formatter
import logger_format
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logger_format.RainbowLoggingHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

#    def test_func():
#        logger.debug("debug msg")
#        logger.info("info msg")
#        logger.warn("warn msg")
#
#    def test_func_2():
#        logger.error("error msg")
#        logger.critical("critical msg")
#
#        try:
#            raise RuntimeError("Opa!")
#        except Exception as e:
#            logger.exception(e)
#
#    test_func()
#    test_func_2()
#daiquiri.setup(level=logging.DEBUG, outputs=(
#                                   daiquiri.output.Stream(formatter=daiquiri.formatter.ColorFormatter(
#                                       fmt="[%(levelname)s: "
#                                    "%(name)s] %(message)s")),
#            ))
#
#logger = daiquiri.getLogger(__name__)

data_width = 4
data = 4
encode = hamming_encode_nbit(data, data_width)
logger.info('Data={0}     Hamming encode={1}'.format(data,encode))
logger.info(' Hamming encode={}'.format(encode))
encode = int(encode,2)
logger.info(' Hamming encode={}'.format(encode))
encode = hamming_encode_nbit(encode, (data_width+3))
logger.info(' Hamming encode={}'.format(encode))
