from sklearn.metrics import classification_report, confusion_matrix

def evaluate_model(model, test_gen):
    y_true = test_gen.classes
    y_pred = model.predict(test_gen)
    y_pred = y_pred.argmax(axis=1)
    print(classification_report(y_true, y_pred))
    print(confusion_matrix(y_true, y_pred))
