import torch



class Policy(torch.nn) :

    def __init__(self) :

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        super().__init__()
        self.flatten = torch.nn.Flatten()
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(28*28,512),
            torch.nn.ReLU(),
            torch.nn.Linear(512,512),
            torch.nn.ReLU(),
            torch.nn.Linear(512,10)
        )

    def forward(self,state):
        state = self.flatten(state)
        logits = self.linear_relu_stack(state)
        return logits
    
    def get_action(self,state):
        logits = self.forward(state)
        probs = torch.softmax(logits,dim=-1)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        log_prob = dist.log_prob(action)

        return action.item(),log_prob
