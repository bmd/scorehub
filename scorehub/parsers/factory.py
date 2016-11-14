from parsers import NcaafParser, NcaabParser
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ParserFactory(object):
    @staticmethod
    def make_parser(name):
        if name == 'ncaaf':
            logger.debug("Making ncaaf parser")
            return NcaafParser()
        elif name == 'ncaab':
            logger.debug("Making ncaab parser")
            return NcaabParser()

        raise NotImplementedError("No parser for type {name}".format(name=name))
