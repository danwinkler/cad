

union() {
	difference() {
		scale(v = [1, 1.0663265306, 1]) {
			translate(v = [-107.9500000000, -139.7000000000, 0]) {
				linear_extrude(height = 3) {
					import(file = "pickguard2.dxf", origin = [0, 0]);
				}
			}
		}
		translate(v = [-1000, -1000, -1]) {
			cube(size = [2000, 1000, 5]);
		}
	}
}