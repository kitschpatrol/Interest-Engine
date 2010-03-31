// Neural Network Software
// By Don Miller, Eric Mika and Patrick Hebron

import javax.swing.JFileChooser;

PImage a;
boolean imageLoaded = false;

Button button;
PFont f;


void setup() {
  size(500,500);
  button = new Button();
  f = createFont("Georgia",16,true);
  textFont(f);
}

void draw() {
  // Draw loading button
  button.render();
  // Check if button is pressed
  if(button.isPressed())
    loadFile();
  
  // Draw image, if loaded
  if(imageLoaded) {
    // load image at 0,0
    image(a,0,0);
    // load pixel data into pixels[] array (entire screen)
    loadPixels();
    // iterate over pixel array
    for(int i=0; i < a.width*a.height; i++){
      // Get current pixel
      int c,r,g,b;
      c = a.pixels[i];  
      r = c >> 16 & 0xFF;       
      g = c >>  8 & 0xFF;
      b = c       & 0xFF; 
      
      // Convert pixels to black/white 
      // Using 382 as polarizer because (255*3)/2 = 382.5
      // Naturally, we can replace this with any pixel analysis op
      if(r+g+b > 382) 
        pixels[i] = color(255,255,255);
      else
        pixels[i] = color(0,0,0);
    }
    updatePixels();
  }
}

void loadFile() {
  // Open a new file loader
  JFileChooser loader = new JFileChooser();
  int returnVal = loader.showOpenDialog(this);
  if(returnVal == JFileChooser.APPROVE_OPTION) {
    File file = loader.getSelectedFile();
    // Handle jpg and png
    if(file.getName().endsWith("jpg") || file.getName().endsWith("png")) {
      a = loadImage(file.getPath());
      // If image exists
      if(a != null) {
        // Resize window to image size plus room for button
        size(a.width,a.height+60);
        frame.setSize(a.width,a.height+60);
        // Set display state
        imageLoaded = true;
      }
    }
  }
}
