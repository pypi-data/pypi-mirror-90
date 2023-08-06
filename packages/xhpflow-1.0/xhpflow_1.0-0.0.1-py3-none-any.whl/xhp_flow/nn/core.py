import numpy as np
class Node:
    """
    我们把这个Node类作为这个神经网络的基础模块
    """

    def __init__(self, inputs=[], name=None, is_trainable=False):
        self.inputs = inputs  # 这个节点的输入，输入的是Node组成的列表
        self.outputs = []  # 这个节点的输出节点
        self.name = name
        self.is_trainable = is_trainable
        for n in self.inputs:
            n.outputs.append(self)  # 这个节点正好对应了这个输人的输出节点，从而建立了连接关系

        self.value = None  # 每个节点必定对应有一个值

        self.gradients = {}  # 每个节点对上个节点的梯度，

    def forward(self):
        """
        先预留一个方法接口不实现，在其子类中实现,且要求其子类一定要实现，不实现的时话会报错。
        """
        raise NotImplemented

    def backward(self):
        raise NotImplemented

    def __repr__(self):
        return "Node:{}".format(self.name)

    
class Placeholder(Node):
    """
    作为x,k,b,weights和bias这类需要赋初始值和更新值的类
    """

    def __init__(self, name=None, is_trainable=True):

        Node.__init__(self, name=name, is_trainable=is_trainable)

    def forward(self, value=None):

        if value is not None: self.value = value

    def backward(self):

        self.gradients[self] = np.zeros_like(self.value).reshape((self.value.shape[0], -1))

        for n in self.outputs:
            self.gradients[self] += n.gradients[self].reshape((n.gradients[self].shape[0], -1))  # 没有输入。


class Linear(Node):

    def __init__(self, x=None, weight=None, bias=None, name=None, is_trainable=False):
        Node.__init__(self, [x, weight, bias], name=name, is_trainable=is_trainable)

    def forward(self):
        k, x, b = self.inputs[1], self.inputs[0], self.inputs[2]

        self.value = np.dot(x.value, k.value) + b.value.squeeze()

    def backward(self):
        k, x, b = self.inputs[1], self.inputs[0], self.inputs[2]

        self.gradients[k] = np.zeros_like(k.value)
        self.gradients[b] = np.zeros_like(b.value).reshape((len(np.zeros_like(b.value))))
        self.gradients[x] = np.zeros_like(x.value)

        for n in self.outputs:
            gradients_from_loss_to_self = n.gradients[self]
            self.gradients[k] += np.dot(gradients_from_loss_to_self.T, x.value).T
            self.gradients[b] += np.mean(gradients_from_loss_to_self, axis=0, keepdims=False).reshape(
                (len(np.zeros_like(b.value))))
            self.gradients[x] += np.dot(gradients_from_loss_to_self, k.value.T)


class Sigmoid(Node):

    def __init__(self, x, name=None, is_trainable=False):
        Node.__init__(self, [x], name=name, is_trainable=is_trainable)
        self.x = self.inputs[0]

    def _Sigmoid(self, x):
        return 1. / (1 + np.exp(-1 * x))

    def forward(self):
        self.value = self._Sigmoid(self.x.value)

    def partial(self):
        return self._Sigmoid(self.x.value) * (1 - self._Sigmoid(self.x.value))

    def backward(self):
        self.gradients[self.x] = np.zeros_like(self.value)

        for n in self.outputs:
            gradients_from_loss_to_self = n.gradients[self]  # 输出节点对这个节点的偏导，self：指的是本身这个节点
            self.gradients[self.x] += gradients_from_loss_to_self * self.partial()


class ReLu(Node):
    def __init__(self, x, name=None, is_trainable=False):
        Node.__init__(self, [x], name=name, is_trainable=is_trainable)
        self.x = self.inputs[0]

    def forward(self):
        self.value = self.x.value * (self.x.value > 0)

    def backward(self):
        self.gradients[self.x] = np.zeros_like(self.value)

        for n in self.outputs:
            gradients_from_loss_to_self = n.gradients[self]
            self.gradients[self.x] += gradients_from_loss_to_self * (self.x.value > 0)


class MSE(Node):

    def __init__(self, y_pre, y, name, is_trainable=False):
        Node.__init__(self, [y_pre, y], name=name, is_trainable=is_trainable)
        self.y_pre, self.y = self.inputs[0], self.inputs[1]

    def forward(self):
        y = self.y.value.reshape(-1, 1)
        y_pre = self.y_pre.value.reshape(-1, 1)

        assert (y.shape == y_pre.shape)

        self.m = self.inputs[0].value.shape[0]
        self.diff = y - y_pre

        self.value = np.mean(self.diff ** 2)

    def backward(self):
        self.gradients[self.y] = (2 / self.m) * self.diff
        self.gradients[self.y_pre] = (-2 / self.m) * self.diff
