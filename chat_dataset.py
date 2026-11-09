import torch

class ChatDataset(torch.utils.data.Dataset):
  """
  A PyTorch Dataset class for chat data.
  """

def __init__(self, X_train, y_train):
    self.n_samples = len(X_train)
    self.x_data = X_train
    self.y_data = y_train

        # ... rest of your ChatDataset class definition ...



  # Support indexing such that dataset[i] can be used to get i-th sample
def __getitem__(self, index):
    """
    Returns a data sample at the given index.

    Args:
      index (int): Index of the sample to retrieve.

    Returns:
      tuple: A tuple containing the bag-of-words representation 
             and the corresponding label of the data sample.
    """
    return self.x_data[index], self.y_data[index]

  # We can call len(dataset) to return the size
def __len__(self):
    """
    Returns the total number of samples in the dataset.

    Returns:
      int: The number of samples in the dataset.
    """
    return self.n_samples

# Example usage (assuming X_train and y_train are defined elsewhere)
dataset = ChatDataset(X_train, y_train)
