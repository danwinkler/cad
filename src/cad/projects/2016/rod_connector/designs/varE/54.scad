

difference() {
	difference() {
		difference() {
			hull() {
				union() {
					union() {
						rotate(a = 62.0301888580, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [37.0072589797, 13.2000000000, 1]);
							}
						}
						rotate(a = 42.1672479175, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [45.0000000000, 13.2000000000, 1]);
							}
						}
						rotate(a = -0.7800997449, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [31.2441847613, 13.2000000000, 1]);
							}
						}
						rotate(a = -38.6642535181, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [45.0000000000, 13.2000000000, 1]);
							}
						}
					}
					translate(v = [0, 0, 9.5999992977]) {
						intersection() {
							hull() {
								rotate(a = 55.3240337793, v = [-0.7263243176, 0.3857024701, 0.0000003406]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 89.9999109776, v = [-0.6712970122, 0.7411884520, -0.0000000699]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 43.9726174278, v = [0.0094537439, 0.6942501433, -0.0000007037]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 89.9999901640, v = [0.6247556290, 0.7808203404, -0.0000014056]) {
									cylinder(h = 45, r = 9.6000000000);
								}
							}
							sphere(r = 45);
						}
					}
				}
			}
			translate(v = [0, 0, 9.5999992977]) {
				rotate(a = 55.3240337793, v = [-0.7263243176, 0.3857024701, 0.0000003406]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 89.9999109776, v = [-0.6712970122, 0.7411884520, -0.0000000699]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 43.9726174278, v = [0.0094537439, 0.6942501433, -0.0000007037]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 89.9999901640, v = [0.6247556290, 0.7808203404, -0.0000014056]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
			}
		}
		translate(v = [-100, -100, -100]) {
			cube(size = [200, 200, 100]);
		}
	}
	translate(v = [0, 0, 2]) {
		rotate(a = 180, v = [0, 1, 0]) {
			linear_extrude(height = 3) {
				text(halign = "center", size = 8, text = "54", valign = "center");
			}
		}
	}
}