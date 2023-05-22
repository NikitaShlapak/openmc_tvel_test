import openmc

openmc.config['cross_sections'] = '/home/main/cross_section_libs/jeff32/jeff-3.3-hdf5/cross_sections.xml'

import matplotlib.pyplot as plt
import neutronics_material_maker as nmm

# Materials
fuel_mat = nmm.Material.from_library(name='Uranium Oxide').openmc_material
water_mat = nmm.Material.from_library(name='Water, Liquid').openmc_material
cladding_mat = nmm.Material.from_library(name='Zircaloy-2').openmc_material
materials = openmc.Materials([fuel_mat, water_mat, cladding_mat])

cladding_surf = openmc.ZCylinder(r=10)
fuel_surf = openmc.ZCylinder(r=9)
water_surf = openmc.hexagonal_prism(orientation='y', edge_length=15)

top_surf = openmc.ZPlane(z0=3500 / 2)
bottom_surf = openmc.ZPlane(z0=-3500 / 2)

top_surf.boundary_type = 'vacuum'
bottom_surf.boundary_type = 'vacuum'
water_surf.boundary_type = 'transmission'

# Geometry
fuel_cell = openmc.Cell(fill=fuel_mat, region=-fuel_surf & +bottom_surf & -top_surf)
cladding_cell = openmc.Cell(fill=cladding_mat, region=+fuel_surf & -cladding_surf & +bottom_surf & -top_surf)
water_cell = openmc.Cell(fill=water_mat, region=+cladding_surf & water_surf & +bottom_surf & -top_surf)
outside_cell = openmc.Cell(region=water_surf & +top_surf & -bottom_surf)

universe = openmc.Universe(cells=[fuel_cell, cladding_cell, water_cell, outside_cell])
geometry = openmc.Geometry(universe)

# Plotting by universe...
colors = {water_mat: (120, 120, 255), cladding_mat: 'black', fuel_mat: 'green'}
color_data = dict(color_by='material', colors=colors)

fig, ax = plt.subplots(2, 2)

universe.plot(width=(50, 50), pixels=(250, 250), basis='xz', **color_data, origin=(0, 0, 3500 / 2 - 10), axes=ax[0][0])
universe.plot(width=(50, 50), pixels=(250, 250), basis='xz', **color_data, origin=(0, 0, 0), axes=ax[1][1])
universe.plot(width=(50, 50), pixels=(250, 250), basis='xz', **color_data, origin=(0, 0, -3500 / 2 + 10), axes=ax[0][1])
universe.plot(width=(50, 50), pixels=(250, 250), basis='xy', **color_data, origin=(0, 0, 0), axes=ax[1][0])
plt.savefig('plots/geometry.jpg')

# ...and by openmc.Plots
plots = [openmc.Plot(), openmc.Plot(), openmc.Plot(), openmc.Plot(), ]
for i in range(4):
    # plots[i].id=(i+1)*111
    plots[i].width = (50, 50)
    plots[i].pixels = (250, 250)
    plots[i].basis = 'xz'
    plots[i].color_by = 'material'
    plots[i].colors = colors
plots[0].origin = (0, 0, 3500 / 2 - 10)
plots[2].origin = (0, 0, -3500 / 2 - 10)
plots[-1].basis = 'xy'

plots = openmc.Plots(plots)
plots.export_to_xml(path='plots.xml')
openmc.plot_geometry()

# Settings
setting = openmc.Settings()
setting.batches = 100
setting.inactive = 10
setting.particles = 5000

uniform_dist = openmc.stats.Box([-10, -10, -3500 / 2], [10, 10, 3500 / 2], only_fissionable=True)
setting.source = openmc.source.Source(space=uniform_dist)

# XML export
materials.export_to_xml('xmls/materials.xml')
geometry.export_to_xml('xmls/geometry.xml')
setting.export_to_xml('xmls/setting.xml')

# RUN
openmc.run()
