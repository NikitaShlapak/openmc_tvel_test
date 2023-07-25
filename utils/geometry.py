from math import sqrt

import openmc
import numpy as np

from .material import fuel_mat, water_mat

# Surfaces
fuel_surf = openmc.ZCylinder(r=10)
water_surf = openmc.hexagonal_prism(edge_length=20, orientation='x', boundary_type='reflective')

top_surf = openmc.ZPlane(z0=100 / 2)
bottom_surf = openmc.ZPlane(z0=-100 / 2)


top_surf.boundary_type = 'vacuum'
bottom_surf.boundary_type = 'vacuum'


# 1. tvel in water
fuel_cell = openmc.Cell(fill=fuel_mat, region=-fuel_surf & +bottom_surf & -top_surf)
water_cell = openmc.Cell(fill=water_mat, region=+fuel_surf & water_surf & +bottom_surf & -top_surf)

universe = openmc.Universe(cells=[fuel_cell, water_cell])


# universe = openmc.Universe(cells=[sub_universe])

#full_lat_cell = openmc.Cell()
# for i in range(6):
#  print(f"i = {i} - {universe.find((i*3,0,0))}\n\n")