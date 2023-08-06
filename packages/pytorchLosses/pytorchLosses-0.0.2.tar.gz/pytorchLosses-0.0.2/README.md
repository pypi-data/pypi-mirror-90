# Download to develop 

```
pip install -e .[dev]

```

# Examples 

```
import torch

from pytorchLosses import  LabelSmoothingCrossEntropy,GamblersLoss,SCELoss,TruncatedLoss

a = torch.rand(4, 5)
b = torch.randint(0, 2, (4,))

loss_fun = LabelSmoothingCrossEntropy() 
print(loss_fun(a,b))
print(GamblersLoss(a,b))

loss_fun = SCELoss(alpha=1.0,beta=1.0,num_classes=5).cuda()
print(loss_fun(a.cuda(),b.cuda()))

# Yet to test
loss_fun = TruncatedLoss(q=0.7, k=0.5, trainset_size=10000).cuda()
print(loss_fun(a.cuda(),b.cuda(),indexes=1))

```