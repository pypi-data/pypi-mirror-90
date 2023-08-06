import unittest
import torch

from minibert import MiniBert


class TestMiniBert(unittest.TestCase):
    def test_minibert_not_fail(self):
        minibert = MiniBert(10, 10, 10)
        x = torch.tensor([
            [0, 1, 3, 4],
            [0, 1, 3, 4],
            [0, 1, 3, 4]
        ])
        out = minibert(x)


if __name__ == '__main__':
    unittest.main()
