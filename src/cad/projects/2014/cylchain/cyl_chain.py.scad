

difference() {
	union() {
		difference() {
			difference() {
				cylinder(h = 30, r = 10, center = true);
				cylinder(h = 31, r = 8, center = true);
			}
			translate(v = [0, 0, -15]) {
				union() {
					rotate(a = -45, v = [0, 0, 1]) {
						translate(v = [0, 7, 10]) {
							rotate(a = -90, v = [1, 0, 0]) {
								cylinder(r1 = 4, r2 = 0, h = 3);
							}
						}
					}
					difference() {
						intersection() {
							cylinder(h = 30, r = 8.5000000000, center = true);
							translate(v = [0.5000000000, 0.5000000000, -50]) {
								cube(size = [100, 100, 100]);
							}
						}
						cylinder(h = 31, r = 6, center = true);
					}
				}
			}
			rotate(a = 180, v = [0, 0, 1]) {
				translate(v = [0, 0, -15]) {
					union() {
						rotate(a = -45, v = [0, 0, 1]) {
							translate(v = [0, 7, 10]) {
								rotate(a = -90, v = [1, 0, 0]) {
									cylinder(r1 = 4, r2 = 0, h = 3);
								}
							}
						}
						difference() {
							intersection() {
								cylinder(h = 30, r = 8.5000000000, center = true);
								translate(v = [0.5000000000, 0.5000000000, -50]) {
									cube(size = [100, 100, 100]);
								}
							}
							cylinder(h = 31, r = 6, center = true);
						}
					}
				}
			}
		}
		translate(v = [0, 0, 15]) {
			difference() {
				union() {
					rotate(a = -45, v = [0, 0, 1]) {
						translate(v = [0, 6.5000000000, 10]) {
							rotate(a = -90, v = [1, 0, 0]) {
								cylinder(r1 = 4, r2 = 0, h = 3);
							}
						}
					}
					intersection() {
						cylinder(h = 30, r = 8, center = true);
						translate(v = [1, 1, -50]) {
							cube(size = [100, 100, 100]);
						}
					}
				}
				cylinder(h = 31, r = 6, center = true);
			}
		}
		rotate(a = 180, v = [0, 0, 1]) {
			translate(v = [0, 0, 15]) {
				difference() {
					union() {
						rotate(a = -45, v = [0, 0, 1]) {
							translate(v = [0, 6.5000000000, 10]) {
								rotate(a = -90, v = [1, 0, 0]) {
									cylinder(r1 = 4, r2 = 0, h = 3);
								}
							}
						}
						intersection() {
							cylinder(h = 30, r = 8, center = true);
							translate(v = [1, 1, -50]) {
								cube(size = [100, 100, 100]);
							}
						}
					}
					cylinder(h = 31, r = 6, center = true);
				}
			}
		}
	}
	union() {
		translate(v = [0, 0, 4.9000000000]) {
			cylinder(r1 = 8, r2 = 0, h = 10, center = true);
		}
	}
}