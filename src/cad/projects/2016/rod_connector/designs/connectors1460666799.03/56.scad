

difference() {
	intersection() {
		hull() {
			rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
				rotate(a = -90.0000000000, v = [-0.9914448614, 0.1305261922, 0.0000000000]) {
					cylinder(h = 60, r = 16.2000000000);
				}
			}
			rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
				rotate(a = -90.0000000000, v = [0.3826834324, -0.9238795325, 0.0000000000]) {
					cylinder(h = 60, r = 16.2000000000);
				}
			}
			rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
				rotate(a = -151.9205722594, v = [-0.4117825928, 0.2280109476, 0.0000000000]) {
					cylinder(h = 60, r = 16.2000000000);
				}
			}
			rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
				rotate(a = -161.5616070448, v = [0.2692672153, -0.1659253944, 0.0000000000]) {
					cylinder(h = 60, r = 16.2000000000);
				}
			}
		}
		sphere(r = 60);
	}
	union() {
		rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
			rotate(a = -90.0000000000, v = [-0.9914448614, 0.1305261922, 0.0000000000]) {
				translate(v = [0, 0, 35]) {
					cylinder(h = 100, r = 13.2000000000);
				}
			}
		}
		rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
			rotate(a = -90.0000000000, v = [0.3826834324, -0.9238795325, 0.0000000000]) {
				translate(v = [0, 0, 35]) {
					cylinder(h = 100, r = 13.2000000000);
				}
			}
		}
		rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
			rotate(a = -151.9205722594, v = [-0.4117825928, 0.2280109476, 0.0000000000]) {
				translate(v = [0, 0, 35]) {
					cylinder(h = 100, r = 13.2000000000);
				}
			}
		}
		rotate(a = -150.2044300830, v = [-0.3560759648, -0.3465924684, 0.0000000000]) {
			rotate(a = -161.5616070448, v = [0.2692672153, -0.1659253944, 0.0000000000]) {
				translate(v = [0, 0, 35]) {
					cylinder(h = 100, r = 13.2000000000);
				}
			}
		}
	}
}