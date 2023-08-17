import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class PointCloud
{
	public static float[] sub( float[] a, float[] b )
	{
		return new float[] { a[0] - b[0], a[1] - b[1], a[2] - b[2] };
	}

	public static float[] add( float[] a, float[] b )
	{
		return new float[] { a[0] + b[0], a[1] + b[1], a[2] + b[2] };
	}

	public static float[] mul( float[] a, float b )
	{
		return new float[] { a[0] * b, a[1] * b, a[2] * b };
	}

	public static float dot( float[] a, float[] b )
	{
		return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
	}

	public static float distance2( float[] a, float[] b )
	{
		float x = a[0]-b[0];
		float y = a[1]-b[1];
		float z = a[2]-b[2];
		return x*x+y*y+z*z;
	}

	public static float distance( float[] a, float[] b )
	{
		float x = a[0]-b[0];
		float y = a[1]-b[1];
		float z = a[2]-b[2];
		return (float)Math.sqrt( x*x+y*y+z*z );
	}

	public static float pointLineSegment2( float[] p, float[] l0, float[] l1 )
	{
		float[] v = sub( l1, l0 );
		float[] w = sub( p, l0 );


		float c1 = dot( w, v );
		if( c1 < 0 )
			return distance2( p, l0 );

		float c2 = dot( v, v );
		if( c2 < c1 )
			return distance2( p, l1 );

		float b = c1 / c2;
		float[] pb = add( l0, mul( v, b ) );
		return distance2( p, pb );
	}

	public static float pointLineSegment( float[] p, float[] l0, float[] l1 )
	{
		float[] v = sub( l1, l0 );
		float[] w = sub( p, l0 );

		float c1 = dot( w, v );
		if( c1 < 0 )
			return distance( p, l0 );

		float c2 = dot( v, v );
		if( c2 < c1 )
			return distance( p, l1 );

		float b = c1 / c2;
		float[] pb = add( l0, mul( v, b ) );
		return distance( p, pb );
	}

	public static float inverseSquare( float r2 )
	{
		return 1.f / r2;
	}

	public static float blobby( float r2, float a, float b )
	{
		return a*(float)Math.pow( Math.E, -b * r2 );
	}

	public static float metaball( float r, float a, float b )
	{
		float b3 = b/3.f;
		if( r < b3 )
		{
			return a * (1.f - ((3.f*r*r)/(b*b)));
		}
		else if( r < b )
		{
			return ((3.f*a)/2.f) * (float)Math.pow(1.f - (r/b), 2);
		}
		else
		{
			return 0;
		}

	}

	public static float softObject( float r2, float a, float b )
	{
		float b2 = b * b;
		float b4 = b2 * b2;
		float b6 = b4 * b2;

		float r4 = r2 * r2;
		float r6 = r4 * r2;

		if( r2 < b2 )
		{
			return a * (1 - ((4.f*r6)/(9.f*b6)) + ((17.f*r4)/(9.f*b4)) - ((22.f*r2)/(9*b2)) );
		}
		else
		{
			return 0;
		}
	}

	public static float[][] getPoints( float[][][] lines, float[] minBound, float[] maxBound, float resolution, float d, float r, int fieldFunction, float[] extras )
	{
		ArrayList<float[]> points = new ArrayList<float[]>();

		float rMin = d - r*.5f;
		float rMax = d + r*.5f;

		float[] pos = new float[3];
		for( float x = minBound[0]; x < maxBound[0]; x += resolution )
		{
			pos[0] = x;
			System.out.println( x );
			for( float y = minBound[1]; y < maxBound[1]; y += resolution )
			{
				pos[1] = y;
				for( float z = minBound[2]; z < maxBound[2]; z += resolution )
				{
					pos[2] = z;
					float v = 0;
					for( int i = 0; i < lines.length; i++ )
					{
						v += inverseSquare( pointLineSegment2( pos, lines[i][0], lines[i][1] ) );

						/*switch( fieldFunction )
						{
							case 0:

							break;
							case 1: v += blobby( pointLineSegment2( pos, lines[i][0], lines[i][1] ), extras[0], extras[1] ); break;
							case 2: v += metaball( pointLineSegment( pos, lines[i][0], lines[i][1] ), extras[0], extras[1] ); break;
							case 3: v += softObject( pointLineSegment2( pos, lines[i][0], lines[i][1] ), extras[0], extras[1] ); break;
						}
						*/
					}

					if( v > rMin && v < rMax )
					{
						points.add( new float[] { x, y, z } );
					}
				}
			}
		}

		float[][] ret = new float[points.size()][3];
		for( int i = 0; i < points.size(); i++ )
		{
			ret[i] = points.get( i );
		}
		return ret;
	}

	public static void main( String[] args )
	{
		try
		{
			List<String> lines = Files.readAllLines( FileSystems.getDefault().getPath( args[0] ), StandardCharsets.US_ASCII );
			String[] first = lines.get( 0 ).split( " " );
			float[] minBound = new float[] { Float.parseFloat( first[0] ), Float.parseFloat( first[1] ), Float.parseFloat( first[2] ) };
			float[] maxBound = new float[] { Float.parseFloat( first[3] ), Float.parseFloat( first[4] ), Float.parseFloat( first[5] ) };
			float resolution = Float.parseFloat( first[6] );
			float d = Float.parseFloat( first[7] );
			float r = Float.parseFloat( first[8] );
			int fieldFunction = 0;

			if( first.length > 9 ) fieldFunction = Integer.parseInt( first[9] );

			float[] extras = new float[first.length-10];
			for( int i = 10; i < first.length; i++ )
			{
				extras[i-10] = Float.parseFloat( first[i] );
			}

			float[][][] linesFloat = new float[lines.size()-1][2][3];
			for( int i = 1; i < lines.size(); i++ )
			{
				String[] line = lines.get( i ).split( " " );
				for( int j = 0; j < 6; j++ )
				{
					linesFloat[i-1][j/3][j%3] = Float.parseFloat( line[j] );
				}
			}

			float[][] points = getPoints( linesFloat, minBound, maxBound, resolution, d, r, fieldFunction, extras );
			StringBuilder sb = new StringBuilder();
			for( int i = 0; i < points.length; i++ )
			{
				sb.append( points[i][0] );
				sb.append( " " );
				sb.append( points[i][1] );
				sb.append( " " );
				sb.append( points[i][2] );
				sb.append( "\n" );
			}

			Files.write( FileSystems.getDefault().getPath( args[1] ), sb.toString().getBytes() );
		}
		catch( IOException e )
		{
			e.printStackTrace();
		}
	}
}
