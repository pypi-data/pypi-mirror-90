import unittest
import torch
from torch.nn import functional as F
from math import sqrt

from minibert import Attention


class TestAttention(unittest.TestCase):
    def test_attention_given_matrix(self):
        k = torch.tensor([[0, 0.5], [1, 0], [0.5, 0.5]], dtype=torch.float)
        q = torch.tensor([[0, 0.5], [0, 0], [0.5, 0.5]], dtype=torch.float)
        v = torch.tensor([[0.5, 0.5], [1, 0.5], [1, 1]], dtype=torch.float)
        attention = Attention.from_weights(k, q, v)

        x = torch.tensor(
            [[1, 0, 1], [1, 1, 1], [0, 0, 1]], dtype=torch.float)

        xk = torch.tensor([[0.5, 1], [1.5, 1], [0.5, 0.5]], dtype=torch.float)
        xq = torch.tensor([[0.5, 1], [0.5, 1], [0.5, 0.5]], dtype=torch.float)
        xv = torch.tensor([[1.5, 1.5], [2.5, 2], [1, 1]], dtype=torch.float)

        x_qk = torch.matmul(xq, xk.t()) / sqrt(2)
        expected = torch.matmul(F.softmax(x_qk, dim=1), xv)

        actual = attention(x)
        self.assertTrue(torch.equal(expected, actual))

    def test_attention_given_batch(self):
        k = torch.tensor([[0, 0.5], [1, 0], [0.5, 0.5]], dtype=torch.float)
        q = torch.tensor([[0, 0.5], [0, 0], [0.5, 0.5]], dtype=torch.float)
        v = torch.tensor([[0.5, 0.5], [1, 0.5], [1, 1]], dtype=torch.float)
        attention = Attention.from_weights(k, q, v)

        x = torch.tensor(
            [[1, 0, 1], [1, 1, 1], [0, 0, 1]], dtype=torch.float)
        batch = torch.stack([x, x, x])

        xk = torch.tensor([[0.5, 1], [1.5, 1], [0.5, 0.5]], dtype=torch.float)
        xq = torch.tensor([[0.5, 1], [0.5, 1], [0.5, 0.5]], dtype=torch.float)
        xv = torch.tensor([[1.5, 1.5], [2.5, 2], [1, 1]], dtype=torch.float)

        x_qk = torch.matmul(xq, xk.t()) / sqrt(2)
        expected = torch.matmul(F.softmax(x_qk, dim=1), xv)
        expected = torch.stack([expected, expected, expected])

        actual = attention(batch)
        self.assertTrue(torch.equal(expected, actual))


if __name__ == '__main__':
    unittest.main()
