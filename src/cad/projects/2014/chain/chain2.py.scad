

union() {
	union() {
		difference() {
			union() {
				translate(v = [4.0000000000, -20, 0]) {
					cube(size = [3, 30, 10]);
				}
				translate(v = [-7.0000000000, -20, 0]) {
					cube(size = [3, 30, 10]);
				}
			}
			translate(v = [0, -15, 5]) {
				rotate(a = 90, v = [0, 1, 0]) {
					cylinder(h = 16, r = 3, center = true);
				}
			}
		}
		translate(v = [-8.0000000000, 0, 0]) {
			cube(size = [16.0000000000, 10, 3]);
		}
		translate(v = [-8.0000000000, 0, 7]) {
			cube(size = [16.0000000000, 10, 3]);
		}
		translate(v = [7.5000000000, 0, 0]) {
			cube(size = [3, 30, 10]);
			translate(v = [0, 25, 5]) {
				rotate(a = 90, v = [0, 1, 0]) {
					cylinder(h = 3, r = 2.5000000000, center = true);
				}
			}
		}
		translate(v = [-10.5000000000, 0, 0]) {
			cube(size = [3, 30, 10]);
			translate(v = [3, 25, 5]) {
				rotate(a = 90, v = [0, 1, 0]) {
					cylinder(h = 3, r = 2.5000000000, center = true);
				}
			}
		}
	}
}