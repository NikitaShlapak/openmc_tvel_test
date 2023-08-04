import openmc
from openmc import deplete, stats

from utils.geometry import universe
# from utils.DAGMC_geometry import universe
from utils.material import water_mat,  fuel_mat

openmc.config['cross_sections'] = '/media/main/data/neutron_libs/jeff-3.3-hdf5/cross_sections.xml'
openmc.config['chain_file'] = '/media/main/data/neutron_libs/chains/chain_endfb71_pwr.xml'

import matplotlib.pyplot as plt
import neutronics_material_maker as nmm

if __name__ == "__main__":
    # Materials
    materials = openmc.Materials([fuel_mat, water_mat, ])

    # Geometry
    geometry = openmc.Geometry(universe)

    # Plotting by universe...
    colors = {water_mat: (120, 120, 255),  fuel_mat: 'green'}
    color_data = dict(color_by='material', colors=colors)
    width = (120,120)

    fig, ax = plt.subplots(2, 2)

    # universe.plot(width=width, pixels=(250, 250), basis='xz', **color_data, origin=(0, 0, 3500 / 2 - 10), axes=ax[0][0])
    universe.plot(width=width, pixels=(250, 250), basis='xz', **color_data, origin=(0, 0, 0), axes=ax[1][1])
    # universe.plot(width=width, pixels=(250, 250), basis='xz', **color_data, origin=(0, 0, -3500 / 2 + 10), axes=ax[0][1])
    universe.plot(width=width, pixels=(250, 250), basis='xy', **color_data, origin=(0, 0, 0), axes=ax[1][0])
    plt.savefig('plots/geometry.jpg')

    # ...and by openmc.Plots
    plots = [openmc.Plot(), openmc.Plot(), openmc.Plot(), openmc.Plot(), ]
    for i in range(4):
        # plots[i].id=(i+1)*111
        plots[i].width = width
        plots[i].pixels = (500, 500)
        plots[i].basis = 'xz'
        plots[i].color_by = 'material'
        plots[i].colors = colors
    plots[0].origin = (0, 0, 3500 / 2 -10)
    plots[2].origin = (0, 0, -3500/2+10)
    plots[-1].basis = 'xy'


    plots = openmc.Plots(plots)


    # Settings
    setting = openmc.Settings()
    setting.batches = 100
    setting.inactive = 10
    setting.particles = 5000

    uniform_dist = openmc.stats.Box([-10, -10, -3500 / 2], [10, 10, 3500 / 2], only_fissionable=True)
    setting.source = openmc.source.Source(space=uniform_dist)
    setting.run_mode = 'fixed source'
    # Tallies
    flux_tally = openmc.Tally(name='flux')
    flux_tally.scores = ['flux']

    U_tally = openmc.Tally(name='fuel')
    U_tally.scores = ['fission', 'total', 'absorption', 'elastic', 'scatter', 'decay-rate']
    U_tally.nuclides = ['U235', 'U238']

    tallies = openmc.Tallies([U_tally, flux_tally])
    # tally.filters = [cell_filter,energy_filter]


    # XML export
    materials.export_to_xml('xmls/materials.xml')
    geometry.export_to_xml('xmls/geometry.xml')
    setting.export_to_xml('xmls/settings.xml')
    tallies.export_to_xml('xmls/tallies.xml')
    plots.export_to_xml('xmls/plots.xml')
    print("xml export finished")

    # RUN
    model = openmc.Model(geometry=geometry, materials=materials, tallies=tallies, plots=plots, settings=setting)
    openmc.plot_geometry(path_input='xmls/')
    # openmc.run(output=False,path_input='xmls/')
    # Deplition
    operator = deplete.CoupledOperator(model=model)
    power = 1e6
    time_steps = [1]
    integrator = deplete.PredictorIntegrator(operator, time_steps, power, timestep_units='s')
    integrator.integrate()

    # with openmc.StatePoint('statepoint.100.h5') as sp:
    #     print(sp.keff)
    #     output_tally = sp.get_tally()
    #     df = output_tally.get_pandas_dataframe()
    #     df.to_csv('out.txt')
    #     print(df)

