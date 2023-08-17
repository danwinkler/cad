

difference(){
	union() {
		union() {
			difference() {
				cube(size = [10, 4, 10]);
				translate(v = [5.0000000000, 0, 5.0000000000]) {
					rotate(a = -90, v = [1, 0, 0]) {
						translate(v = [0, 0, -3.5000000000]) {
							union() {
								translate(v = [0, 0, -0.0100000000]) {
									cylinder($fn = 24, h = 4.0200000000, r = 2);
								}
								translate(v = [0, 0, 4]) {
									cylinder($fn = 24, h = 3.5100000000, r1 = 2, r2 = 4);
								}
								translate(v = [0, 0, 7.5000000000]) {
									cylinder($fn = 24, h = 2.0100000000, r = 4);
								}
							}
						}
					}
				}
			}
			translate(v = [10, 0, 0]) {
				difference() {
					cube(size = [12.0000000000, 10, 10]);
					union() {
						translate(v = [6.0000000000, 3.0000000000, -1]) {
							cylinder($fn = 24, h = 12, r = 4.0000000000);
						}
						translate(v = [6.0000000000, 4.0000000000, 5.0000000000]) {
							rotate(a = -90, v = [1, 0, 0]) {
								cylinder($fn = 24, h = 12, r = 3.2000000000);
							}
						}
						translate(v = [-0.0100000000, 5, 1]) {
							minkowski() {
								translate(v = [0.0010000000, 1.7000000000, 1.7000000000]) {
									cube(size = [1.9980000000, 0.6000000000, 4.6000000000]);
								}
								rotate(a = 90, v = [0, 1, 0]) {
									cylinder($fn = 12, h = 0.0010000000, r = 1.7000000000);
								}
							}
						}
						translate(v = [10.0100000000, 5, 1]) {
							minkowski() {
								translate(v = [0.0010000000, 1.7000000000, 1.7000000000]) {
									cube(size = [1.9980000000, 0.6000000000, 4.6000000000]);
								}
								rotate(a = 90, v = [0, 1, 0]) {
									cylinder($fn = 12, h = 0.0010000000, r = 1.7000000000);
								}
							}
						}
					}
				}
			}
			translate(v = [22.0000000000, 0, 0]) {
				difference() {
					cube(size = [10, 4, 10]);
					translate(v = [5.0000000000, 0, 5.0000000000]) {
						rotate(a = -90, v = [1, 0, 0]) {
							translate(v = [0, 0, -3.5000000000]) {
								union() {
									translate(v = [0, 0, -0.0100000000]) {
										cylinder($fn = 24, h = 4.0200000000, r = 2);
									}
									translate(v = [0, 0, 4]) {
										cylinder($fn = 24, h = 3.5100000000, r1 = 2, r2 = 4);
									}
									translate(v = [0, 0, 7.5000000000]) {
										cylinder($fn = 24, h = 2.0100000000, r = 4);
									}
								}
							}
						}
					}
				}
			}
		}
		translate(v = [0, -17, 0]) {
			union() {
				translate(v = [9.6500000000, 0, 0]) {
					union() {
						minkowski() {
							translate(v = [-0.6000000000, 6.7000000000, 5.8000000000]) {
								cube(size = [0.2000000000, 0.6000000000, 4.4000000000]);
							}
							sphere($fn = 12, r = 1.4000000000);
						}
						translate(v = [-1.5000000000, 0, 0]) {
							translate(v = [0, 5.8500000000, 0]) {
								cube(size = [1.5000000000, 6.1500000000, 16]);
							}
						}
					}
				}
				translate(v = [22.3500000000, 0, 0]) {
					union() {
						minkowski() {
							translate(v = [0.4000000000, 6.7000000000, 5.8000000000]) {
								cube(size = [0.2000000000, 0.6000000000, 4.4000000000]);
							}
							sphere($fn = 12, r = 1.4000000000);
						}
						translate(v = [0, 5.8500000000, 0]) {
							cube(size = [1.5000000000, 6.1500000000, 16]);
						}
					}
				}
				difference() {
					union() {
						translate(v = [-3, 10.4000000000, 0]) {
							translate(v = [2, 2, 2]) {
								minkowski() {
									cube(size = [34.0000000000, 1, 12]);
									sphere($fn = 24, r = 2);
								}
							}
						}
						translate(v = [0, 0, 0]) {
							translate(v = [0, 5.8500000000, 0]) {
								cube(size = [6.1500000000, 4.6000000000, 16]);
							}
						}
						translate(v = [25.8500000000, 0, 0]) {
							translate(v = [0, 5.8500000000, 0]) {
								cube(size = [6.1500000000, 4.6000000000, 16]);
							}
						}
						translate(v = [-3, 0, 0]) {
							translate(v = [0, 7.1000000000, 0]) {
								difference() {
									translate(v = [2, 2, 2]) {
										minkowski() {
											cube(size = [34.0000000000, 3.5000000000, 0.5000000000]);
											sphere($fn = 24, r = 2);
										}
									}
									translate(v = [-1, 0, 4.0000000000]) {
										rotate(a = 90, v = [0, 1, 0]) {
											cylinder($fn = 24, h = 40.0000000000, r = 3.5000000000);
										}
									}
								}
							}
						}
						translate(v = [-3, 0, 16]) {
							scale(v = [1, 1, -1]) {
								translate(v = [0, 7.1000000000, 0]) {
									difference() {
										translate(v = [2, 2, 2]) {
											minkowski() {
												cube(size = [34.0000000000, 3.5000000000, 0.5000000000]);
												sphere($fn = 24, r = 2);
											}
										}
										translate(v = [-1, 0, 4.0000000000]) {
											rotate(a = 90, v = [0, 1, 0]) {
												cylinder($fn = 24, h = 40.0000000000, r = 3.5000000000);
											}
										}
									}
								}
							}
						}
					}
					translate(v = [16.0000000000, 10, 8.0000000000]) {
						rotate(a = -90, v = [1, 0, 0]) {
							cylinder($fn = 24, h = 5.4000000000, r = 3.2000000000);
						}
					}
				}
			}
		}
	}
	/* Holes Below*/
	union(){
		translate(v = [0, -17, 0]){
			union(){
				translate(v = [9.6500000000, 0, 0]){
					union(){
						translate(v = [-1.5000000000, 0, 0]){
							translate(v = [0, 5.8500000000, 0]){
								translate(v = [-2, 0, -1]) {
									cube(size = [2, 6.1500000000, 18]);
								}
								translate(v = [1.5000000000, 0, -1]) {
									cube(size = [1, 4.1500000000, 4]);
								}
								translate(v = [1.5000000000, 0, 13]) {
									cube(size = [1, 4.1500000000, 4]);
								}
							}
						}
					}
				}
				translate(v = [22.3500000000, 0, 0]){
					union(){
						translate(v = [0, 5.8500000000, 0]){
							translate(v = [1.5000000000, 0, -1]) {
								cube(size = [2, 6.1500000000, 18]);
							}
							translate(v = [-1, 0, -1]) {
								cube(size = [1, 4.1500000000, 4]);
							}
							translate(v = [-1, 0, 13]) {
								cube(size = [1, 4.1500000000, 4]);
							}
						}
					}
				}
			}
		}
	} /* End Holes */ 
}