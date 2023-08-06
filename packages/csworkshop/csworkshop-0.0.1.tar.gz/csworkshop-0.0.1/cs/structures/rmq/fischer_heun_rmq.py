import math
from typing import Dict, List

from .precomputed_rmq import PrecomputedRMQ
from .rmq import RMQ
from .sparse_table_rmq import SparseTableRMQ


def calc_cart_num(arr: List[int]) -> int:
    """
    Calculate cartesian number
    >>> arr = [93, 84, 33, 64, 62, 83, 63, 58]
    >>> calc_cart_num(arr) == int('1010110110100100'[::-1], 2)
    True
    >>> arr = [1, 2, 0, 4, 5]
    >>> arr2 = [17, 34, 5, 100, 120]
    >>> calc_cart_num(arr) == calc_cart_num(arr2)
    True
    >>> arr = [952, 946, 414, 894, 675, 154, 627, 154, 414]
    >>> arr2 = [764, 319, 198, 680, 376, 113, 836, 368, 831]
    >>> calc_cart_num(arr) == calc_cart_num(arr2)
    True
    """
    result = ""
    stack: List[int] = []
    for elem in arr:
        if not stack:
            stack.append(elem)
            result = "1" + result
        else:
            while len(stack) > 0 and stack[-1] > elem:
                stack.pop()
                result = "0" + result
            stack.append(elem)
            result = "1" + result
    return int(result, 2)


class FischerHeunRMQ(RMQ):
    def __init__(self, elems: List[int]) -> None:
        super().__init__(elems)
        self.block_size = max(1, math.floor(math.log2(len(elems))) // 4)
        self.block_mins = []
        block_min_vals = []
        for i in range(0, len(elems), self.block_size):
            curr_min = i
            for j in range(i + 1, min(i + self.block_size, len(elems))):
                curr_min = self.return_smaller_index(j, curr_min)
            self.block_mins.append(curr_min)
            block_min_vals.append(elems[curr_min])

        self.summary_rmq = SparseTableRMQ(block_min_vals)

        self.block_index_to_cart = []
        # Can also use:  [None] * (4 ** self.block_size)
        self.cart_to_rmq: Dict[int, RMQ] = {}
        for i in range(math.ceil(len(elems) / self.block_size)):
            start = i * self.block_size
            current_range = self.elems[start : min(len(elems), start + self.block_size)]
            cartesian_num = calc_cart_num(current_range)
            self.block_index_to_cart.append(cartesian_num)
            if cartesian_num not in self.cart_to_rmq:
                self.cart_to_rmq[cartesian_num] = PrecomputedRMQ(current_range)

    def rmq(self, low: int, high: int) -> int:
        if low >= high:
            raise RuntimeError("In the range, low must be lower than high.")

        min_index = -1
        if high - low < self.block_size:
            for i in range(low, high):
                min_index = self.return_smaller_index(i, min_index)
            return min_index

        start_block = math.ceil(low / self.block_size)
        end_block = math.floor(high / self.block_size)

        if start_block < end_block:
            block_min_index = self.summary_rmq.rmq(start_block, end_block)
            min_index = self.block_mins[block_min_index]

        if low < start_block * self.block_size:
            block_rmq = self.cart_to_rmq[self.block_index_to_cart[start_block - 1]]
            adjust_factor = (start_block - 1) * self.block_size
            new_index = (
                block_rmq.rmq(low - adjust_factor, len(block_rmq.elems)) + adjust_factor
            )
            min_index = self.return_smaller_index(new_index, min_index)

        if end_block * self.block_size < high:
            block_rmq = self.cart_to_rmq[self.block_index_to_cart[end_block]]
            adjust_factor = end_block * self.block_size
            new_index = block_rmq.rmq(0, high - adjust_factor) + adjust_factor
            min_index = self.return_smaller_index(new_index, min_index)

        return min_index
