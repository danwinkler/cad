

union() {
	difference() {
		union() {
			translate(v = [0, 2.5000000000, 0]) {
				rotate(a = 90, v = [1, 0, 0]) {
					linear_extrude(height = 5) {
						polygon(paths = [[0, 1, 2, 3, 4, 5]], points = [[0, 5], [21, 21], [19, 54], [0, 80], [-19, 54], [-21, 21]]);
					}
				}
			}
			cylinder(h = 78, r1 = 5, r2 = 1);
		}
		cylinder($fn = 36, h = 10, r = 2.7000000000);
	}
}