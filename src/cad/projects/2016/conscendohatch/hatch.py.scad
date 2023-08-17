

union() {
	difference() {
		translate(v = [0, -8.5000000000, 0]) {
			cube(size = [40, 17, 9]);
		}
		translate(v = [7, -10, 9]) {
			rotate(a = 150, v = [0, 1, 0]) {
				translate(v = [0, 0, -5]) {
					cube(size = [20, 20, 5]);
				}
			}
		}
	}
	translate(v = [25, -8.5000000000, 9]) {
		cube(size = [15, 17, 9]);
	}
	translate(v = [26, -13, 12]) {
		rotate(a = -3, v = [0, 1, 0]) {
			cube(size = [139, 26, 8]);
		}
	}
	translate(v = [163.5000000000, -4.2500000000, 0]) {
		cube(size = [1.5000000000, 8.5000000000, 29.7500000000]);
	}
	translate(v = [163.5000000000, -4.2500000000, 4.5000000000]) {
		rotate(a = -90, v = [1, 0, 0]) {
			linear_extrude(height = 8.5000000000) {
				polygon(paths = [[0, 1, 2, 3]], points = [[0, 0], [4.5000000000, 0], [1.5000000000, 4.5000000000], [0, 4.5000000000]]);
			}
		}
	}
	translate(v = [165, 0, -8]) {
		rotate(a = -85, v = [0, 1, 0]) {
			difference() {
				difference() {
					cylinder(h = 140, r1 = 31.7500000000, r2 = 25.5000000000);
					cylinder(h = 140, r1 = 21.7500000000, r2 = 15.5000000000);
				}
				translate(v = [-100, -50, 0]) {
					cube(size = [100, 100, 200]);
				}
			}
		}
	}
}