

union() {
	rotate(a = 0, v = [0, 0, 1]) {
		translate(v = [0, 500, 0]) {
			rotate(a = -60, v = [0, 0, 1]) {
				translate(v = [0, -500, 0]) {
					rotate(a = 45, v = [0, 1, 0]) {
						difference() {
							cylinder(h = 50, r = 500);
							translate(v = [0, 0, -1]) {
								cylinder(h = 52, r = 420);
							}
						}
					}
				}
			}
		}
	}
	rotate(a = 120, v = [0, 0, 1]) {
		translate(v = [0, 500, 0]) {
			rotate(a = -60, v = [0, 0, 1]) {
				translate(v = [0, -500, 0]) {
					rotate(a = 45, v = [0, 1, 0]) {
						difference() {
							cylinder(h = 50, r = 500);
							translate(v = [0, 0, -1]) {
								cylinder(h = 52, r = 420);
							}
						}
					}
				}
			}
		}
	}
	rotate(a = 240, v = [0, 0, 1]) {
		translate(v = [0, 500, 0]) {
			rotate(a = -60, v = [0, 0, 1]) {
				translate(v = [0, -500, 0]) {
					rotate(a = 45, v = [0, 1, 0]) {
						difference() {
							cylinder(h = 50, r = 500);
							translate(v = [0, 0, -1]) {
								cylinder(h = 52, r = 420);
							}
						}
					}
				}
			}
		}
	}
}