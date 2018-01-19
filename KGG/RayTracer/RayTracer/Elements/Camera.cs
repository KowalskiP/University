using RayTracer.Scalars;

namespace RayTracer.Elements
{
	public struct Camera {
		public Vector Position;
		public Vector Direction;
		public Vector Upward;
		public Vector Rightward;

		private static readonly Vector Downward = Vector.FromCoords(0, -1, 0);

		private Camera(Vector position, Vector direction, Vector upward, Vector rightward)
		{
			Position = position;
			Direction = direction;
			Upward = upward;
			Rightward = rightward;
		}

		public static Camera CreateCamera(Vector position, Vector target)
		{
			var direction = Vector.Normal(target - position);
			var rightward = 1.5 * Vector.Normal(Vector.Cross(direction, Downward));
			var upward = 1.5 * Vector.Normal(Vector.Cross(direction, rightward));
			return new Camera(position, direction, upward, rightward);
		}
	}
}