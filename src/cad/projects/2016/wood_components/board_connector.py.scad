

union() {
	difference() {
		difference() {
			difference() {
				difference() {
					difference() {
						difference() {
							union() {
								union() {
									union() {
										cube(size = [100, 101, 50]);
										translate(v = [35.3553390593, 0, 50]) {
											rotate(a = -45, v = [0, 1, 0]) {
												cube(size = [100, 101, 50]);
											}
										}
									}
									cube(size = [100, 101, 85.3553390593]);
								}
								translate(v = [50.0000000000, 0, 0]) {
									cube(size = [50.0000000000, 101, 120.7106781187]);
								}
							}
							translate(v = [-1, 5, 5]) {
								cube(size = [102, 91, 40]);
							}
						}
						translate(v = [35.3553390593, 0, 50]) {
							rotate(a = -45, v = [0, 1, 0]) {
								translate(v = [-1, 5, 5]) {
									cube(size = [102, 91, 40]);
								}
							}
						}
					}
					translate(v = [33.3333333333, 33.6666666667, 0]) {
						union() {
							cylinder($fn = 12, h = 84.2791184895, r = 2);
							translate(v = [0, 0, -1.5000000000]) {
								cylinder($fn = 12, h = 3, r1 = 8, r2 = 0);
							}
						}
					}
				}
				translate(v = [33.3333333333, 67.3333333333, 0]) {
					union() {
						cylinder($fn = 12, h = 84.2791184895, r = 2);
						translate(v = [0, 0, -1.5000000000]) {
							cylinder($fn = 12, h = 3, r1 = 8, r2 = 0);
						}
					}
				}
			}
			translate(v = [66.6666666667, 33.6666666667, 0]) {
				union() {
					cylinder($fn = 12, h = 107.8493445290, r = 2);
					translate(v = [0, 0, -1.5000000000]) {
						cylinder($fn = 12, h = 3, r1 = 8, r2 = 0);
					}
				}
			}
		}
		translate(v = [66.6666666667, 67.3333333333, 0]) {
			union() {
				cylinder($fn = 12, h = 107.8493445290, r = 2);
				translate(v = [0, 0, -1.5000000000]) {
					cylinder($fn = 12, h = 3, r1 = 8, r2 = 0);
				}
			}
		}
	}
}