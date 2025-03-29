import numpy as np
from scipy.linalg import expm

class GaugeField:
    def __init__(self, dim=4):
        self.A_mu = np.random.randn(dim)

    def covariant_derivative(self, melody):
        return np.gradient(melody) + 1j * self.A_mu[0] * melody


class SU3Engine:
    def __init__(self):
        self.lambdas = [
            np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),  # Matrice 1
            np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]),  # Matrice 2
            # Ajouter ici les autres matrices de Gell-Mann...
        ]

    def transform(self, rhythm, intensity=0.1):
        gen = self.lambdas[np.random.choice(len(self.lambdas))]
        U = expm(1j * intensity * gen)
        return U @ rhythm @ U.conj().T
