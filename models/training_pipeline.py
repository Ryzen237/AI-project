import torch
from torch.utils.data import Dataset, DataLoader


class MusicDataset(Dataset):
    def __init__(self, midi_files):
        self.data = self.process_midi(midi_files)

    def process_midi(self, files):
        # Convertir les fichiers MIDI en tenseurs
        pass

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return torch.tensor(self.data[idx][0]), torch.tensor(self.data[idx][1]))

        def train_model():
            dataset = MusicDataset("data/midi/*.mid")
            loader = DataLoader(dataset, batch_size=32, shuffle=True)

            model = GaugeTransformer().cuda()
            optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

            for epoch in range(100):
                for x, y in loader:
                    x, y = x.cuda(), y.cuda()
                    pred = model(x)
                    loss = torch.nn.functional.mse_loss(pred, y)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()