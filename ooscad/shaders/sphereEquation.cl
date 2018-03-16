__constant double max_r = {};
__constant double min_r = {};

__constant double phi_start = {};
__constant double phi_end = {};
__constant double phi_inc = {};

__constant double theta_start = {};
__constant double theta_end = {};
__constant double theta_inc = {};

double getRadius(double phi, double theta){{
    return {};
}}

double4 get_coordinates(float phi, float theta){{
    double r = getRadius(phi, theta);

    double x = r*sin(phi)*cos(theta);
    double y = r*sin(phi)*sin(theta);
    double z = r*cos(phi);

    return (double4)(x,y,z, 0.0);
}}

__kernel void sphere_points(
    __global double* coordinate_array,
    __global long* vtk_vert_array
){{
    long pos = get_global_id(0);

    double phi = fmod(phi_start + (pos)*phi_inc, phi_end);
    double theta = fmod(theta_start + (pos)*theta_inc, theta_end);

    double4 xyzn = get_coordinates(phi, theta);

    coordinate_array[pos*3  ] = xyzn.x;
    coordinate_array[pos*3+1] = xyzn.y;
    coordinate_array[pos*3+2] = xyzn.z;

    vtk_vert_array[pos*2]=1;
    vtk_vert_array[pos*2+1]=pos;
}}