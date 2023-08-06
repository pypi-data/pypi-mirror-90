from architectures import efficientnet
import datautils

backbone = efficientnet.efficientnetb0((224, 224, 3))
head = efficientnet.LivenessHead(num_classes=1, dropout1=0.1, dropout2=0.3, feature_embedding_shape=1280)

model = efficientnet.build_classifier(backbone, head)

model.summary()

train_generator, valid_generator = datautils.dataset_generator.load_data(resize_shape=(224, 224),
                                                                         train_data_path="/Users/vamshi/kicflow/datasets/sample_keras_dataset/train",
                                                                         valid_data_path="/Users/vamshi/kicflow/datasets/sample_keras_dataset/validation",
                                                                         train_batch_size=2,
                                                                         valid_batch_size=1,
                                                                         interpolation="lanczos",
                                                                         )


model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])


model.fit(x=train_generator,
          steps_per_epoch=4,
          epochs=2,
          validation_steps=8,
          validation_data=valid_generator,
          verbose=1,
          )
