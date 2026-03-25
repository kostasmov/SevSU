# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from model import DeepQNetwork
import torch 

net1=DeepQNetwork(1,1,1)
net2=DeepQNetwork(1,1,2)

par1=[p.shape for p in net1.parameters()]

print('par1=',par1)

par2=[p.shape for p in net2.parameters()]

print('par2=',par2)

#print(net1.optimizer())

states=torch.tensor([1.0], dtype=torch.float64)
Q_target=torch.tensor([1.0], dtype=torch.float64)
#print(type(states.item))

#print(list(net1.parameters()))
net1.gradient_update(states, Q_target)
print('grad1=',list(net1.parameters()))

net2.gradient_update(states, Q_target)
print('grad2=',list(net2.parameters()))
print('grad1=',list(net1.parameters()))

print('MSE LOSS')
x1 = torch.rand(10,2)
x2 = torch.rand(10,2)

mse_torch = torch.nn.functional.mse_loss(x1,x2)
print(mse_torch) # 0.1557

mse_torch = torch.nn.functional.mse_loss(x1,x2,reduction='mean')
print(mse_torch) # 0.1557