# -*- coding: utf-8 -*-
import unittest
import logging

from gstomd.corpus import Corpus
from gstomd.my_settings import SetupLogging

SetupLogging()
logger = logging.getLogger(__name__)


class CorpusTest(unittest.TestCase):
    """Tests operations of corpus class.
    """
    # ga = GoogleAuth('settings/test1.yaml')
    # ga.LocalWebserverAuth()
    # drive = GoogleDrive(ga)

    def test_01(self):
        logger.debug("Begin")

        corpus = Corpus('settings/test1.yaml')
        logger.debug("Corpus Created")

        corpus.fetch()
        logger.debug("Corpus Fetched")

        for col in corpus.collections:

            logger.info(col.root_folder)

        corpus.to_disk()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
