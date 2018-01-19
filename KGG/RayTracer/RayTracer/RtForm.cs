using System;
using System.Drawing;
using System.Windows.Forms;

namespace RayTracer
{
	public class RtForm : Form
	{
		private readonly Bitmap Bitmap;
		private readonly PictureBox PictureBox;
		private const int width = 600;
		private const int height = 600;

		public RtForm()
		{
			Bitmap = new Bitmap(width,height);

			PictureBox = new PictureBox
			{
				Dock = DockStyle.Fill,
				SizeMode = PictureBoxSizeMode.StretchImage,
				Image = Bitmap
			};

			ClientSize = new Size(width, height + 24);
			Controls.Add(PictureBox);
			Text = "Ray Tracer";
			Load += RtFormPaintEvent;

			Show();
		}

		private void RtFormPaintEvent(object sender, EventArgs e)
		{
			Show();
			var rayTracer = new RayTracer(width, height, (x, y, color) =>
			{
				Bitmap.SetPixel(x, y, color);
				if (x == 0) PictureBox.Refresh();
			});
			rayTracer.DrawEnvironment(rayTracer.Environment);
			PictureBox.Invalidate();
		}

		[STAThread]
		private static void Main() {
			Application.EnableVisualStyles();
			Application.Run(new RtForm());
		}
	}
}