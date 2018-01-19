using System;
using RayTracer.Scalars;

namespace RayTracer.Elements
{
	public struct Surface
	{
		public Func<Vector, ColorRt> Diffuse;
		public Func<Vector, ColorRt> Specular;
		public Func<Vector, double> Reflect;
		public double Roughness;
	}
}