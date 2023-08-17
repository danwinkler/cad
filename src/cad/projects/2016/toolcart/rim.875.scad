

difference(){
	union() {
		union() {
			cylinder($fn = 60, h = 2, r = 19.1125000000);
			cylinder($fn = 60, h = 22.0500000000, r = 11.1125000000);
		}
	}
	/* Holes Below*/
	union(){
		union(){
			translate(v = [0, 0, -1]) {
				cylinder($fn = 60, h = 24.0500000000, r = 9.1125000000);
			}
		}
	} /* End Holes */ 
}