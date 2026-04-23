import torch



class Policy(torch.nn.Module):

    def __init__(self, state_dim, action_dim):
        super().__init__()

        self.net = torch.nn.Sequential(
            torch.nn.Linear(state_dim, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.net(x)

    def get_action(self, state):
        logits = self.forward(state)
        probs = torch.softmax(logits, dim=-1)
        dist = torch.distributions.Categorical(probs)

        action = dist.sample()
        return action.item() + 1, dist.log_prob(action)
