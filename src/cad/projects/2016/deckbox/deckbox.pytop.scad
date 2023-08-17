

union() {
	difference() {
		difference() {
			difference() {
				translate(v = [0, 0, 55]) {
					cube(size = [83, 57, 55]);
				}
				translate(v = [5, 5, 5]) {
					cube(size = [73, 47, 100]);
				}
			}
			translate(v = [2, 0, 55]) {
				rotate(a = 90, v = [0, 0, 1]) {
					rotate(a = 90, v = [1, 0, 0]) {
						linear_extrude(height = 79) {
							polygon(paths = [[0, 1, 2, 3]], points = [[5, -2], [55, -2], [55, 20], [5, 0]]);
						}
					}
				}
			}
		}
		translate(v = [41, 53.0000000000, 65.0000000000]) {
			sphere($fn = 20, r = 3);
		}
	}
}