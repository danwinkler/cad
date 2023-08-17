

difference(){
	union() {
		union() {
			cylinder($fn = 60, h = 2, r = 27.0500000000);
			cylinder($fn = 60, h = 59.1500000000, r = 19.0500000000);
			translate(v = [0, 0, 59.1500000000]) {
				sphere($fn = 60, r = 19.0500000000);
			}
		}
	}
	/* Holes Below*/
	union(){
		union(){
			translate(v = [0, 0, -1]) {
				cylinder(h = 60.1500000000, r = 17.0500000000);
			}
			translate(v = [0, 0, 59.1500000000]) {
				sphere($fn = 60, r = 17.0500000000);
			}
		}
	} /* End Holes */ 
}