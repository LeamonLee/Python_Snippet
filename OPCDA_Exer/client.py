import OpenOPC

opc = OpenOPC.client()
# opc = OpenOPC.open_client('localhost')

lstServers = opc.servers()
print("lstServers : ",lstServers)

opc.connect('Matrikon.OPC.Simulation.1', 'localhost')

opc.read('Random.Time')