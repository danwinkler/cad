

union() {
	intersection() {
		union() {
			difference() {
				difference() {
					difference() {
						intersection() {
							cube(size = [80, 80, 5]);
							translate(v = [0, 0, -1]) {
								cylinder(h = 7, r = 80);
							}
						}
						translate(v = [14.5000000000, 14.5000000000, -1]) {
							cylinder($fn = 12, h = 7, r = 1.5000000000);
						}
					}
					translate(v = [60, 14.5000000000, -1]) {
						cylinder($fn = 12, h = 7, r = 1.5000000000);
					}
				}
				translate(v = [14.5000000000, 60, -1]) {
					cylinder($fn = 12, h = 7, r = 1.5000000000);
				}
			}
			translate(v = [0, 5, 0]) {
				rotate(a = 90, v = [1, 0, 0]) {
					difference() {
						difference() {
							difference() {
								intersection() {
									cube(size = [80, 80, 5]);
									translate(v = [0, 0, -1]) {
										cylinder(h = 7, r = 80);
									}
								}
								translate(v = [14.5000000000, 14.5000000000, -1]) {
									cylinder($fn = 12, h = 7, r = 1.5000000000);
								}
							}
							translate(v = [60, 14.5000000000, -1]) {
								cylinder($fn = 12, h = 7, r = 1.5000000000);
							}
						}
						translate(v = [14.5000000000, 60, -1]) {
							cylinder($fn = 12, h = 7, r = 1.5000000000);
						}
					}
				}
			}
			translate(v = [5, 0, 0]) {
				rotate(a = -90, v = [0, 1, 0]) {
					difference() {
						difference() {
							difference() {
								intersection() {
									cube(size = [80, 80, 5]);
									translate(v = [0, 0, -1]) {
										cylinder(h = 7, r = 80);
									}
								}
								translate(v = [14.5000000000, 14.5000000000, -1]) {
									cylinder($fn = 12, h = 7, r = 1.5000000000);
								}
							}
							translate(v = [60, 14.5000000000, -1]) {
								cylinder($fn = 12, h = 7, r = 1.5000000000);
							}
						}
						translate(v = [14.5000000000, 60, -1]) {
							cylinder($fn = 12, h = 7, r = 1.5000000000);
						}
					}
				}
			}
		}
		sphere(r = 79);
	}
}