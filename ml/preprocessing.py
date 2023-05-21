import re


# read species
f = open("species.txt", "r")
species = f.readlines()
species = [x.replace("\n", "") for x in species]
print(f"Species amount: {len(species)}")

# read file
f = open("input.txt", "r")
atlas_raw = ''.join(f.readlines())

split_index = []
for specie in species:
    occasions = [m.start() for m in re.finditer(specie, atlas_raw)]
    split_index.append(occasions[0])
print(f"Will split by {len(split_index)}")
