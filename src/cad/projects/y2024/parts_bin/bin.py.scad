

union() {
	difference() {
		union() {
			difference() {
				hull() {
					translate(v = [4, 4, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
					translate(v = [63, 4, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
					translate(v = [4, 29.5000000000, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
					translate(v = [63, 29.5000000000, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
				}
				translate(v = [1.5000000000, 1.5000000000, 1.5000000000]) {
					hull() {
						translate(v = [2.5000000000, 2.5000000000, 2.5000000000]) {
							cylinder($fn = 32, h = 41.5000000000, r = 2.5000000000);
							sphere($fn = 32, r = 2.5000000000);
						}
						translate(v = [61.5000000000, 2.5000000000, 2.5000000000]) {
							cylinder($fn = 32, h = 41.5000000000, r = 2.5000000000);
							sphere($fn = 32, r = 2.5000000000);
						}
						translate(v = [2.5000000000, 28.0000000000, 2.5000000000]) {
							cylinder($fn = 32, h = 41.5000000000, r = 2.5000000000);
							sphere($fn = 32, r = 2.5000000000);
						}
						translate(v = [61.5000000000, 28.0000000000, 2.5000000000]) {
							cylinder($fn = 32, h = 41.5000000000, r = 2.5000000000);
							sphere($fn = 32, r = 2.5000000000);
						}
					}
				}
			}
			intersection() {
				translate(v = [33.5000000000, 0, 0.5000000000]) {
					rotate(a = [-90, 0, 0]) {
						cylinder($fn = 32, h = 33.5000000000, r = 3.0000000000);
					}
				}
				hull() {
					translate(v = [4, 4, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
					translate(v = [63, 4, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
					translate(v = [4, 29.5000000000, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
					translate(v = [63, 29.5000000000, 4]) {
						cylinder($fn = 32, h = 40, r = 4);
						sphere($fn = 32, r = 4);
					}
				}
			}
		}
		translate(v = [33.5000000000, 0, 0]) {
			rotate(a = [-90, 0, 0]) {
				cylinder($fn = 32, h = 33.5000000000, r = 2.5000000000);
			}
		}
	}
}