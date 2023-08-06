import multiprocessing
from multiprocessing import Lock, Process
import os
import numpy as np
import time
from PIL import Image
import argparse

from gan_recover_image.NetWork.factory_network import SRGanSingletone


def recover_async(image_recover):

    model= "SRGAN"
    height=64
    width=64
    save_path= "result/SRGAN"
    save_name="result.jpg"


    assert model in (
        "SRGAN", "VAEGAN", "Pix2Pix", "CycleGAN"), "--model must be SRGAN, VAEGAN, Pix2Pix or CycleGAN."
    assert width > 0 and height > 0, "--width and --height > 0."
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    if model == "SRGAN":
        image, real_width, real_height = load_image(image_recover, width, height)
        start = time.time()
        # recover image
        predicted = SRGanSingletone.get_instance().Gen.predict(image, real_width, real_height,
                                                               save_name=save_name, save_path=save_path)
        time_cal = time.time() - start

        print("gan_recover_image using: {}".format(model))
        print("Time of recovering this image is {} s.".format(time_cal))
        print("Results are saved at {}/*.jpg".format(save_path))
        # return image has been recovery
        return predicted
    elif model == "VAEGAN":
        pass
    elif model == "Pix2Pix":
        pass
    elif model == "CycleGAN":
        pass

def load_image(image_path, width, height):
    image = Image.open(image_path)
    assert image is not None, "Can't load image!"
    real_width, real_height = image.size
    image = image.resize([width, height], Image.ANTIALIAS)
    image = (np.array(image) - 127.5) / 127.5
    image = np.expand_dims(image, axis=0)
    time.sleep(2)
    return image, real_width, real_height


def create_defaut_args():
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


def load_image_task(balance, q1, q2, lock):
    while not q1.empty():
        value = q1.get()
        image = Image.open(value.image)
        assert image is not None, "Can't load image!"
        real_width, real_height = image.size
        image = image.resize([value.width, value.height], Image.ANTIALIAS)
        image = (np.array(image) - 127.5) / 127.5
        image = np.expand_dims(image, axis=0)
        value.image = image
        value.width = real_width
        value.height = real_height
        print('thread1 is handing {0}'.format(value))
        time.sleep(2)
        lock.acquire()
        q2.put(value)
        lock.release()
    lock.acquire()
    balance.value = False
    lock.release()


def recover_image_task(balance, q2, q3, lock):
    while balance.value:
        while not q2.empty():
            lock.acquire()
            value = q2.get()
            lock.release()
            predicted = SRGanSingletone.get_instance().Gen.predict(value.image, value.width, value.height,
                                                                   save_name="result.jpg",
                                                                   save_path="result/SRGAN")
            print('thread2 is handing {0}'.format(value))
            value.image = predicted
            q3.put(value)
    # while not q2.empty():
    #     lock.acquire()
    #     value = q2.get()
    #     lock.release()
    #     predicted = SRGanSingletone.get_instance().Gen.predict(value.image, value.width, value.height,
    #                                                            save_name="result.jpg",
    #                                                            save_path="result/SRGAN")
    #     print('thread2 is handing {0}'.format(value))
    #     result = ImageModel(predicted, 64, 64)
    #     lock.acquire()
    #     q3.put(result)
    #     lock.release()
    print("Finish")


def dump_queue(queqe):
    result = []
    while not queqe.empty():
        result.append(queqe.get())
    return result


def recover_performce(images):
    # core = multiprocessing.cpu_count()
    # assert core >= 3, "Core of CPU have to >= 3"
    with multiprocessing.Manager() as manager:
        balance = multiprocessing.Value('i', True)
        queqe2 = manager.Queue()
        queqe3 = manager.Queue()
        # queqe1 = manager.Queue()
        # for image in images:
        #     queqe1.put(image)
        lock = Lock()
        p1 = Process(target=load_image_task, args=(balance, images, queqe2, lock))
        p2 = Process(target=recover_image_task, args=(balance, queqe2, queqe3, lock))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        # result = dump_queue(queqe3)
        # return result
