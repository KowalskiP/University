using System.Drawing;

namespace RayTracer.Scalars
{
	public class ColorRt
	{
		public double R;
		public double G;
		public double B;

		public static readonly ColorRt Background = FromRgb(0, 0, 0);
		public static readonly ColorRt Default = FromRgb(0, 0, 0);

		private ColorRt(double r, double g, double b) { R = r; G = g; B = b; }

		private static double Normalize(double component)
		{
			return component > 1 ? 1 : component;
		}

		public static ColorRt FromRgb(double r, double g, double b) { return new ColorRt(r, g, b); }

		public static ColorRt operator *(double n, ColorRt v)
		{
			return FromRgb(n * v.R, n * v.G, n * v.B);
		}

		public static ColorRt operator *(ColorRt v1, ColorRt v2)
		{
			return FromRgb(v1.R * v2.R, v1.G * v2.G, v1.B * v2.B);
		}

		public static ColorRt operator +(ColorRt v1, ColorRt v2)
		{
			return FromRgb(v1.R + v2.R, v1.G + v2.G, v1.B + v2.B);
		}

		public static ColorRt operator -(ColorRt v1, ColorRt v2)
		{
			return FromRgb(v1.R - v2.R, v1.G - v2.G, v1.B - v2.B);
		}

		internal Color Draw()
		{
			return Color.FromArgb((int)(Normalize(R) * 255), (int)(Normalize(G) * 255), (int)(Normalize(B) * 255));
		}
	}
}