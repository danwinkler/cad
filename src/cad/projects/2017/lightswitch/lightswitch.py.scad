

union() {
	difference() {
		translate(v = [5, 5, 0]) {
			minkowski() {
				cube(size = [105, 60, 0.0001000000]);
				difference() {
					sphere($fn = 24, r = 5);
					translate(v = [-5, -5, -5]) {
						cube(size = [10, 10, 5]);
					}
				}
			}
		}
		union() {
			translate(v = [5, 5, -1]) {
				cube(size = [105, 60, 10]);
			}
			translate(v = [4, 4, 4]) {
				cube(size = [107, 62, 10]);
			}
		}
	}
}