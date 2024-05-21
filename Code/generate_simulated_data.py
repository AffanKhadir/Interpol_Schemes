import os
import nifty8 as ift
import numpy as np
import matplotlib.pyplot as pl
import sys
import importlib

from src import load_field_model, PlaneProjector, InverseGammaOperator


def main(data_name, n_data, do_plot, noise_sigma, seed,  # general setup
         domain_parameters,  # domain parameters,
         extragal_params, simulation_name = 'Results_Patchy' # model parameter dictionaries
         ):

    ift.random.push_sseq_from_seed(seed)
    # Setting up directories if necessary
    if 'Patchy' in simulation_name:
        data_path = './Data/simulated_patchy/' + data_name + '/'
    elif 'Filamentary' in simulation_name:
        data_path = './Data/simulated_fil/' + data_name + '/'
    else:
        data_path = './Data/simulated_example/' + data_name + '/'
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Construct the data and sky domains, i.e. the spaces on which the fields live and connet them via response operator

    data_domain = ift.makeDomain(ift.UnstructuredDomain((n_data,)))
    
    simulation_path = "../Simulations/"+simulation_name+"/all_boxes_sim_nth_sim_b_gaussian_dir0/"
    
    true_rm = np.load(simulation_path + 'RM.npy')
    
    nx, ny = true_rm.shape

    dx = domain_parameters['dx']
    dy = domain_parameters['dy']
    center = domain_parameters['center']
    signal_domain = ift.makeDomain(ift.RGSpace(shape=(nx, ny), distances=(dx, dy)))
    true_rm = ift.Field(signal_domain, true_rm)
    phi = center[0] - nx*dx/2 + nx*dx*np.random.uniform(0, 1, n_data)
    theta = center[1] - ny*dy/2 + ny*dy*np.random.uniform(0, 1, n_data)
    response = PlaneProjector(theta=theta, phi=phi, target=data_domain, domain=signal_domain, center=center)

    #  ################### BUILDING THE MODELS ##############

    # Setting up the sky models.


    # calculate the mocksk from a random sample

    if do_plot:
        plot = ift.Plot()
        plot.add(true_rm, title='rm')
        plot.output(name=data_path + 'true_skies.png')

    # calculate the galactic contrbution to the data
    gal_rm = response(true_rm)

    # We have three option implement the extraglactic component

    if extragal_params['model'] == 'UnivariateGaussian':
        # Option A: gaussian model with a single standard deviation for all extra galactic rms
        extragal_rm = extragal_params['extragal_sigma']*ift.from_random(data_domain)
        full_rm = gal_rm + extragal_rm

        if do_plot:
            pl.figure()
            pl.scatter(gal_rm.val, extragal_rm.val)
            pl.xlabel('Galactic RM')
            pl.ylabel('Extragalactic RM')
            pl.savefig(data_path + 'gal_vs_egal_scatter.png')

    elif extragal_params['model'] == 'MultivariateGaussian':
        # Option B: gaussian model with a varying standard deviation for all extra galactic rms
        # the factor steering the variation is modelled via an inverse gamma distribution, allowing for a lot of variation for some sigmas
        ivg = InverseGammaOperator(data_domain, alpha=extragal_params['alpha'], q=extragal_params['q'])
        eta = ivg(ift.from_random(data_domain))
        extragal_sigma = (extragal_params['extragal_sigma']**2*eta).sqrt()
        extragal_rm = extragal_sigma*ift.from_random(data_domain)
        full_rm = gal_rm + extragal_rm

        if do_plot:
            pl.figure()
            pl.scatter(gal_rm.val, extragal_rm.val)
            pl.xlabel('Galactic RM')
            pl.ylabel('Extragalactic RM')
            pl.savefig(data_path + 'gal_vs_egal_scatter.png')

    elif extragal_params['model'] is None:
        extragal_sigma = None
        extragal_rm = None
        full_rm = gal_rm
    else:
        raise KeyError('Unkown extragalactic RM model (allowed are univariate, multivariate or None)')

    noise = noise_sigma*ift.from_random(data_domain)

    data = full_rm + noise

    if do_plot:
        pl.figure()
        pl.scatter(gal_rm.val, data.val)
        pl.xlabel('RM_gal')
        pl.ylabel('data')
        pl.savefig(data_path + 'RM_gal_vs_data_scatter.png')

        pl.figure()
        pl.scatter(theta, phi)
        pl.xlabel('theta')
        pl.ylabel('phi')
        pl.savefig(data_path + 'coordinate_scatter.png')

        data_adjoint_dict = {'data': response.adjoint(data),
                             'angular_position': response.counts()}
        for name, data_adjoint in data_adjoint_dict.items():
            plot = ift.Plot()
            plot.add(data_adjoint)
            plot.output(name=data_path + 'data_projection.png')


    # these four arrays will be loaded in the Inference
    np.save(data_path + 'data', data.val)
    np.save(data_path + 'noise_sigma', np.full(n_data, noise_sigma))
    np.save(data_path + 'theta', theta)
    np.save(data_path + 'phi', phi)

    # These are saved for convenience & reproducability
    np.save(data_path + 'extragal_sigma', extragal_sigma.val)
    np.save(data_path + 'noise', noise.val)
    np.save(data_path + 'extragal_rm', extragal_rm.val)
    np.save(data_path + 'gal_rm', gal_rm.val)
    np.save(data_path + 'rm_sky', true_rm.val)


if __name__ == '__main__':
    paramfile_name = str(sys.argv[1])

    pm = importlib.import_module('.' + paramfile_name, 'Parameters')
    general_parameter_dict = getattr(pm, 'data_params')
    domain_dict = getattr(pm, 'domain_params')
    egal_dict = getattr(pm, 'extragal_params')
    main(**general_parameter_dict, domain_parameters=domain_dict,
         extragal_params=egal_dict, )
