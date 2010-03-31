void setup() {
  size(200,200);
}

void draw() {
  PImage img = loadImage("img.jpg");
  PImage croppedImage = cropAndResize(img, 75, 75);
  image(croppedImage, 0, 0);
}

PImage cropAndResize(PImage img, int w, int h) {
  int shorterDim;
  if(img.width >= img.height)
    shorterDim = img.height;
  else
    shorterDim = img.width;
  PImage newImg = createImage(shorterDim,shorterDim,RGB);
  for(int x = 0; x < shorterDim; x++) {
    for(int y = 0; y < shorterDim; y++) {
      newImg.pixels[y*newImg.width + x] = img.pixels[y*img.width + x];
    }
  }
  newImg.resize(w, h);
  
  return newImg;
}
