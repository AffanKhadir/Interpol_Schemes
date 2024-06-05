# SPDX-License-Identifier: GPL-3.0-or-later
# Original author: Sebastian Hutschenreuter (https://github.com/shutsch)

data_params = {
    'seed': 2646,  # Can be None
    'data_name': 'test',  # The arrays will be saved in ./Data/<data_name>. Te inference script needs this name
    'noise_sigma': 5,   # THe noise standard deviation in units of rad/m2
    'do_plot': True,  # if set to true, several plots illustrating groundtruths and the data willbe produced
    'n_data': 26200,  # number of data points, which will be disributed randomly over the domain
}

domain_params = {
    'dx': .05,  # resolution in x
    'dy': .05,  # resolution in x
    'center': [0, 0],  # coordinate of the central pixels on the sky
}


extragal_params = {'model': 'MultivariateGaussian',  # Model for the generation of the extragalactic component, choices are
                                                     # MultivariateGaussian, UnivariateGaussian or <None>
                   'alpha': 2., 'q': 1.,  # Parameters for the eta factor in the MultivariateGaussian case
                   'extragal_sigma': 7, # The standard deviation for the extraglactic RMs (might be modified again )
                   }
