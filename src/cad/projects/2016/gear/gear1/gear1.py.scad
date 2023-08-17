

union() {
	union() {
		cube(size = [20, 5, 68]);
		translate(v = [10, 1, 41]) {
			rotate(a = 90, v = [1, 0, 0]) {
				cylinder(h = 20, r = 3.5000000000);
			}
		}
		translate(v = [0, 0, 63]) {
			cube(size = [20, 54, 5]);
		}
		translate(v = [10, 27, 67]) {
			cylinder(h = 20, r = 3.5000000000);
		}
		translate(v = [0, 49, 0]) {
			cube(size = [20, 5, 68]);
		}
		translate(v = [10, 53, 41]) {
			rotate(a = -90, v = [1, 0, 0]) {
				cylinder(h = 20, r = 3.5000000000);
			}
		}
	}
}