import openmc
import numpy as np

from .material import fuel_mat, cladding_mat, water_mat

# Surfaces
fuel_surf = openmc.ZCylinder(r=9)
cladding_surf = openmc.ZCylinder(r=10)
water_surf = openmc.rectangular_prism(width=25, height=25, boundary_type='vacuum')

top_surf = openmc.ZPlane(z0=3500 / 2)
bottom_surf = openmc.ZPlane(z0=-3500 / 2)

lat_surf = openmc.rectangular_prism(width=75, height=75, boundary_type='vacuum')

top_surf.boundary_type = 'vacuum'
bottom_surf.boundary_type = 'vacuum'

# Geometry
# 1. tvel in water
fuel_cell = openmc.Cell(fill=fuel_mat, region=-fuel_surf & +bottom_surf & -top_surf)
cladding_cell = openmc.Cell(fill=cladding_mat, region=+fuel_surf & -cladding_surf & +bottom_surf & -top_surf)
water_cell = openmc.Cell(fill=water_mat, region=+cladding_surf & water_surf & +bottom_surf & -top_surf)

sub_universe = openmc.Universe(cells=[fuel_cell, cladding_cell, water_cell])

# 2. lattice

lat = openmc.RectLattice()
lat.lower_left = (-25 * 3 / 2, -25 * 3 / 2)
lat.pitch = (25, 25)
lat.universes = np.tile(sub_universe, (3, 3))

lat_cell = openmc.Cell(region=lat_surf, fill=lat)
outside_cell = openmc.Cell(region=lat_surf & +top_surf & -bottom_surf)
universe = openmc.Universe(cells=[lat_cell, outside_cell])
# for i in range(6):
#  print(f"i = {i} - {universe.find((i*3,0,0))}\n\n")