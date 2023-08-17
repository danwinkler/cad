

union() {
	difference() {
		union() {
			intersection() {
				translate(v = [-239.7125000000, 0, 95.2500000000]) {
					cube(size = [239.7125000000, 2, 101.6000000000]);
				}
				translate(v = [0, 0, 239.7125000000]) {
					rotate(a = -90, v = [1, 0, 0]) {
						minkowski() {
							translate(v = [0, 0, 15]) {
								cylinder($fn = 128, h = 55.7250000000, r = 224.7125000000);
							}
							sphere(r = 15);
						}
					}
				}
			}
			intersection() {
				translate(v = [-239.7125000000, 83.7250000000, 95.2500000000]) {
					cube(size = [239.7125000000, 2, 101.6000000000]);
				}
				translate(v = [0, 0, 239.7125000000]) {
					rotate(a = -90, v = [1, 0, 0]) {
						minkowski() {
							translate(v = [0, 0, 15]) {
								cylinder($fn = 128, h = 55.7250000000, r = 224.7125000000);
							}
							sphere(r = 15);
						}
					}
				}
			}
			translate(v = [-2, 0, 95.2500000000]) {
				cube(size = [2, 85.7250000000, 101.6000000000]);
			}
			intersection() {
				difference() {
					translate(v = [0, 0, 239.7125000000]) {
						rotate(a = -90, v = [1, 0, 0]) {
							minkowski() {
								translate(v = [0, 0, 15]) {
									cylinder($fn = 128, h = 55.7250000000, r = 224.7125000000);
								}
								sphere(r = 15);
							}
						}
					}
					translate(v = [0, 0, 2]) {
						translate(v = [0, 2, 0]) {
							translate(v = [0, 0, 237.7125000000]) {
								rotate(a = -90, v = [1, 0, 0]) {
									minkowski() {
										translate(v = [0, 0, 13]) {
											cylinder($fn = 128, h = 55.7250000000, r = 224.7125000000);
										}
										sphere(r = 13);
									}
								}
							}
						}
					}
				}
				translate(v = [-239.7125000000, 0, 95.2500000000]) {
					cube(size = [239.7125000000, 85.7250000000, 101.6000000000]);
				}
			}
			intersection() {
				translate(v = [-239.7125000000, 0, 95.2500000000]) {
					cube(size = [239.7125000000, 85.7250000000, 2]);
				}
				translate(v = [0, 0, 239.7125000000]) {
					rotate(a = -90, v = [1, 0, 0]) {
						minkowski() {
							translate(v = [0, 0, 15]) {
								cylinder($fn = 128, h = 55.7250000000, r = 224.7125000000);
							}
							sphere(r = 15);
						}
					}
				}
			}
		}
		translate(v = [-20, 0, 95.2500000000]) {
			cube(size = [10, 10, 10]);
		}
		translate(v = [-20, 75.7250000000, 95.2500000000]) {
			cube(size = [10, 10, 10]);
		}
		translate(v = [-181.2921032087, 0, 95.2500000000]) {
			cube(size = [10, 10, 10]);
		}
		translate(v = [-181.2921032087, 75.7250000000, 95.2500000000]) {
			cube(size = [10, 10, 10]);
		}
	}
}