using System.Collections.Generic;
using System.Linq;
using RayTracer.Elements;

namespace RayTracer.Objects
{
	public class Environment
	{
		public IObject[] Objects;
		public Light[] Lights;
		public Camera Camera;

		public IEnumerable<Intersection> Intersect(Ray r) {
			return from obj in Objects select obj.Intersect(r);
		}
	}
}