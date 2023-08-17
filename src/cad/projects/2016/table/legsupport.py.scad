

difference(){
	union() {
		difference() {
			union() {
				difference() {
					difference() {
						translate(v = [0, 0, -10]) {
							rotate(a = 10, v = [0, 1, 0]) {
								translate(v = [-13.6500000000, -23.1500000000, 0]) {
									cube(size = [27.3000000000, 46.3000000000, 50]);
								}
							}
						}
						translate(v = [0, 0, -20]) {
							translate(v = [-50.0000000000, -50.0000000000, 0]) {
								cube(size = [100, 100, 20]);
							}
						}
					}
					translate(v = [0, 0, 30]) {
						translate(v = [-50.0000000000, -50.0000000000, 0]) {
							cube(size = [100, 100, 20]);
						}
					}
				}
				union() {
					translate(v = [0, 23.1500000000, 0]) {
						rotate(a = -45, v = [0, 0, 1]) {
							translate(v = [0, 0, 0]) {
								difference() {
									cube(size = [21.2000000000, 40, 30]);
									translate(v = [0, 40, 0]) {
									}
								}
							}
						}
					}
					translate(v = [0, -23.1500000000, 0]) {
						rotate(a = 45, v = [0, 0, 1]) {
							translate(v = [0, -40, 0]) {
								difference() {
									cube(size = [21.2000000000, 40, 30]);
								}
							}
						}
					}
				}
			}
			translate(v = [0, 0, -10]) {
				rotate(a = 10, v = [0, 1, 0]) {
					translate(v = [-9.6500000000, -19.1500000000, 0]) {
						cube(size = [19.3000000000, 38.3000000000, 50]);
					}
				}
			}
		}
	}
	/* Holes Below*/
	union(){
		difference(){
			union(){
				union(){
					translate(v = [0, 23.1500000000, 0]){
						rotate(a = -45, v = [0, 0, 1]){
							translate(v = [0, 0, 0]){
								union(){
									translate(v = [0, 40, 0]){
										union() {
											translate(v = [10.6000000000, 1, 15.0000000000]) {
												rotate(a = 90, v = [1, 0, 0]) {
													cylinder(h = 31, r = 6.6000000000);
												}
											}
											translate(v = [10.6000000000, -15.0000000000, 4]) {
												rotate(a = 180, v = [1, 0, 0]) {
													union() {
														union() {
															translate(v = [0, 0, -24]) {
																cylinder($fn = 12, h = 28, r = 1.9000000000);
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
					}
					translate(v = [0, -23.1500000000, 0]){
						rotate(a = 45, v = [0, 0, 1]){
							translate(v = [0, -40, 0]){
								difference(){
									union() {
										translate(v = [10.6000000000, -1, 15.0000000000]) {
											rotate(a = -90, v = [1, 0, 0]) {
												cylinder(h = 31, r = 6.6000000000);
											}
										}
										translate(v = [10.6000000000, 15.0000000000, 4]) {
											rotate(a = 180, v = [1, 0, 0]) {
												union() {
													union() {
														translate(v = [0, 0, -24]) {
															cylinder($fn = 12, h = 28, r = 1.9000000000);
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
				}
			}
		}
	} /* End Holes */ 
}