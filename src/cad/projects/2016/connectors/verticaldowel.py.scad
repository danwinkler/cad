

union() {
	difference() {
		difference() {
			difference() {
				difference() {
					union() {
						cylinder(h = 30, r = 9.6000000000);
						union() {
							scale(v = [3, 1.2000000000, 1]) {
								cylinder(h = 5, r = 9.6000000000);
							}
							translate(v = [0, 0, 5]) {
								cylinder(h = 3, r1 = 11.5200000000, r2 = 9.6000000000);
							}
						}
					}
					translate(v = [0, 0, -1]) {
						cylinder(h = 32, r = 6.6000000000);
					}
				}
				translate(v = [0, -5, 20]) {
					rotate(a = 90, v = [1, 0, 0]) {
						cylinder($fn = 12, h = 6, r = 1.5000000000);
					}
				}
			}
			translate(v = [-20, 0, 0]) {
				union() {
					cylinder($fn = 12, h = 5, r = 1.5000000000);
					translate(v = [0, 0, 3]) {
						cylinder($fn = 12, h = 2, r1 = 1.5000000000, r2 = 3);
					}
				}
			}
		}
		translate(v = [20, 0, 0]) {
			union() {
				cylinder($fn = 12, h = 5, r = 1.5000000000);
				translate(v = [0, 0, 3]) {
					cylinder($fn = 12, h = 2, r1 = 1.5000000000, r2 = 3);
				}
			}
		}
	}
}