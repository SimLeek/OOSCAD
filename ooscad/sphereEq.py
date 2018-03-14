import os
import numpy as np
import pyopencl as cl
import math as m

import pygp_util as pgpu
from .shader_util import shader_dir

if False:
    from typing import List, Any, Callable

def get_sphere_equation_program(
        sphere_equation="1.0",

        max_r="FLT_MAX",
        min_r="FLT_MIN",

        phi_start=-m.pi/2.0,
        phi_end=m.pi/2.0,
        phi_inc=m.pi/(2.0**12),

        theta_start=-m.pi/2.0,
        theta_end=m.pi/2.0,
        theta_inc=m.pi/(2.0**5),

        gpu=0
):  # type: (...)->pgpu.ShaderProgram
    cl_str = pgpu.format_read_file(shader_file=shader_dir+os.sep+'sphereEquation.cl',
                                   format_args=(max_r, min_r,
                                                phi_start, phi_end, phi_inc,
                                                theta_start, theta_end, theta_inc,
                                                sphere_equation))
    shady_program = pgpu.ShaderProgram(gpu)

    shady_program.build_program(cl_str, [])

    return shady_program



def get_sphere_coordinates(
        sphere_equation="1.0",

        max_r="FLT_MAX",
        min_r="FLT_MIN",

        phi_start=0,
        phi_end=m.pi,
        phi_inc=m.pi / (2.0 ** 11),

        theta_start=0,
        theta_end=2*m.pi,
        theta_inc=m.pi/(2.0**5),

        num_points = 65536,

        gpu=0
):  # type: (...)->Callable[List[Any], None]
    p=get_sphere_equation_program(
        sphere_equation=sphere_equation,
        max_r=max_r, min_r=min_r,
        phi_start=phi_start, phi_end=phi_end, phi_inc=phi_inc,
        theta_start=theta_start, theta_end=theta_end, theta_inc=theta_inc,
        gpu=0
    )

    coords_np = np.zeros((num_points*3,), dtype=np.float64)
    coords_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, coords_np.nbytes)

    vtk_v_np = np.zeros((num_points*2 ,), dtype=np.int64)
    vtk_v_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, vtk_v_np.nbytes)

    p.build.sphere_points(p.queue, (num_points,), (64,), coords_buf, vtk_v_buf)

    cl.enqueue_copy(p.queue, coords_np, coords_buf).wait()
    cl.enqueue_copy(p.queue, vtk_v_np, vtk_v_buf).wait()

    return coords_np.reshape((num_points,3)), vtk_v_np.astype(np.int64)