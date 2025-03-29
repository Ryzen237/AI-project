import numba.cuda as cuda


@cuda.jit(device=True)
def cuda_covariant_derivative(melody, A_mu, output):
    i = cuda.grid(1)
    if i < melody.size:
        if i == 0:
            output[i] = (melody[i + 1] - melody[i]) + 1j * A_mu * melody[i]
        elif i == melody.size - 1:
            output[i] = (melody[i] - melody[i - 1]) + 1j * A_mu * melody[i]
        else:
            output[i] = (melody[i + 1] - melody[i - 1]) / 2 + 1j * A_mu * melody[i]


class CUDAGaugeField:
    def __init__(self, melody):
        self.d_melody = cuda.to_device(melody)
        self.d_output = cuda.device_array_like(melody)

    def compute_derivative(self, A_mu):
        threadsperblock = 32
        blockspergrid = (self.d_melody.size + (threadsperblock - 1)) // threadsperblock
        cuda_covariant_derivative[blockspergrid, threadsperblock](
            self.d_melody, A_mu, self.d_output
        )
        return self.d_output.copy_to_host()