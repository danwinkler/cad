

difference() {
	difference() {
		difference() {
			hull() {
				union() {
					union() {
						rotate(a = -112.9670952956, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [19.7813799521, 13.2000000000, 1]);
							}
						}
						rotate(a = -177.8490947668, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [43.7776724166, 13.2000000000, 1]);
							}
						}
						rotate(a = -77.5676307803, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [44.6799022502, 13.2000000000, 1]);
							}
						}
						rotate(a = -140.9690420392, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [45.0000000000, 13.2000000000, 1]);
							}
						}
						rotate(a = 103.1410956385, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [12.4643124189, 13.2000000000, 1]);
							}
						}
						rotate(a = 114.1908214377, v = [0, 0, 1]) {
							translate(v = [0, -6.6000000000, 0]) {
								cube(size = [45.0000000000, 13.2000000000, 1]);
							}
						}
					}
					translate(v = [0, 0, 9.6000063295]) {
						intersection() {
							hull() {
								rotate(a = 26.0775585139, v = [0.4047407225, -0.1715285065, -0.0000002332]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 76.6152199097, v = [0.0365123292, -0.9721519768, 0.0000009356]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 83.1620221697, v = [0.9696044444, 0.2137555464, -0.0000011834]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 90.0000886481, v = [0.6297402054, -0.7768058147, 0.0000001471]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 16.0802827559, v = [-0.2697304023, -0.0629733920, 0.0000003327]) {
									cylinder(h = 45, r = 9.6000000000);
								}
								rotate(a = 89.9999683355, v = [-0.9121857726, -0.4097769105, 0.0000013220]) {
									cylinder(h = 45, r = 9.6000000000);
								}
							}
							sphere(r = 45);
						}
					}
				}
			}
			translate(v = [0, 0, 9.6000063295]) {
				rotate(a = 26.0775585139, v = [0.4047407225, -0.1715285065, -0.0000002332]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 76.6152199097, v = [0.0365123292, -0.9721519768, 0.0000009356]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 83.1620221697, v = [0.9696044444, 0.2137555464, -0.0000011834]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 90.0000886481, v = [0.6297402054, -0.7768058147, 0.0000001471]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 16.0802827559, v = [-0.2697304023, -0.0629733920, 0.0000003327]) {
					translate(v = [0, 0, 20]) {
						cylinder(h = 45, r = 6.6000000000);
					}
				}
				rotate(a = 89.9999683355, v = [-0.9121857726, -0.4097769105, 0.0000013220]) {
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
				text(halign = "center", size = 8, text = "22", valign = "center");
			}
		}
	}
}