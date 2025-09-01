import os
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from src1.model.transfer_model import build_transfer_model
from src1.preprocessing.prepare import get_data_generators
# Paths
DATA_DIR = "D://assignment//datasets//seg_test//seg_test"        # Change this to your dataset folder
MODEL_DIR = "D://assignment//models"
MODEL_PATH = os.path.join('D://assignment//models', "transfer_model_best.h5")

def train_transfer_cnn():
    os.makedirs(MODEL_DIR, exist_ok=True)

    train_gen, val_gen = get_data_generators(DATA_DIR)

    model = build_transfer_model(
        input_shape=(150, 150, 3),
        num_classes=train_gen.num_classes
    )

    checkpoint = ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    )

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics=['accuracy'])
    # Train model
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=10,
        callbacks=[checkpoint, early_stop]
    )

    print(f"✅ Training complete! Best transfer learning model saved at: {MODEL_PATH}")
    return history

if __name__ == "__main__":
    train_transfer_cnn()
