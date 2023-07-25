import openmc

DAGMC_universe = openmc.DAGMCUniverse(filename='TVEL.h5m')
cell=openmc.Cell()
cell.fill=DAGMC_universe
universe = openmc.Universe(cells=[cell])