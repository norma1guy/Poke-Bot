import torch


class Actor(torch.nn.Module):

    def __init__(self, state_dim, action_dim):
        super().__init__()

        self.actor_net = torch.nn.Sequential(
            torch.nn.Linear(state_dim, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128,action_dim)
        )

    def forward(self, state):
        logits = self.actor_net(state)
        return logits
        

    def get_action(self, state):
        logits,value = self.forward(state)
        probs = torch.softmax(logits, dim=-1)
        dist = torch.distributions.Categorical(probs)

        action = dist.sample()
        return action.item() + 1, dist.log_prob(action),value


class Critic(torch.nn.Module):

    def __init__(self, state_dim):
        super().__init__()

        self.critic_net = torch.nn.Sequential(
            torch.nn.Linear(state_dim, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128,1)
        )

    def forward(self, state):
        state_value = self.critic_net(state)
        return state_value