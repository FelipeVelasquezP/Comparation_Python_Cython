from __future__ import print_function
import time
import argparse
import heat as heatPy
import heatmap_Cy as heatCy
#from heat import init_fields, write_field, iterate as heatPy

# from heatmap_Cy import  init_fields, write_field, iterate

def main(input_file='bottle.dat', a=0.5, dx=0.1, dy=0.1, 
         timesteps=2000, image_interval=8000):

    # Initialise the temperature field
    field, field0 = heatPy.init_fields(input_file)

    #print("Heat equation solver")
    #print("Diffusion constant: {}".format(a))
    #print("Input file: {}".format(input_file))
    #print("Parameters")
    #print("----------")
    #print("  nx={} ny={} dx={} dy={}".format(field.shape[0], field.shape[1],dx, dy))
    #print("  time steps={}  image interval={}".format(timesteps,image_interval))

    # Plot/save initial field





    #Python
    heatPy.write_field(field, 0)
    # Iterate
    t0 = time.time()
    heatPy.iterate(field, field0, a, dx, dy, timesteps, image_interval)
    t1 = time.time()
    # Plot/save final field
    heatPy.write_field(field, timesteps)

    print("Simulation finished in Pyhton {0} s".format(t1-t0))

    #
    
    field, field0 = heatCy.init_fields(input_file)

    heatCy.write_field(field, 0)
    # Iterate
    t0 = time.time()
    heatCy.iterate(field, field0, a, dx, dy, timesteps, image_interval)
    t1 = time.time()
    # Plot/save final field
    heatCy.write_field(field, timesteps)

    print("Simulation finished in Cyhton {0} s".format(t1-t0))

if __name__ == '__main__':

    # Process command line arguments
    parser = argparse.ArgumentParser(description='Heat equation')
    parser.add_argument('-dx', type=float, default=0.01,
                        help='grid spacing in x-direction')
    parser.add_argument('-dy', type=float, default=0.01,
                        help='grid spacing in y-direction')
    parser.add_argument('-a', type=float, default=0.5,
                        help='diffusion constant')
    parser.add_argument('-n', type=int, default=200,
                        help='number of time steps')
                        
    parser.add_argument('-i', type=int, default=4000,
                        help='image interval')
    parser.add_argument('-f', type=str, default='bottle.dat', 
                        help='input file')

    args = parser.parse_args()


    main(args.f, args.a, args.dx, args.dy, args.n, args.i)

