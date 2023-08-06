# coding=utf-8
from torch.utils.data import Dataset
import numpy as np
from typing import Any, Callable, List, Optional, Tuple


class EEGDataset(Dataset):
    """
    This is an abstract class for all EEG dataset in this folder.

    `data` should be Numpy's ndarray: (session, trial, channel, time)
    """
    def __init__(self, data: np.ndarray, targets: np.ndarray):
        self.data = data.astype(np.float32)
        self.targets = targets
        self.sample_rate = None
        self.channel_names = None

    def __getitem__(self, n: int) -> Tuple[np.ndarray, int]:
        """
        Override implementation:
            def __getitem__(self, n: int) -> Tuple[np.ndarray, int]:
                return (self.data[n], self.targets[n])
        """
        return (self.data[n], self.targets[n])

    def __len__(self) -> int:
        return len(self.data)

    def _load_data(self, root: str) -> None:
        raise NotImplementedError

    def set_channel_names(self, channel_names) -> List[str]:
        self.channel_names = channel_names
