using RayTracer.Elements;
using RayTracer.Scalars;

namespace RayTracer.Objects
{
	public struct Presets
	{
		public static readonly Environment PresetOne = new Environment
		{
			Objects = new IObject[] {
					new Plane {
						Norm = Vector.FromCoords(0,1,0),
						Offset = 0,
						Surface = Surfaces.ChessBoard
					},
					new Triangle
					{
						v0 = Vector.FromCoords(0,1,-1),
						v1 = Vector.FromCoords(-0.5,0,-2),
						v2 = Vector.FromCoords(-0.5,0,0),
						Surface = Surfaces.Blue
					},
					new Triangle
					{
						v0 = Vector.FromCoords(0,1,-1),
						v1 = Vector.FromCoords(1,0,-1),
						v2 = Vector.FromCoords(-0.5,0,-2),
						Surface = Surfaces.Red
					},
					new Triangle
					{
						v0 = Vector.FromCoords(0,1,-1),
						v1 = Vector.FromCoords(-0.5,0,0),
						v2 = Vector.FromCoords(1,0,-1),
						Surface = Surfaces.Green
					},
					new Triangle
					{
						v0 = Vector.FromCoords(-0.5,0,-2),
						v1 = Vector.FromCoords(-0.5,0,0),
						v2 = Vector.FromCoords(1,0,-1),
						Surface = Surfaces.Yellow
					},

					new Triangle
					{
						v0 = Vector.FromCoords(2,1,1),
						v1 = Vector.FromCoords(1.5,0,0),
						v2 = Vector.FromCoords(1.5,0,2),
						Surface = Surfaces.Blue
					},
					new Triangle
					{
						v0 = Vector.FromCoords(2,1,1),
						v1 = Vector.FromCoords(3,0,1),
						v2 = Vector.FromCoords(1.5,0,0),
						Surface = Surfaces.Red
					},
					new Triangle
					{
						v0 = Vector.FromCoords(2,1,1),
						v1 = Vector.FromCoords(1.5,0,2),
						v2 = Vector.FromCoords(3,0,1),
						Surface = Surfaces.Green
					},
					new Triangle
					{
						v0 = Vector.FromCoords(1.5,0,0),
						v1 = Vector.FromCoords(1.5,0,2),
						v2 = Vector.FromCoords(3,0,1),
						Surface = Surfaces.Yellow
					},

			},
			Lights = new[] {
					new Light {
						Position = Vector.FromCoords(-2,2.5,0),
						ColorRt = ColorRt.FromRgb(.49,.07,.07)
					},
					new Light {
						Position = Vector.FromCoords(1.5,2.5,1.5),
						ColorRt = ColorRt.FromRgb(.07,.07,.49)
					},
					new Light {
						Position = Vector.FromCoords(1.5,2.5,-1.5),
						ColorRt = ColorRt.FromRgb(.07,.49,.071)
					},
					new Light {
						Position = Vector.FromCoords(0,3.5,-3),
						ColorRt = ColorRt.FromRgb(.21,.21,.35)
					}},
			Camera = Camera.CreateCamera(Vector.FromCoords(10, 2, 0), Vector.FromCoords(0, 0, 0))
		};	
	}
}