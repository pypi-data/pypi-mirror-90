# __all__ = ["load_data", "load_data_fit"]

import tensorflow as tf
from typing import Tuple


def load_data(resize_shape: Tuple[int, int],
              train_data_path: str,
              valid_data_path: str,
              train_batch_size: int,
              valid_batch_size: int,
              interpolation: str,
              ):
    """:arg

    """
    data_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

    train_generator = data_generator.flow_from_directory(directory=train_data_path,
                                                         target_size=resize_shape,
                                                         class_mode='binary',
                                                         batch_size=train_batch_size,
                                                         interpolation=interpolation,
                                                         )

    validation_generator = data_generator.flow_from_directory(directory=valid_data_path,
                                                              target_size=resize_shape,
                                                              class_mode='binary',
                                                              batch_size=valid_batch_size,
                                                              interpolation=interpolation,
                                                              )
    return train_generator, validation_generator


def load_data_fit(resize_shape: Tuple[int, int],
                  data_path: str,
                  train_batch_size: int,
                  interpolation: str,
                  ):
    """:arg

    """
    data_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

    data_generator = data_generator.flow_from_directory(directory=data_path,
                                                        target_size=resize_shape,
                                                        class_mode='binary',
                                                        batch_size=train_batch_size,
                                                        interpolation=interpolation,
                                                        )

    return data_generator
