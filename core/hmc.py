import numpy as np


class MusicalHMC:
    def __init__(self, melody, mass=1.0):
        self.melody = melody.astype(np.float64)
        self.momentum = np.random.randn(*melody.shape)
        self.mass = mass

    def potential_energy(self, gauge_field):
        D_melody = gauge_field.covariant_derivative(self.melody)
        return np.linalg.norm(D_melody) ** 2

    def leapfrog(self, gauge_field, steps=10, dt=0.1):
        new_melody = np.copy(self.melody)
        new_momentum = np.copy(self.momentum)

        # Demi-step initial pour le momentum
        grad = self.compute_gradient(gauge_field)
        new_momentum -= 0.5 * dt * grad

        # Intégration complète
        for _ in range(steps):
            new_melody += dt * new_momentum / self.mass
            grad = self.compute_gradient(gauge_field)
            new_momentum -= dt * grad

        # Dernier demi-step
        grad = self.compute_gradient(gauge_field)
        new_momentum -= 0.5 * dt * grad

        return new_melody, new_momentum

    def compute_gradient(self, gauge_field):
        epsilon = 1e-5
        grad = np.zeros_like(self.melody)
        for i in range(len(self.melody)):
            delta = np.zeros_like(self.melody)
            delta[i] = epsilon
            grad[i] = (self.potential_energy(gauge_field, self.melody + delta) -
                       self.potential_energy(gauge_field, self.melody - delta)) / (2 * epsilon)
        return grad