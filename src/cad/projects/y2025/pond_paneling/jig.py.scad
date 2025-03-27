

union() {
	difference() {
		minkowski() {
			translate(v = [5, 5, 5]) {
				cube(size = [48.1000000000, 98.9000000000, 61]);
			}
			sphere($fn = 36, r = 5);
		}
		difference() {
			translate(v = [10, 10, 26]) {
				rotate(a = -7.5000000000, v = [1, 0, 0]) {
					cube(size = [38.1000000000, 177.8000000000, 66]);
				}
			}
			cube(size = [58.1000000000, 108.9000000000, 26]);
		}
		translate(v = [29.0500000000, 73.5000000000, -1]) {
			union() {
				cylinder($fn = 90, h = 28, r = 6);
				cylinder($fn = 90, h = 14, r = 6.3750000000);
			}
		}
		translate(v = [29.0500000000, 48.1000000000, -1]) {
			union() {
				cylinder($fn = 90, h = 28, r = 6);
				cylinder($fn = 90, h = 14, r = 6.3750000000);
			}
		}
	}
}