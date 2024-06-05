# SPDX-License-Identifier: GPL-3.0-or-later
# Original author: Sebastian Hutschenreuter (https://github.com/shutsch)

import numpy as np


def get_mock_data(location, data_name):
    # These
    data_path = './Data/' + location + '/' + data_name + '/'
    data = np.load(data_path + 'data.npy')
    std = np.load(data_path + 'noise_sigma.npy')
    theta = np.load(data_path + 'theta.npy')
    phi = np.load(data_path + 'phi.npy')

    return theta, phi, data, std


def get_real_data():
    raise NotImplementedError()
    
    
def get_simulated_data():
    raise NotImplementedError()
