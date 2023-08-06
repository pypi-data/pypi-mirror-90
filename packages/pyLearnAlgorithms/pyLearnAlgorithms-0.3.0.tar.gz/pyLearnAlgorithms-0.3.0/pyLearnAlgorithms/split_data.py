import numpy as np

class SplitData():
    """class responsible for dividing the data"""
    
    def __init__(self, data):
        # data to be divided
        self.data = data
        
        return None
    
    def split_train_test(self, test_ratio):
        """divides data for training and testing"""

        if type(self.data) == dict:
            # matlab file is not yet supported
            print('unsupported data format')

            return None, None

        shuffled_indices = np.random.permutation(len(self.data))
        test_set_size = int(len(self.data) * test_ratio)
        test_indices = shuffled_indices[:test_set_size]
        train_indices = shuffled_indices[test_set_size:]

        return self.data.iloc[train_indices], self.data.iloc[test_indices]
    
    def split_train_test_val(self, test_ratio, val_ratio):
        """divides data for training, validation and testing"""

        if type(self.data) == dict:
            # matlab file is not yet supported
            print('unsupported data format')

            return None, None, None

        shuffled_indices = np.random.permutation(len(self.data))
        test_set_size = int(len(self.data) * test_ratio)
        val_set_size = int(len(self.data) * val_ratio)
        test_indices = shuffled_indices[:test_set_size]
        val_indices = shuffled_indices[test_set_size:(val_set_size + test_set_size)]
        train_indices = shuffled_indices[(val_set_size + test_set_size):]

        return self.data.iloc[train_indices], self.data.iloc[test_indices], self.data.iloc[val_indices]

