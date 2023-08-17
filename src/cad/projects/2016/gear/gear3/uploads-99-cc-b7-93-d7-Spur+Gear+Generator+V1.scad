// Spur Gear Generator, V1.0
// Damon Printz
// 15 February 2014

// --------------INPUT-----------------------------
teeth = 24;   // number of teeth on gear
base = 3 / 2; // 1/2 length of base of tooth
top = 2 / 2;  // 1/2 length of top of tooth
height = 3;   // height of tooth
thick = 4;    // thickness of gear
hole = 4;     // radius of hole

//--------------PROGRAM----------------------------
// calculated variables
theta = 180 / teeth; // angle between midpoint perpendicular lines
spaceD = (base + top * cos(theta)) / sin(theta); // radius from midpoint of space to center of gear
baseD = spaceD * cos(theta) + top * sin(theta); // radius from midpoint of tooth baseline to center of gear
//echo("space radius = ");
//echo(spaceD);
//echo("base radius = ");
//echo(baseD);
//echo("theta = ");
//echo(theta);
mR = baseD + height / 2;
echo("Tooth Mesh Radius =");
echo(mR);
echo("Contact Circumference =");
echo(2 * 3.14 * mR);
gP = atan((base - top)/2 / height);
echo("Tooth Angle = ");
echo(gP);



module buildTooth()
{
  linear_extrude(thick, center = false, convexity = 1) polygon([[0,0],[0, baseD + height],[top, baseD + height],[base, baseD],[spaceD * sin(theta), spaceD * cos(theta)],[0,0]]);
  linear_extrude(thick, center = false, convexity = 1) mirror([1,0,0]) polygon([[0,0],[0, baseD + height],[top, baseD + height],[base, baseD],[spaceD * sin(theta), spaceD * cos(theta)],[0,0]]);
}
//translate([0,0, thick + 4])buildTooth();
difference()
{
  for(i = [0:theta*2:360])
  {
    rotate([0,0,i])buildTooth();
  }
  translate([0,0,-1]) cylinder(h = thick + 2, r = hole, $fn = 7 * hole);
}