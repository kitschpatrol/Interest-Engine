
PImage a;
int[] aPixels;
float tmpval;

void setup(){ 
  a = loadImage("flower.gif");
  // make window match image size
  size(a.width,a.height);    
  // create array the size of image  
  aPixels = new int[a.width*a.height];
}

void draw(){
  // load image at 0,0
  image(a,0,0);
  // load pixel data into pixels[] array (entire screen)
  loadPixels();
  // go thru array and print the color value of each pixel
  for(int i=0; i<pixels.length; i++){
    aPixels[i] = pixels[i];
    // values are 32 bits, for RGBA, so just pull out red value
    tmpval = red(aPixels[i]);
    // change to int, print the value to screen, but can be used for whatever
    println(int(tmpval));
  }
  // why do this shit more than once?
  noLoop();
}













