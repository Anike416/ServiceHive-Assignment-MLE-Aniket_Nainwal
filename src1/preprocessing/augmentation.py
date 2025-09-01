from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_augmented_generator(data_dir, img_size=(150,150), batch_size=32):
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2
    )

    return datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size
    )
