

translate(v = [0, 0, 10]) {
	rotate(a = 180, v = [0, 1, 0]) {
		difference() {
			difference() {
				difference() {
					translate(v = [0, 0, 5]) {
						cube(center = true, size = [24, 24, 10]);
					}
					cylinder(h = 4.2000000000, r = 7.5000000000);
				}
				translate(v = [0, 0, 6.4500000000]) {
					cube(center = true, size = [6.8000000000, 6.8000000000, 4.5000000000]);
				}
			}
			cylinder(h = 12, r = 3.4000000000);
		}
	}
}