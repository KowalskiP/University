using System;
using RayTracer.Elements;
using RayTracer.Scalars;

namespace RayTracer.Objects
{
	public class Triangle : IObject
	{
		public Vector v0;
		public Vector v1;
		public Vector v2;

		public Surface Surface { get; set; }

		public Intersection Intersect(Ray ray)
		{
			var e1 = v1 - v0;
			var e2 = v2 - v0;
 
			var p = Vector.Cross(ray.Direction, e2);

			var det = Vector.Dot(e1, p);

			if (det > -1E-08 && det < 1E-08) { return null; }
			var invDet = 1.0f / det;

			var t = ray.Origin - v0;

			var u = Vector.Dot(t, p) * invDet;

			if (u < 0 || u > 1) { return null; }

			var q = Vector.Cross(t, e1);

			var v = Vector.Dot(ray.Direction, q) * invDet;

			if (v < 0 || u + v > 1) { return null; }

			if ((Vector.Dot(e2, q) * invDet) > 1E-08)
			{
				return new Intersection
				{
					Object = this,
					Ray = ray,
                    Distance = Vector.Dot(e2, q) * invDet
				};
			}

			return null;
		}

		public Vector Normal(Vector pos)
		{
			var normal = Vector.Cross(v1 - v0, v2 - v0);
			//return Vector.Dot(normal, pos) > 0 ? normal : -1*normal;
			return normal;
		}
	}
}