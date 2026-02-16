# pk_emulator

`pk_emulator` is a Python-based interactive tool for emulating the **non-linear matter power spectrum**. It allows you to vary cosmological parameters in real-time and see the resulting power spectrum instantly. This is particularly useful for educational purposes.

The emulator uses a pre-trained model to predict the power spectrum without needing to run expensive Boltzmann solvers like CAMB every time, making it fast and efficient.

## Features

- Interactive Dash web interface with sliders for cosmological parameters:
  - Hubble constant, $h$.
  - Cold dark matter density, $\Omega_c$.
  - Baryon density, $\Omega_b$.
  - Scalar amplitude, $A_s \cdot 10^9$.
  - Scalar spectral index, $n_s$.
  - Sum of neutrino masses, $\sum_\nu m_\nu$.
- Real-time plot updates for the matter power spectrum $P(k)$.
- Reset to default cosmological parameters with one click.

## Requirements

- numpy
- dash
- plotly
- joblib
- matplotlib
- scikit-learn
- camb
- tqdm
- scipy
