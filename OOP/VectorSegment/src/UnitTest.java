/**
 * Created by Антон on 17.10.2014.
 */
import org.junit.Test;
import static org.junit.Assert.*;

public class UnitTest {
    @Test
    public void length() {
        nSegment a = new nSegment(new Vector2D(0, 0), new Vector2D(2, 2));
        nSegment b = new nSegment(new Vector3D(-3, 3, 123), new Vector3D(100, 23, 1233));
        assertEquals(a.len(), Math.sqrt(2 * 2 + 2 * 2), 1e-9);
        assertEquals(b.len(), Math.sqrt(103 * 103 + 20 * 20 + 1110 * 1110), 1e-9);
    }

    @Test
    public void distance()
    {
        nSegment a = new nSegment(new Vector2D(0, 0), new Vector2D(2, 2));
        Vector2D pnt_2d = new Vector2D(0, 2);
        assertEquals(a.distanceTo(pnt_2d), Math.sqrt(2), 1e-9);

        nSegment b = new nSegment(new Vector3D(0, 0, 0), new Vector3D(0, 3, 3));
        Vector3D pnt_3d = new Vector3D(0, 1, 1);
        assertEquals(b.distanceTo(pnt_3d), Math.sqrt(2), 1e-9);
    }
}
