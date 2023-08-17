

union() {
	cube(size = [60, 20, 4]);
	translate(v = [10, 10, 0]) {
		union() {
			cylinder(h = 10, r = 3.5000000000);
			translate(v = [41.1100000000, 0, 0]) {
				cylinder(h = 10, r = 3.5000000000);
			}
		}
	}
}