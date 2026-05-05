from torchrl.envs.transforms import Transform
import torch

class FlattenEachTensor(Transform):
    def _call(self, td):
        for key, val in td.items(True):
            if torch.is_tensor(val):
                td.set(key, val.reshape(-1))
        return td