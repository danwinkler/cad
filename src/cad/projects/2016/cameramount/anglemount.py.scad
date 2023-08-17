

union() {
	cube(size = [24, 24, 3]);
	translate(v = [4, 4, 3]) {
		difference() {
			union() {
				cube(size = [16, 16, 12]);
				translate(v = [0, 8, 12]) {
					rotate(a = 90, v = [0, 1, 0]) {
						cylinder($fn = 64, h = 16, r = 8);
					}
				}
			}
			union() {
				translate(v = [3.9000000000, 0, 3.5000000000]) {
					cube(size = [4.2000000000, 16, 25]);
				}
				translate(v = [11.9000000000, 0, 3.5000000000]) {
					cube(size = [4.2000000000, 16, 25]);
				}
				translate(v = [0, 8, 12]) {
					rotate(a = 90, v = [0, 1, 0]) {
						cylinder($fn = 32, h = 16, r = 2.1500000000);
					}
				}
			}
		}
	}
}