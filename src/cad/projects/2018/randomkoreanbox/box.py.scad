

union() {
	difference() {
		difference() {
			minkowski() {
				translate(v = [2, 2, 2]) {
					cube(size = [64.0000000000, 44.0000000000, 34.0000000000]);
				}
				sphere($fn = 12, r = 2);
			}
			translate(v = [0, 0, 36.0000000000]) {
				cube(size = [68.0000000000, 48.0000000000, 3]);
			}
		}
		translate(v = [3, 3, 3]) {
			cube(size = [62.0000000000, 42.0000000000, 34.0000000000]);
		}
	}
	translate(v = [3, 3, 3]) {
		cube(size = [10, 10, 10]);
	}
	translate(v = [65.0000000000, 3, 3]) {
		scale(v = [-1, 1, 1]) {
			cube(size = [10, 10, 10]);
		}
	}
	translate(v = [65.0000000000, 45.0000000000, 3]) {
		scale(v = [1, -1, 1]) {
			scale(v = [-1, 1, 1]) {
				cube(size = [10, 10, 10]);
			}
		}
	}
	translate(v = [3, 45.0000000000, 3]) {
		scale(v = [1, -1, 1]) {
			cube(size = [10, 10, 10]);
		}
	}
}