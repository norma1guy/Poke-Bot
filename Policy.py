import torch
from Encoders import StateEncoder

class Actor(torch.nn.Module):

    def __init__(self):
        super().__init__()

        self.encoder = StateEncoder()

        self.actor_net = torch.nn.Sequential(
            torch.nn.Linear(256, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128,8)
        )

    def forward(self, td):
        x = self.encoder(td)
        logits = self.actor_net(x)
        return logits

class Critic(torch.nn.Module):

    def __init__(self):
        super().__init__()
        self.encoder = StateEncoder()

        self.critic_net = torch.nn.Sequential(
            torch.nn.Linear(256, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128,1)
        )

    def forward(self, td):
        x = self.encoder(td)
        state_value = self.critic_net(x)
        return state_value