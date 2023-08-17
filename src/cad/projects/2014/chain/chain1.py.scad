

union() {
	union() {
		difference() {
			translate(v = [-10.0000000000, 0, 0]) {
				cube(size = [20, 10, 10]);
			}
			translate(v = [0, 5, 5]) {
				rotate(a = 90, v = [0, 1, 0]) {
					cylinder(h = 22, r = 3, center = true);
				}
			}
		}
		translate(v = [7.5000000000, 10, 0]) {
			cube(size = [3, 20, 10]);
			translate(v = [0, 15, 5]) {
				rotate(a = 90, v = [0, 1, 0]) {
					cylinder(h = 3, r = 2.5000000000, center = true);
				}
			}
		}
		translate(v = [-10.5000000000, 10, 0]) {
			cube(size = [3, 20, 10]);
			translate(v = [3, 15, 5]) {
				rotate(a = 90, v = [0, 1, 0]) {
					cylinder(h = 3, r = 2.5000000000, center = true);
				}
			}
		}
	}
}