import tensorflow as tf
from gan_recover_image.SRGAN.networks import Generator
import os


class SRGanSingletone:
    __instance__ = None
    GEN = None

    def __init__(self):
        if SRGanSingletone.__instance__ is None:
            SRGanSingletone.__instance__ = self
            ckpt_path = "../SRGAN/training_ckp_generator/checkpoint"
            ckpt_dir = os.path.dirname(ckpt_path)
            self.Gen = Generator(input_shape=(64, 64, 3))
            latest_ckpt = tf.train.latest_checkpoint(ckpt_dir)
            assert latest_ckpt is not None, "Your path of checkpoint is wrong or there's no checkpoint!"
            ckpt = tf.train.Checkpoint(net=self.Gen)
            ckpt.restore(latest_ckpt)
        else:
            raise Exception("You cannot create another SRGanSingletone class")

    @staticmethod
    def get_instance():
        if not SRGanSingletone.__instance__:
            SRGanSingletone()
        return SRGanSingletone.__instance__
