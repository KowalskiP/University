using System;
using RayTracer.Elements;
using RayTracer.Scalars;

namespace RayTracer.Objects
{
	public class Sphere : IObject
	{
		public Vector Center;
		public double Radius;
	    public Surface Surface { get; set; }

		public Intersection Intersect(Ray ray)
		{
			var eo = Center - ray.Origin;
			var v = Vector.Dot(eo, ray.Direction);
			double dist;
			if (v < 0) {
				dist = 0;
			}
			else {
				var disc = Math.Pow(Radius,2) - (Vector.Dot(eo, eo) - Math.Pow(v,2));
				dist = disc < 0 ? 0 : v - Math.Sqrt(disc);
			}
			if (Math.Abs(dist) < 1E-8) return null;
			return new Intersection() {
				Object = this,
				Ray = ray,
				Distance = dist};
		}

		public Vector Normal(Vector pos)
		{
			return Vector.Normal(pos - Center);
		}
	}
}