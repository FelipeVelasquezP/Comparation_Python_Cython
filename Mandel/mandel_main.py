import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from compute_mandel import compute_mandel as compute_mandel_py
try:
    from compute_mandel_Cy import compute_mandel as compute_mandel_cyt
    # import compute_mandel_Cy
except ImportError:
    print("EX", ImportError)




def plot_mandel(mandel):
    plt.imshow(mandel)
    plt.axis('off')
    plt.show()

def main(version='py',steps=200):
    # kwargs = dict(cr = 0.285, ci = 0.01, n = steps, bound = 1.5)

    # choose pure Python or Cython version
    if version == 'py':
        #print("Using pure Python")
        mandel_func = compute_mandel_py
    elif version == 'cyt': 
        #print("Using Cython")
        try:
            mandel_func = compute_mandel_cyt
        except NameError as ex:
            raise RuntimeError("Cython extension missing") from ex
    else:
        raise RuntimeError("Unknown version")

    mandel_set, runtime = mandel_func(N = steps)
    return mandel_set, runtime

def make_csv(registers):
    writer = pd.ExcelWriter('archivo.xlsx')
    for register in registers:
        df=pd.DataFrame(data=register[1],columns=['Python','Cython'])
        df.to_excel(writer, sheet_name=f"N={register[0]}", index=False)
    writer.save()
    writer.close()

if __name__ == '__main__':
    registros=[]
    cargas=[200,400,800, 1000, 1200]
    for carga in cargas:
       print(carga)
       regCarga=[]
       for i in range(31):
           mandel_set, runtimeCy = main('cyt',carga)
           mandel_set, runtimePy = main(steps = carga)
           regCarga.append([runtimePy,runtimeCy])
       registros.append((carga,regCarga))
    make_csv(registros)

    
    

    # if len(sys.argv) == 2:
    #     mandel_set, runtime = main('cyt')
    # else:
    #     mandel_set, runtime = main()
    # print(runtime)
    # print('Mandelbrot set generated in {0:5.2f} seconds'.format(runtime))
    # # plot_mandel(mandel_set)
    

