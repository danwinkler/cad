

union() {
	difference() {
		translate(v = [0, 0, 0]) {
			minkowski() {
				cube(size = [115, 70, 0.0001000000]);
				difference() {
					sphere($fn = 24, r = 5);
					translate(v = [-5, -5, -5]) {
						cube(size = [10, 10, 5]);
					}
				}
			}
		}
		union() {
			translate(v = [1, 1, -1]) {
				cube(size = [113, 68, 10]);
			}
			translate(v = [-0.2000000000, -0.2000000000, 3]) {
				cube(size = [115.4000000000, 70.4000000000, 10]);
			}
		}
	}
}