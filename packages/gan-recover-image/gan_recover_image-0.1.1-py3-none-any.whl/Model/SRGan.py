import tensorflow as tf
from SRGAN.networks import Generator
import os
import numpy as np
import time
from PIL import Image
import argparse


class SRGan:
    def __init__(self):
        pass
    def recover(self, image_recover):

        args = self.create_defaut_args()
        
        assert args.model in (
            "SRGAN", "VAEGAN", "Pix2Pix", "CycleGAN"), "--model must be SRGAN, VAEGAN, Pix2Pix or CycleGAN."
        assert args.width > 0 and args.height > 0, "--width and --height > 0."
        if not os.path.isdir(args.save_path):
            os.makedirs(args.save_path)
        if args.model == "SRGAN":
            ckpt_path = "../SRGAN/training_ckp_generator/checkpoint"
            ckpt_dir = os.path.dirname(ckpt_path)
            Gen = Generator(input_shape=(args.height, args.width, 3))
            latest_ckpt = tf.train.latest_checkpoint(ckpt_dir)

            assert latest_ckpt is not None, "Your path of checkpoint is wrong or there's no checkpoint!"

            ckpt = tf.train.Checkpoint(net=Gen)
            ckpt.restore(latest_ckpt)

            image, real_width, real_height = self.load_image(image_recover, args.width, args.height)
            start = time.time()
            # recover image
            predicted = Gen.predict(image, real_width, real_height, save_name=args.save_name, save_path=args.save_path)

            time_cal = time.time() - start
            predicted.show()
        elif args.model == "VAEGAN":
            pass
        elif args.model == "Pix2Pix":
            pass
        elif args.model == "CycleGAN":
            pass

        print("gan_recover_image using: {}".format(args.model))
        print("Time of recovering this image is {} s.".format(time_cal))
        print("Results are saved at {}/*.jpg".format(args.save_path))

    def load_image(self, image_path, width, height):

        image = Image.open(image_path)
        assert image is not None, "Can't load image!"
        real_width, real_height = image.size
        image = image.resize([width, height], Image.ANTIALIAS)
        image = (np.array(image) - 127.5) / 127.5
        image = np.expand_dims(image, axis=0)
        return image, real_width, real_height

    def create_defaut_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--save_path", type=str, default="result/SRGAN", help="Save image to this path.")
        parser.add_argument("--save_name", type=str, default="result.jpg", help="Name of saved image.")
        parser.add_argument("--width", type=int, default=64,
                            help="Resize image to this width. (must be suitable to your model)")
        parser.add_argument("--height", type=int, default=64,
                            help="Resize image to this height. (must be suitable to your model)")
        parser.add_argument("--model", type=str, default="SRGAN",
                            help="Choose model to recover image (SRGAN, VAEGAN, Pix2Pix, CycleGAN).")
        args = parser.parse_args()
        return args
