# Network Documentation

## player controlled networks

`10.4x.<team_number>.y/24`

x=0 -> team VM
x=1 -> openvpn network for teams
x=2 -> wireguard network for teams, y in [1..5] (team members)

## gameserver networks

`10.3x.1.y/24`

x=8 -> gameserver attack/defense
x=9 -> jeopardy (hosted socket applications)


## jeopardy network

10.