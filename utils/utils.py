import neutronics_material_maker as nmm

def search_in_library(mat:str):
    mats = list(nmm.material_dict.keys())
    for mat in mats:
        if 'zir' in mat.lower():
            print(mat)