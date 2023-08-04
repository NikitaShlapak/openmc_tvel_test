from math import pi

import openmc
import neutronics_material_maker as nmm

# Materials
fuel_mat = openmc.Material(name='mat1')
fuel_mat.add_element('U',1, enrichment=5)
fuel_mat.add_element('O', 2)
fuel_mat.set_density('g/cm3', 8.3)
fuel_mat.volume = pi*10**2*100
water_mat = nmm.Material.from_library(name='Water, Liquid').openmc_material
# cladding_mat = nmm.Material.from_library(name='Zircaloy-2').openmc_material

