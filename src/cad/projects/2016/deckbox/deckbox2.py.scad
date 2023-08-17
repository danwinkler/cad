

union() {
	difference() {
		difference() {
			difference() {
				cube(size = [83, 57, 119]);
				translate(v = [5, 5, 5]) {
					cube(size = [73, 47, 1000]);
				}
			}
			translate(v = [2, -1, 108]) {
				cube(size = [79, 56, 6]);
			}
		}
		translate(v = [5, -1, 108]) {
			cube(size = [73, 7, 100]);
		}
	}
	translate(v = [-83, 0, 0]) {
		cube(size = [77, 49, 5]);
	}
}