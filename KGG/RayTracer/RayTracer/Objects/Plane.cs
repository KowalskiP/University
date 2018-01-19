using RayTracer.Elements;
using RayTracer.Scalars;

namespace RayTracer.Objects
{
	public class Plane : IObject
	{
		public Vector Norm;
		public double Offset;
		public Surface Surface { get; set; }

		public Intersection Intersect(Ray ray)
		{
			var denominator = Vector.Dot(Norm, ray.Direction);
			if (denominator > 0) return null;
			return new Intersection {
				Object = this,
				Ray = ray,
				Distance = (Vector.Dot(Norm, ray.Origin) + Offset) / (-denominator)};
		}

		public Vector Normal(Vector pos)
		{
			return Norm;
		}
	}
}