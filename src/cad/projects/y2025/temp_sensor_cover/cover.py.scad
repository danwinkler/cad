

union() {
	union() {
		difference() {
			union() {
				difference() {
					union() {
						sphere($fn = 100, r = 40);
						rotate(a = 90, v = [1, 0, 0]) {
							cylinder($fn = 100, h = 40, r = 40);
						}
					}
					translate(v = [0, 0, -44]) {
						cylinder(h = 40, r = 100);
					}
				}
				translate(v = [0, 0, -5]) {
					cylinder($fn = 100, h = 5, r = 40);
				}
				translate(v = [-40, -40, -5]) {
					cube(size = [80, 40, 5]);
				}
			}
			union() {
				difference() {
					union() {
						sphere($fn = 100, r = 38);
						rotate(a = 90, v = [1, 0, 0]) {
							cylinder($fn = 100, h = 38, r = 38);
						}
					}
					translate(v = [0, 0, -43]) {
						cylinder(h = 38, r = 100);
					}
				}
				translate(v = [0, 0, -6]) {
					cylinder($fn = 100, h = 6, r = 38);
				}
				translate(v = [-38, -38, -6]) {
					cube(size = [76, 38, 6]);
				}
			}
		}
		difference() {
			translate(v = [0, 0, -5]) {
				union() {
					translate(v = [-25.0000000000, -40, 0]) {
						cube(size = [50, 50, 5.5000000000]);
					}
					intersection() {
						translate(v = [25.0000000000, 0, 0]) {
							difference() {
								translate(v = [0, -15, 0]) {
									cube(size = [15.0000000000, 25, 5.5000000000]);
								}
								translate(v = [15.0000000000, -15, -1]) {
									scale(v = [15.0000000000, 23, 1]) {
										cylinder($fn = 100, h = 7.5000000000, r = 1);
									}
								}
							}
						}
						union() {
							difference() {
								union() {
									sphere($fn = 100, r = 40);
									rotate(a = 90, v = [1, 0, 0]) {
										cylinder($fn = 100, h = 40, r = 40);
									}
								}
								translate(v = [0, 0, -44]) {
									cylinder(h = 40, r = 100);
								}
							}
							translate(v = [0, 0, -5]) {
								cylinder($fn = 100, h = 5, r = 40);
							}
							translate(v = [-40, -40, -5]) {
								cube(size = [80, 40, 5]);
							}
						}
					}
					intersection() {
						translate(v = [-25.0000000000, 0, 0]) {
							scale(v = [-1, 1, 1]) {
								difference() {
									translate(v = [0, -15, 0]) {
										cube(size = [15.0000000000, 25, 5.5000000000]);
									}
									translate(v = [15.0000000000, -15, -1]) {
										scale(v = [15.0000000000, 23, 1]) {
											cylinder($fn = 100, h = 7.5000000000, r = 1);
										}
									}
								}
							}
						}
						union() {
							difference() {
								union() {
									sphere($fn = 100, r = 40);
									rotate(a = 90, v = [1, 0, 0]) {
										cylinder($fn = 100, h = 40, r = 40);
									}
								}
								translate(v = [0, 0, -44]) {
									cylinder(h = 40, r = 100);
								}
							}
							translate(v = [0, 0, -5]) {
								cylinder($fn = 100, h = 5, r = 40);
							}
							translate(v = [-40, -40, -5]) {
								cube(size = [80, 40, 5]);
							}
						}
					}
				}
			}
			translate(v = [0, 0, -1]) {
				linear_extrude(height = 5) {
					offset(r = -2) {
						projection() {
							translate(v = [0, 0, -5]) {
								union() {
									translate(v = [-25.0000000000, -40, 0]) {
										cube(size = [50, 50, 5.5000000000]);
									}
									intersection() {
										translate(v = [25.0000000000, 0, 0]) {
											difference() {
												translate(v = [0, -15, 0]) {
													cube(size = [15.0000000000, 25, 5.5000000000]);
												}
												translate(v = [15.0000000000, -15, -1]) {
													scale(v = [15.0000000000, 23, 1]) {
														cylinder($fn = 100, h = 7.5000000000, r = 1);
													}
												}
											}
										}
										union() {
											difference() {
												union() {
													sphere($fn = 100, r = 40);
													rotate(a = 90, v = [1, 0, 0]) {
														cylinder($fn = 100, h = 40, r = 40);
													}
												}
												translate(v = [0, 0, -44]) {
													cylinder(h = 40, r = 100);
												}
											}
											translate(v = [0, 0, -5]) {
												cylinder($fn = 100, h = 5, r = 40);
											}
											translate(v = [-40, -40, -5]) {
												cube(size = [80, 40, 5]);
											}
										}
									}
									intersection() {
										translate(v = [-25.0000000000, 0, 0]) {
											scale(v = [-1, 1, 1]) {
												difference() {
													translate(v = [0, -15, 0]) {
														cube(size = [15.0000000000, 25, 5.5000000000]);
													}
													translate(v = [15.0000000000, -15, -1]) {
														scale(v = [15.0000000000, 23, 1]) {
															cylinder($fn = 100, h = 7.5000000000, r = 1);
														}
													}
												}
											}
										}
										union() {
											difference() {
												union() {
													sphere($fn = 100, r = 40);
													rotate(a = 90, v = [1, 0, 0]) {
														cylinder($fn = 100, h = 40, r = 40);
													}
												}
												translate(v = [0, 0, -44]) {
													cylinder(h = 40, r = 100);
												}
											}
											translate(v = [0, 0, -5]) {
												cylinder($fn = 100, h = 5, r = 40);
											}
											translate(v = [-40, -40, -5]) {
												cube(size = [80, 40, 5]);
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}