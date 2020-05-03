import logging

from typing import Dict
from noteline.core import noteline_notebook, envs
from kfp.dsl._container_op import ContainerOp


logger = logging.getLogger(__name__)

DEFAULT_IMAGE = "gcr.io/deeplearning-platform-release/tf-cpu"


class NotelineNbOp(ContainerOp):

  def __init__(self,
               notebook_in: str,
               notebook_out: str = None,
               op_name: str = None,
               image: str = None,
               file_outputs: Dict[str, str] = None,
               **kwargs):
    if not notebook_in:
      raise ValueError("notebook_in can't be empty. Current value: {}".format(
          notebook_in))
    if "command" in kwargs:
      raise ValueError("command should NOT be passed in kwargs")
    if "arguments" in kwargs:
      raise ValueError("arguments should NOT be passed in kwargs")

    if not notebook_out:
      notebook_out = notebook_in
    if not file_outputs:
      file_outputs = {}

    file_outputs["in"] = notebook_in
    file_outputs["out"] = notebook_out

    image_from_notebook = self._attempt_get_image_from_notebook(notebook_in)
    if image and image_from_notebook:
      logger.warning("looks like both input env ({}) provided and env from"
                     " notebook({}). Using env provided explicitly".format(image,
                                                                           image_from_notebook))
    else:
      image = image_from_notebook

    if not image:
      logger.warning("No image provided neither in Notebook metadata nor in by input variable. Using default image: {}"
                     .format(DEFAULT_IMAGE))
      image = DEFAULT_IMAGE

    if not op_name:
      op_name = notebook_in.split("/")[-1].replace(".", "_")

    command = ["nbexecutor"]
    arguments = ["--input-notebook", notebook_in,
                 "--output-notebook", notebook_out]

    super().__init__(name=op_name, image=image, command=command, arguments=arguments, **kwargs)

  def _attempt_get_image_from_notebook(self, notebook_uri):
    noteline_notebook_obj = noteline_notebook.get_noteline_notebook(notebook_uri)
    env = noteline_notebook_obj.get_env()
    if env.get("type", "") == envs.DOCKER_ENV_TYPE:
        return env["uri"]
    return ""
