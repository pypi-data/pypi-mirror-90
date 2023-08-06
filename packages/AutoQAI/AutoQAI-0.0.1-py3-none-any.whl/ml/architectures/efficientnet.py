import tensorflow as tf
from typing import Tuple


def efficientnetb0(input_shape: Tuple[int, int, int]) -> tf.keras.Model:

    model = tf.keras.applications.EfficientNetB0(
        include_top=False, weights="imagenet", input_shape=input_shape
    )
    outputs = tf.keras.layers.GlobalAveragePooling2D()(model.output)
    model = tf.keras.Model(inputs=model.input, outputs=outputs, name="EfficientNetB0")
    return model

def LivenessHead(
    num_classes: int,
    classifier_activation: str = "softmax",
    dropout1: float = 0.3,
    dropout2: float = 0.3,
    dense1_neurons: int = 20,
    dense2_neurons: int = 10,
    feature_embedding_shape: int = 1280,
    hidden_activation: str = "relu",
) -> tf.keras.Model:

    inputs = tf.keras.layers.Input(shape=feature_embedding_shape)
    dropout_0 = tf.keras.layers.Dropout(dropout1)(inputs)
    dense_0 = tf.keras.layers.Dense(dense1_neurons, activation=hidden_activation)(
        dropout_0
    )
    dropout_1 = tf.keras.layers.Dropout(dropout2)(dense_0)
    dense_1 = tf.keras.layers.Dense(dense2_neurons, activation=hidden_activation)(
        dropout_1
    )
    dense_2 = tf.keras.layers.Dense(num_classes, activation=classifier_activation)(
        dense_1
    )
    head = tf.keras.models.Model(inputs=inputs, outputs=dense_2)

    return head


def build_classifier(backbone, head) -> tf.keras.Model:
    """:arg

    """
    output = head(backbone.output)
    model = tf.keras.Model(inputs=backbone.input, outputs=output, name=backbone.name)

    return model


if __name__ == '__main__':
    backbone = efficientnetb0((224, 224, 3))
    head = LivenessHead(num_classes=1, dropout1=0.1, dropout2=0.3, feature_embedding_shape=1280)
    model = build_classifier(backbone, head)
    model.summary()
