import torch


class CUDAMusicalHMC(MusicalHMC):
    def __init__(self, melody):
        super().__init__(melody)
        self.melody = torch.tensor(melody, device='cuda')
        self.momentum = torch.cuda.FloatTensor(melody.shape).normal_()

    @torch.jit.script
    def cuda_gradient(self, A_mu: torch.Tensor) -> torch.Tensor:
        return torch.diff(self.melody) + 1j * A_mu * self.melody[1:-1]