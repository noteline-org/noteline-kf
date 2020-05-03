import unittest
import shutil
import os

from noteline.kf import noteline_nb_op
from noteline.core import noteline_notebook, envs

ORIGINAL_NOTEBOOK_FILE_NAME="test/noteline/kf/test.ipynb"
TEST_NOTEBOOK_FOLDER="/tmp"
TEST_NOTEBOOK_FILE_NAME="{}/test.ipynb".format(TEST_NOTEBOOK_FOLDER)


class TestNotelineNotebook(unittest.TestCase):

    def setUp(self):
        shutil.copy(ORIGINAL_NOTEBOOK_FILE_NAME, TEST_NOTEBOOK_FOLDER)

    def tearDown(self):
        os.remove(TEST_NOTEBOOK_FILE_NAME)

    def test_metadata_set_get(self):
        docker_uri = "uri123"

        env_name = "name1"
        env_type = envs.DOCKER_ENV_TYPE
        env_uri = docker_uri

        nb = noteline_notebook.get_noteline_notebook(TEST_NOTEBOOK_FILE_NAME)

        nb.set_env(name=env_name, type=env_type, uri=env_uri)
        nb.save_notebook(TEST_NOTEBOOK_FILE_NAME)

        test_op = noteline_nb_op.NotelineNbOp(notebook_in=TEST_NOTEBOOK_FILE_NAME)

        self.assertEqual(test_op.image, docker_uri)
