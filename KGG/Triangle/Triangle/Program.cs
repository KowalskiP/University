using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Triangle
{
	static class Program
	{
		[STAThread]
		static void Main()
		{
			var polygon = new List<PointF>();
			using (var sr = new StreamReader("input4.txt"))
			{
				while (!sr.EndOfStream)
				{
					var readLine = sr.ReadLine();
					if (readLine == null) continue;
					var line = readLine.Split(' ');
					polygon.Add(new PointF(float.Parse(line[0]) + 400,float.Parse(line[1])+300));
				}
			}
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			var triangle = new Triangle(polygon)
			{
				Text = "Triangle",
				Size = new Size(800, 600),
				StartPosition = FormStartPosition.CenterScreen
			};

			var widthRatio = (Screen.PrimaryScreen.Bounds.Width / 1920f);
			var heighRatio = (Screen.PrimaryScreen.Bounds.Height / 1080f);

			var scale = new SizeF(widthRatio, heighRatio);

			triangle.Scale(scale);

			foreach (Control control in triangle.Controls)
			{
				control.Font = new Font("Microsoft Sans Serif", control.Font.SizeInPoints * heighRatio * widthRatio);
			}

			Application.Run(triangle);
		}
	}

	internal class Triangle : Form
	{
		private readonly List<PointF> Polygon; 
		public Triangle(List<PointF> polygon)
		{
			Polygon = polygon;
			InitGraph();
		}

		private void InitGraph()
		{
			Paint += PaintEvent;
		}

		private void PaintEvent(object sender, PaintEventArgs e)
		{
			var clr = Color.Violet;
			var pnBorder = new Pen(clr);
			e.Graphics.DrawPolygon(pnBorder, Polygon.ToArray());

			var copyiedPolygon = new List<PointF>(Polygon.Count);
			Polygon.ForEach((item) => { copyiedPolygon.Add(new PointF(item.X, item.Y)); });
			var i = 0;
			while (copyiedPolygon.Count != 3)
			{
				var intersect = false;
				var p = copyiedPolygon.ToArray();
				int left;
				int right;
				if (i - 1 < 0)
					left = p.Length - 1;
				else left = i - 1;
				if (i + 1 > p.Length - 1)
					right = 0;
				else right = i + 1;
				for (var j = 0; j < p.Length - 1; j++)
				{
					if (Intersection(copyiedPolygon[left], copyiedPolygon[right], p[j], p[j + 1]))
						intersect = true;
				}
				var inside = false;
				if (!intersect)
				{

					var middle = new PointF((copyiedPolygon[left].X + copyiedPolygon[right].X)/2,
						(copyiedPolygon[left].Y + copyiedPolygon[right].Y)/2);
					inside = IsPointInside(copyiedPolygon, middle);
					if (inside)
					{
						e.Graphics.DrawLine(pnBorder, copyiedPolygon[left], copyiedPolygon[right]);
						copyiedPolygon.Remove(copyiedPolygon[i]);
					}
				}
				if (intersect || !inside) i++;
				if (i > copyiedPolygon.Count) break;
			}
		}

		private static bool Intersection(PointF start1, PointF end1, PointF start2, PointF end2)
		{
			var dir1 = new PointF(end1.X - start1.X, end1.Y - start1.Y);
			var dir2 = new PointF(end2.X - start2.X, end2.Y - start2.Y);

			//считаем уравнения прямых проходящих через отрезки
			var a1 = -dir1.Y;
			var b1 = +dir1.X;
			var d1 = -(a1 * start1.X + b1 * start1.Y);

			var a2 = -dir2.Y;
			var b2 = +dir2.X;
			var d2 = -(a2 * start2.X + b2 * start2.Y);

			//подставляем концы отрезков, для выяснения в каких полуплоскотях они
			var seg1Line2Start = a2 * start1.X + b2 * start1.Y + d2;
			var seg1Line2End = a2 * end1.X + b2 * end1.Y + d2;

			var seg2Line1Start = a1 * start2.X + b1 * start2.Y + d1;
			var seg2Line1End = a1 * end2.X + b1 * end2.Y + d1;

			//если концы одного отрезка имеют один знак, значит он в одной полуплоскости и пересечения нет.
			if (seg1Line2Start * seg1Line2End >= 0 || seg2Line1Start * seg2Line1End >= 0)
				return false;
			return true;
		}

		private static bool IsPointInside(IReadOnlyList<PointF> polygon, PointF point)
		{

			if (polygon.Count <= 1)
				return false;

			var intersectionsNum = 0;
			var prev = polygon.Count - 1;
			var prevUnder = polygon[prev].Y < point.Y;

			for (var i = 0; i < polygon.Count; ++i)
			{
				var curUnder = polygon[i].Y < point.Y;

				var a = new PointF(polygon[prev].X - point.X, polygon[prev].Y - point.Y);
				var b = new PointF(polygon[i].X - point.X, polygon[i].Y - point.Y);

				var t = (a.X*(b.Y - a.Y) - a.Y*(b.X - a.X));
				if (curUnder && !prevUnder)
				{
					if (t > 0)
						intersectionsNum += 1;
				}
				if (!curUnder && prevUnder)
				{
					if (t < 0)
						intersectionsNum += 1;
				}

				prev = i;
				prevUnder = curUnder;
			}

			return (intersectionsNum & 1) != 0;
		}
	}
}
