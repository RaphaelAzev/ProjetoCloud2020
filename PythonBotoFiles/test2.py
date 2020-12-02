Lista_subnets = ['1', '2', '3']

VPCzone = Lista_subnets[0]

for x in Lista_subnets[1:]:
    VPCzone += f',{x}'

print(VPCzone)