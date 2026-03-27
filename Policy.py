import torch



class Policy(torch.nn) :

    def __init__(self) :

        self.device = torch.accelerator.current_accelerator().type if torch.accelerator_is_available() else 'cpu'
        super().__init()
        self.flatten = torch.nn.Flatten()
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(28*28,512),
            torch.nn.ReLU(),
            torch.nn.Linear(512,512),
            torch.nn.ReLU(),
            torch.nn.Linear(512,10)
        )

    def forward(self,x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
