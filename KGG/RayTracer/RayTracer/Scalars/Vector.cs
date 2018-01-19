using System;

namespace RayTracer.Scalars
{
	public class Vector
	{
		public double X;
		public double Y;
		public double Z;

		public Vector(double x, double y, double z) { X = x; Y = y; Z = z; }

		public static Vector FromCoords(double x, double y, double z) { return new Vector(x, y, z); }
        
		public static Vector operator *(double n, Vector v)
		{
			return FromCoords(v.X * n, v.Y * n, v.Z * n);
		}

		public static Vector operator -(Vector v1, Vector v2)
		{
			return FromCoords(v1.X - v2.X, v1.Y - v2.Y, v1.Z - v2.Z);
		}

		public static Vector operator +(Vector v1, Vector v2)
		{
			return FromCoords(v1.X + v2.X, v1.Y + v2.Y, v1.Z + v2.Z);
		}

		public static double Dot(Vector v1, Vector v2)
		{
			return v1.X * v2.X + v1.Y * v2.Y + v1.Z * v2.Z;
		}

		public static double Magnitude(Vector v) { return Math.Sqrt(Dot(v, v)); }

		public static Vector Normal(Vector v)
		{
			var mag = Magnitude(v);
			var div = Math.Abs(mag) < 1E-8 ? double.PositiveInfinity : 1 / mag;
			return div * v;
		}

		public static Vector Cross(Vector v1, Vector v2)
		{
			return FromCoords(
				v1.Y * v2.Z - v1.Z * v2.Y,
				v1.Z * v2.X - v1.X * v2.Z,
				v1.X * v2.Y - v1.Y * v2.X
				);
		}

		public static bool Equals(Vector v1, Vector v2)
		{
			return (v1.X == v2.X) && (v1.Y == v2.Y) && (v1.Z == v2.Z);
		} 
	}
}