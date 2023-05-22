import openmc

openmc.config['cross_sections'] = '/home/main/cross_section_libs/jeff32/jeff-3.3-hdf5/cross_sections.xml'

import matplotlib.pyplot as plt
import neutronics_material_maker as nmm

#Materials
fuel_mat = nmm.Material.from_library(name='Uranium Oxide').openmc_material
water_mat = nmm.Material.from_library(name='Water, Liquid').openmc_material
cladding_mat = nmm.Material.from_library(name='Zircaloy-2').openmc_material
materials = openmc.Materials([fuel_mat,water_mat,cladding_mat])

cladding_surf = openmc.ZCylinder(r=10)
fuel_surf = openmc.ZCylinder(r=9)
water_surf = openmc.ZCylinder(r=20)
top_surf = openmc.ZPlane(z0=3500/2)
bottom_surf = openmc.ZPlane(z0=-3500/2)

top_surf.boundary_type='vacuum'
bottom_surf.boundary_type='vacuum'
water_surf.boundary_type='vacuum'

#Geometry
fuel_cell = openmc.Cell(fill=fuel_mat, region=-fuel_surf&+bottom_surf&-top_surf)
cladding_cell = openmc.Cell(fill=cladding_mat, region=+fuel_surf & -cladding_surf&+bottom_surf&-top_surf)
water_cell = openmc.Cell(fill=fuel_mat, region=+cladding_surf & -water_surf& +bottom_surf&-top_surf)
outside_cell = openmc.Cell(region=+water_surf&+top_surf&-bottom_surf)

universe = openmc.Universe(cells=[fuel_cell, cladding_cell, water_cell, outside_cell])
fig, ax = plt.subplots(2,2)

universe.plot(width=(50, 50),pixels=(250,250),basis='xz', origin=(0,0,3500/2-10), axes=ax[0][0])
universe.plot(width=(50, 50),pixels=(250,250),basis='xz', origin=(0,0,0), axes=ax[1][1])
universe.plot(width=(50, 50),pixels=(250,250),basis='xz', origin=(0,0,-3500/2+10), axes=ax[0][1])
universe.plot(width=(100, 100),pixels=(500,500),basis='xy', origin=(0,0,0), axes=ax[1][0])
plt.savefig('plots/geometry.jpg')

geometry = openmc.Geometry(universe)

#Settings
setting = openmc.Settings()
setting.batches = 100
setting.inactive = 10
setting.particles = 1000

uniform_dist = openmc.stats.Box([-10,-10,-3500/2],[10,10,3500/2], only_fissionable=True)
setting.source = openmc.source.Source(space=uniform_dist)

#XML export
materials.export_to_xml('xmls/materials.xml')
geometry.export_to_xml('xmls/geometry.xml')
setting.export_to_xml('xmls/setting.xml')

#RUN
openmc.run()
