from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout

def build_transfer_model(input_shape, num_classes):
    """
    Builds a model using VGG16 as a pre-trained base for transfer learning.
    The VGG16 base layers are frozen, and a new classifier head is added.
    """
    # Load the VGG16 model without the top classification layers
    vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    
    # Freeze the layers of the pre-trained base model
    for layer in vgg_base.layers:
        layer.trainable = False
        
    # Build a new classifier on top of the VGG16 base
    x = vgg_base.output
    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=vgg_base.input, outputs=predictions)
    
    return model

if __name__ == '__main__':
    # Example usage
    model = build_transfer_model(input_shape=(150, 150, 3), num_classes=6)
    model.summary()