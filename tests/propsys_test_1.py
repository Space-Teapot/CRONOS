from propulsion.propsys import Engine, Tank

tank1 = Tank(dimensions=(2.0, 0.25), shell_density=2700, propellant="N2O", prop_mass=10, prop_temp=100)
print("Tank 1 pressure:", round(tank1.get_pressure(), 0), "Pa")

tank2 = Tank(dimensions=(2.0, 0.25), shell_density=2700, propellant="ethanol", prop_mass=10, prop_temp=100)
print("Tank 2 pressure:", round(tank2.get_pressure(), 0), "Pa")

engine1 = Engine(dimensions=(1.0, 0.5), dry_density=2700, At=1e-4, Ae=1e-3, Tc=3000, gamma=1.4, R=287)
thrust, isp = engine1.get_thrust_isp(Pc=tank1.get_pressure(), Pa=1e5)
print("Engine 1 thrust:", round(thrust, 0), "N")
print("Engine 1 specific impulse:", round(isp, 2), "s")