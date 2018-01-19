using System;
using RayTracer.Elements;
using RayTracer.Scalars;

namespace RayTracer.Objects
{
	public struct Surfaces
	{
		public static readonly Surface ChessBoard  = 
			new Surface
			{
				Diffuse = pos => (Math.Abs((Math.Floor(pos.Z) + Math.Floor(pos.X)) % 2) > 1E-8) ? ColorRt.FromRgb(1,1,1) : ColorRt.FromRgb(0,0,0),
				Specular = pos => ColorRt.FromRgb(1,1,1),
				Reflect = pos => (Math.Abs((Math.Floor(pos.Z) + Math.Floor(pos.X)) % 2) > 1E-8) ? .1 : .7,
				Roughness = 150
			};

		public static readonly Surface Red = 
			new Surface() {
				Diffuse = pos => ColorRt.FromRgb(1,0,0),
				Specular = pos => ColorRt.FromRgb(.5,.5,.5),
				Reflect = pos => .2,
				Roughness = 150
			};

		public static readonly Surface Green =
			new Surface()
			{
				Diffuse = pos => ColorRt.FromRgb(0, 1, 0),
				Specular = pos => ColorRt.FromRgb(.5, .5, .5),
				Reflect = pos => .2,
				Roughness = 150
			};

		public static readonly Surface Blue =
			new Surface()
			{
				Diffuse = pos => ColorRt.FromRgb(0, 0, 1),
				Specular = pos => ColorRt.FromRgb(.5, .5, .5),
				Reflect = pos => .2,
				Roughness = 150
			};

		public static readonly Surface Yellow =
			new Surface()
			{
				Diffuse = pos => ColorRt.FromRgb(1, 1, 0),
				Specular = pos => ColorRt.FromRgb(.5, .5, .5),
				Reflect = pos => .2,
				Roughness = 150
			};
	}
}