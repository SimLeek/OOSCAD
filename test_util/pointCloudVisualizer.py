import vtk
from vtk.util import numpy_support

#todo: create 3d testing library for point clouds
class MockModel(object):
    def __init__(self):
        self.points = vtk.vtkPoints()
        self.vertices = vtk.vtkCellArray()

    def batch_points(self, array_in):
        vtk_point_data = numpy_support.numpy_to_vtk(array_in, deep=True, array_type=vtk.VTK_FLOAT)
        #self.points.DeepCopy(vtk_point_data)
        self.points.SetData(vtk_point_data)

    def batch_vertices(self, array_in):
        vtk_vertex_data = numpy_support.numpy_to_vtkIdTypeArray(array_in, deep=True)
        #self.vertices.SetNumberOfCells(int(len(vtk_vertex_data)/2))
        #self.vertices.UpdateCellCount(int(len(array_in)/2))
        #self.vertices.DeepCopy(vtk_vertex_data)
        self.vertices.SetCells(int(len(array_in)/2),vtk_vertex_data)

    def show_cloud(self):
        cloud = vtk.vtkPolyData()

        cloud.SetPoints(self.points)
        cloud.SetVerts(self.vertices)

        # Visualize
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(cloud)
        else:
            mapper.SetInputData(cloud)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetPointSize(2)

        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(actor)

        renderWindow.Render()
        renderWindowInteractor.Start()