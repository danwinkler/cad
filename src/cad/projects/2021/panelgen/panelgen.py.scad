

union() {
	union() {
		union() {
			translate(v = [40, 40]) {
				translate(v = [-3, -4]) {
					import(file = "mini_pushbutton.stl", origin = [0, 0]);
				}
			}
		}
		difference() {
			cube(size = [100, 100, 10]);
			union() {
				translate(v = [40, 40]) {
					cylinder(h = 20, r = 8);
					translate(v = [-10, -10, 0]) {
						cube(size = [20, 20, 5]);
					}
				}
			}
		}
	}
}