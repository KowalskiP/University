using System.Linq;
using System;
using System.Collections.Generic;
using System.Drawing;
using RayTracer.Elements;
using RayTracer.Objects;
using RayTracer.Scalars;
using Environment = RayTracer.Objects.Environment;

namespace RayTracer {
	public class RayTracer {

		private readonly int ScreenWidth;
		private readonly int ScreenHeight;
		private const int MaxDepth = 5;

		public Action<int, int, Color> SetPixel;

		public RayTracer(int screenWidth, int screenHeight, Action<int,int, Color> setPixel)
		{
			ScreenWidth = screenWidth;
			ScreenHeight = screenHeight;
			SetPixel = setPixel;
		}

		private double ShiftX(double x)
		{
			return (x - (ScreenWidth / 2.0)) / (2.0 * ScreenWidth);
		}

		private double ShiftY(double y)
		{
			return -(y - (ScreenHeight / 2.0)) / (2.0 * ScreenHeight);
		}

		private static IEnumerable<Intersection> Intersections(Ray ray, Environment environment)
		{
			return environment.Objects
				.Select(obj => obj.Intersect(ray))
				.Where(intersection => intersection != null)
				.OrderBy(intersection => intersection.Distance);
		}

		private static double TestRay(Ray ray, Environment environment)
		{
			var isects = Intersections(ray, environment);
			var isect = isects.FirstOrDefault();
            if (isect == null)
                return 0;
			return isect.Distance;
		}

		private ColorRt TraceRay(Ray ray, Environment environment, int depth)
		{
			var isects = Intersections(ray, environment);
			var isect = isects.FirstOrDefault();
			return isect == null ? ColorRt.Background : Shade(isect, environment, depth);
		}

		private static ColorRt NaturalColor(IObject obj, Vector position, Vector normal, Vector reflectDirection, Environment environment)
		{
			var tracedColor = ColorRt.FromRgb(0, 0, 0);
			foreach (var light in environment.Lights) {
				var lightVector = light.Position - position;
				var lightRay = Vector.Normal(lightVector);
				var distance = TestRay(new Ray { Origin = position, Direction = lightRay }, environment);
				var isInShadow = !((distance > Vector.Magnitude(lightVector)) || (Math.Abs(distance) < 1E-8));
				if (isInShadow) continue;

				var illumination = Vector.Dot(lightRay, normal);
				var lightColor = illumination > 0 ? illumination * light.ColorRt : ColorRt.FromRgb(0, 0, 0);

				var specular = Vector.Dot(lightRay, Vector.Normal(reflectDirection));
				var specularColor = specular > 0 ? Math.Pow(specular, obj.Surface.Roughness) * light.ColorRt : ColorRt.FromRgb(0, 0, 0);
                tracedColor += obj.Surface.Diffuse(position) * lightColor + obj.Surface.Specular(position) * specularColor;
			}
			return tracedColor;
		}

		private ColorRt ReflectionColor(IObject obj, Vector position, Vector reflectDirection, Environment environment, int depth)
		{
			return obj.Surface.
				Reflect(position) * TraceRay(new Ray { Origin = position, Direction = reflectDirection }, environment, depth + 1);
		}

		private ColorRt Shade(Intersection intersection, Environment environment, int depth)
		{
			var direction = intersection.Ray.Direction;
			var position = intersection.Distance * intersection.Ray.Direction + intersection.Ray.Origin;
			var normal = intersection.Object.Normal(position);
			if (Vector.Dot(normal, direction) > 0)
			{
				normal = -1* normal;
			}
            var reflectDirection = direction - 2 * Vector.Dot(normal, direction) * normal;
			var tracedColor = ColorRt.Default;
			tracedColor += NaturalColor(intersection.Object, position, normal, reflectDirection, environment);
			if (depth >= MaxDepth) {
                return tracedColor + ColorRt.FromRgb(.5, .5, .5);
			}
            return tracedColor + ReflectionColor(intersection.Object, position + .001 * reflectDirection, reflectDirection, environment, depth);
		}

		private Vector Point(double x, double y, Camera camera)
		{
			return Vector.Normal(camera.Direction + ShiftX(x) * camera.Rightward + ShiftY(y) * camera.Upward);
		}

		public void DrawEnvironment(Environment environment)
		{
			for (var y = 0; y < ScreenHeight; y++)
			{
				for (var x = 0; x < ScreenWidth; x++)
				{
					var tracedColor = TraceRay(new Ray { Origin = environment.Camera.Position, Direction = Point(x, y, environment.Camera) }, environment, 0);
					SetPixel(x, y, tracedColor.Draw());
				}
			}
		}

		public readonly Environment Environment = Presets.PresetOne;
	}

	public delegate void Action<in T, in TU, in TV>(T t, TU u, TV v);
}