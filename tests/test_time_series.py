import pytest
from spignos.modeling.time_series_model import TimeSeriesModel

def test_time_series_prediction():
    # Dummy data pour le test
    train_data = [10, 15, 20, 25, 30]
    model = TimeSeriesModel()

    # Entraînement du modèle
    model.train(train_data)

    # Test de la prédiction
    prediction = model.predict_next()
    assert prediction is not None, "La prédiction ne doit pas être None"
    assert isinstance(prediction, (int, float)), "La prédiction doit être un nombre"
