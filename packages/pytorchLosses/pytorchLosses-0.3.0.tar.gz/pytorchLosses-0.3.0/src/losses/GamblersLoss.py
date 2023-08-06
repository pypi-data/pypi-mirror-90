import torch.nn.functional as F
import torch 

reward = 0.6
def GamblersLoss(outputs,target):
        outputs  = F.softmax(outputs,dim=1)        
        outputs, reservation = outputs[:,:-1], outputs[:,-1]
        gain = torch.gather(outputs, dim=1, index=target.unsqueeze(1)).squeeze()

        doubling_rate = (gain.add(reservation.div(reward))).log()
        
        loss = -outputs.mean()
        return loss