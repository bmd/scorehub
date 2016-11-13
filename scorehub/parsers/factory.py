from parsers import NcaafParser
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ParserFactory(object):
    @staticmethod
    def make_parser(name):
        if name == 'ncaaf':
            logger.debug("Making ncaaf parser")
            return NcaafParser()

        raise NotImplementedError("No parser for type {name}".format(name=name))
