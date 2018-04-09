// credits: Jerome Mutterer, https://gist.github.com/mutterer/035ade419bf9c96475ce
// see also http://jcs.biologists.org/content/124/4/635

setBatchMode(true);
w=getWidth;h=getHeight;
roiManager("reset");
roiManager("add");
newImage("512", "8-bit black", w, h, 1);
size = 20;
for (y=0;y<h/size;y++) {
	for (x=0;x<w/size;x++) {
		setPixel (x*size+(y%2)*size/2,y*size,255);
	}
}
run("Make Binary");
run("Voronoi");setThreshold(0,1)
run("Make Binary");
roiManager("select",0);
run("Analyze Particles...", "display exclude clear add");
close();
setOption("Show All",true);
run("Restore Selection");
wait(1000);
roiManager("add");
for (i=0;i<nResults-1;i++) {
	roiManager("select",i);
	run("Enlarge...", "enlarge=0.5");
	getStatistics(area, mean, min, max, std, histogram);
	setColor(mean);
	fill();
}
wait(1000);
setOption("Show All",false);
run("Select None");
