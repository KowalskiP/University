/**
 * Created by Антон on 17.10.2014.
 */
import org.junit.Test;
import static org.junit.Assert.*;

public class UTest {
    @Test
    public void leng() {
        Vector2D a = new Vector2D(2, 2);
        assertEquals(a.len(), Math.sqrt(8), 1e-9);
        Vector3D b = new Vector3D(2, 2, 2);
        assertEquals(b.len(), Math.sqrt(12), 1e-9);
    }

    @org.junit.Test
    public void add() {
        Vector2D a = new Vector2D(1, 1);
        Vector2D b = new Vector2D(2, 2);
        Vector2D c = new Vector2D(3, 3);
        assertEquals(a.add(b).len(), c.len(), 1e-9);
        Vector3D x = new Vector3D(1, 1, 1);
        Vector3D y = new Vector3D(2, 2, 2);
        Vector3D z = new Vector3D(3, 3, 3);
        assertEquals(x.add(y).len(), z.len(), 1e-9);
    }

    @org.junit.Test
    public void sub() {
        Vector2D a = new Vector2D(1, 1);
        Vector2D b = new Vector2D(2, 2);
        Vector2D c = new Vector2D(3, 3);
        assertEquals(c.sub(b).len(), a.len(), 1e-9);
        Vector3D x = new Vector3D(1, 1, 1);
        Vector3D y = new Vector3D(2, 2, 2);
        Vector3D z = new Vector3D(3, 3, 3);
        assertEquals(z.sub(y).len(), x.len(), 1e-9);
    }

    @Test
    public void mult() {
        Vector2D a = new Vector2D(2, 2);
        Vector2D b = new Vector2D(1, 1);
        assertEquals(a.multiply(0.5).len(), b.len(), 1e-9);
        Vector3D c = new Vector3D(2, 2, 2);
        Vector3D d = new Vector3D(1, 1, 1);
        assertEquals(c.multiply(0.5).len(), d.len(), 1e-9);
    }

    @Test
    public void scal() {
        Vector2D a = new Vector2D(2, 2);
        Vector2D b = new Vector2D(1, 1);
        assertEquals(a.scalar(b), 4, 1e-9);
        Vector3D c = new Vector3D(2, 2, 2);
        Vector3D d = new Vector3D(1, 1, 1);
        assertEquals(c.scalar(d), 6, 1e-9);
    }
}
