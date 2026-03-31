import torch

tensor = torch.rand(3,4)
if torch.cuda.is_available():
    tensor = tensor.to('cuda')
    print(tensor.device)

