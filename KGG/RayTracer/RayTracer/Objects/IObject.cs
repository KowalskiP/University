using RayTracer.Elements;
using RayTracer.Scalars;

namespace RayTracer.Objects
{
	public interface IObject
	{
		Surface Surface { get; set; }
		Intersection Intersect(Ray ray);
		Vector Normal(Vector pos);
	}
}