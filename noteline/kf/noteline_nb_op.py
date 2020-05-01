from noteline import core


from kfp.dsl._container_op import ContainerOp


class NotelineNbOp(ContainerOp):

    def __init__(self,
                 notebook_in: str,
                 notebook_out: str = None,
                 image: str = None,
                 **kwargs):
        if not notebook_in:
          raise ValueError("notebook_in can't be empty. Current value: {}".format(
              notebook_in))
        if not notebook_out:
          notebook_out = "out_{}".format(notebook_in)
        if not image:
          image = "gcr.io/deeplearning-platform-release/tf-cpu"

        if image and image in kwargs:
          raise ValueError(
              "image should be set as input variable, and not via kwargs")

        if "command" in kwargs:
          raise ValueError("command should NOT be passed in kwargs")
        if "arguments" in kwargs:
          raise ValueError("arguments should NOT be passed in kwargs")

        kwargs["image"] = image
        kwargs["command"] = ["nbexecutor"]
        kwargs["arguments"] = ["--input-notebook", notebook_in,
                               "--output-notebook", notebook_out]

        super().__init__(**kwargs)