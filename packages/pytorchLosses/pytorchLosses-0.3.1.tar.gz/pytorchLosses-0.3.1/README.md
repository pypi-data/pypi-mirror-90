# Install to use

```
pip install pytorchLosses
```



# Examples 

```
from pytorchLosses import  LabelSmoothingCrossEntropy,GamblersLoss,SCELoss,TruncatedLoss,FocalCosineLoss

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

loss_fun = FocalCosineLoss(alpha=1.0, gamma=2.0,xent=0.1).cuda()
print(loss_fun(a.cuda(),b.cuda()))

```

# Explanation 
 - [Label encoding](#Label_encoding)
 - 

## Label_encoding
Neural net face 2 major error that are we usually told in every course and 1 major issue that is not famous which is called over confidence. 
- ### Over confidence 
  consider 100 examples within our dataset, each with predicted probability 0.9 by our model. If our model is calibrated, then 90 examples should be classified correctly. Similarly, among another 100 examples with predicted probabilities 0.6, we would expect only 60 examples being correctly classified. Copied form [here](https://towardsdatascience.com/what-is-label-smoothing-108debd7ef06). Read full artical and if you like him love by applauding his work.
  So basically convert [(0,1)] prediction to [(0.0333,0.9666)]

# Download to develop 

```
pip install -e .[dev]

```
