

union() {
	difference() {
		union() {
			union() {
				union() {
					translate(v = [0, 0, 10]) {
						rotate(a = 45, v = [0, 0, 1]) {
							rotate(a = 10, v = [0, 1, 0]) {
								difference() {
									translate(v = [-13.6500000000, -23.1500000000, 0]) {
										cube(size = [27.3000000000, 46.3000000000, 40]);
									}
									union() {
										translate(v = [9.6500000000, -9.5000000000, 25]) {
											rotate(a = 90, v = [0, 1, 0]) {
												union() {
													union() {
														translate(v = [0, 0, -12]) {
															cylinder($fn = 12, h = 16, r = 1.9000000000);
														}
														translate(v = [0, 0, 1]) {
															cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
														}
													}
													translate(v = [0, 0, 4]) {
														cylinder($fn = 12, h = 3, r = 4);
													}
												}
											}
										}
										translate(v = [9.6500000000, 9.5000000000, 25]) {
											rotate(a = 90, v = [0, 1, 0]) {
												union() {
													union() {
														translate(v = [0, 0, -12]) {
															cylinder($fn = 12, h = 16, r = 1.9000000000);
														}
														translate(v = [0, 0, 1]) {
															cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
														}
													}
													translate(v = [0, 0, 4]) {
														cylinder($fn = 12, h = 3, r = 4);
													}
												}
											}
										}
										translate(v = [-9.6500000000, -9.5000000000, 25]) {
											rotate(a = -90, v = [0, 1, 0]) {
												union() {
													union() {
														translate(v = [0, 0, -12]) {
															cylinder($fn = 12, h = 16, r = 1.9000000000);
														}
														translate(v = [0, 0, 1]) {
															cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
														}
													}
													translate(v = [0, 0, 4]) {
														cylinder($fn = 12, h = 3, r = 4);
													}
												}
											}
										}
										translate(v = [-9.6500000000, 9.5000000000, 25]) {
											rotate(a = -90, v = [0, 1, 0]) {
												union() {
													union() {
														translate(v = [0, 0, -12]) {
															cylinder($fn = 12, h = 16, r = 1.9000000000);
														}
														translate(v = [0, 0, 1]) {
															cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
														}
													}
													translate(v = [0, 0, 4]) {
														cylinder($fn = 12, h = 3, r = 4);
													}
												}
											}
										}
										translate(v = [0, 19.1500000000, 25]) {
											rotate(a = -90, v = [1, 0, 0]) {
												union() {
													union() {
														translate(v = [0, 0, -12]) {
															cylinder($fn = 12, h = 16, r = 1.9000000000);
														}
														translate(v = [0, 0, 1]) {
															cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
														}
													}
													translate(v = [0, 0, 4]) {
														cylinder($fn = 12, h = 3, r = 4);
													}
												}
											}
										}
										translate(v = [0, -19.1500000000, 25]) {
											rotate(a = 90, v = [1, 0, 0]) {
												union() {
													union() {
														translate(v = [0, 0, -12]) {
															cylinder($fn = 12, h = 16, r = 1.9000000000);
														}
														translate(v = [0, 0, 1]) {
															cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
														}
													}
													translate(v = [0, 0, 4]) {
														cylinder($fn = 12, h = 3, r = 4);
													}
												}
											}
										}
									}
								}
							}
						}
					}
					translate(v = [0, 0, 0]) {
						rotate(a = 45, v = [0, 0, 1]) {
							translate(v = [-13.4426258286, -23.1500000000, 0]) {
								cube(size = [26.8852516572, 46.3000000000, 12.3702976252]);
							}
						}
					}
				}
				union() {
					translate(v = [-35.0000000000, -35.0000000000, 0]) {
						cube(size = [70, 70, 4]);
					}
					rotate(a = 45, v = [0, 0, 1]) {
						translate(v = [-35.0000000000, -35.0000000000, 0]) {
							cube(size = [70, 70, 4]);
						}
					}
				}
			}
			union() {
				translate(v = [0, 0, 4]) {
					intersection() {
						translate(v = [-2.0000000000, -37.5000000000, 0]) {
							cube(size = [4, 75, 20]);
						}
						rotate(a = 90, v = [0, 1, 0]) {
							translate(v = [0, 0, -2.0000000000]) {
								scale(v = [20, 37.5000000000, 1]) {
									cylinder($fn = 32, h = 4, r = 1);
								}
							}
						}
					}
				}
				translate(v = [0, 0, 4]) {
					intersection() {
						translate(v = [-37.5000000000, -2.0000000000, 0]) {
							cube(size = [75, 4, 20]);
						}
						rotate(a = 90, v = [1, 0, 0]) {
							translate(v = [0, 0, -2.0000000000]) {
								scale(v = [37.5000000000, 20, 1]) {
									cylinder($fn = 32, h = 4, r = 1);
								}
							}
						}
					}
				}
			}
		}
		union() {
			union() {
				translate(v = [0, 0, 10]) {
					rotate(a = 45, v = [0, 0, 1]) {
						rotate(a = 10, v = [0, 1, 0]) {
							translate(v = [-9.6500000000, -19.1500000000, 0]) {
								cube(size = [19.3000000000, 38.3000000000, 41]);
							}
						}
					}
				}
				rotate(a = 45, v = [0, 0, 1]) {
					translate(v = [3, 0, -1]) {
						cylinder($fn = 12, h = 30, r = 1.9000000000);
					}
					translate(v = [3, 10, -1]) {
						cylinder($fn = 12, h = 30, r = 1.9000000000);
					}
					translate(v = [3, -10, -1]) {
						cylinder($fn = 12, h = 30, r = 1.9000000000);
					}
				}
			}
			rotate(a = 45, v = [0, 0, 1]) {
				translate(v = [33.0000000000, 0, 0]) {
					union() {
						union() {
							translate(v = [0, 0, -12]) {
								cylinder($fn = 12, h = 16, r = 1.9000000000);
							}
							translate(v = [0, 0, 1]) {
								cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
							}
						}
						translate(v = [0, 0, 4]) {
							cylinder($fn = 12, h = 3, r = 4);
						}
					}
				}
				translate(v = [-33.0000000000, 0, 0]) {
					union() {
						union() {
							translate(v = [0, 0, -12]) {
								cylinder($fn = 12, h = 16, r = 1.9000000000);
							}
							translate(v = [0, 0, 1]) {
								cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
							}
						}
						translate(v = [0, 0, 4]) {
							cylinder($fn = 12, h = 3, r = 4);
						}
					}
				}
				translate(v = [0, 33.0000000000, 0]) {
					union() {
						union() {
							translate(v = [0, 0, -12]) {
								cylinder($fn = 12, h = 16, r = 1.9000000000);
							}
							translate(v = [0, 0, 1]) {
								cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
							}
						}
						translate(v = [0, 0, 4]) {
							cylinder($fn = 12, h = 3, r = 4);
						}
					}
				}
				translate(v = [0, -33.0000000000, 0]) {
					union() {
						union() {
							translate(v = [0, 0, -12]) {
								cylinder($fn = 12, h = 16, r = 1.9000000000);
							}
							translate(v = [0, 0, 1]) {
								cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
							}
						}
						translate(v = [0, 0, 4]) {
							cylinder($fn = 12, h = 3, r = 4);
						}
					}
				}
			}
		}
	}
}