import numpy as np
import joblib

# Load artifacts
pca = joblib.load("results/pca.pkl")
gps = joblib.load("results/gps.pkl")
scaler = joblib.load("results/scaler.pkl")

def predict_pk(params):
    params_scaled = scaler.transform(np.array(params).reshape(1, -1))

    # Predict PC coefficients
    pc_pred = np.array([gp.predict(params_scaled)[0] for gp in gps])

    # Reconstruct log(Pk) and exponentiate
    log_pk_pred = pca.inverse_transform(pc_pred.reshape(1, -1)).flatten()
    pk_pred = np.exp(log_pk_pred)

    return pk_pred

    