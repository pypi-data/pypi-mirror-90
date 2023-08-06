import torch

from pytorchLosses import  LabelSmoothingCrossEntropy

a = torch.rand(4, 3)
b = torch.randint(0, 2, (4,))

loss_fun = LabelSmoothingCrossEntropy() 
print(
    loss_fun(
        a,b
        )
)