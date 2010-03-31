import processing.core.*; 
import processing.xml.*; 

import nn.*; 
import controlP5.*; 
import javax.swing.JFileChooser; 

import java.applet.*; 
import java.awt.*; 
import java.awt.image.*; 
import java.awt.event.*; 
import java.io.*; 
import java.net.*; 
import java.text.*; 
import java.util.*; 
import java.util.zip.*; 
import java.util.regex.*; 

public class interestingness_meter extends PApplet {

// Neural Network Software
// By Don Miller, Eric Mika and Patrick Hebron
// Based heavily on the numberRecognizer example code by Daniel Shiffman
// http://www.shiffman.net/teaching/nature

// Using a Neural Network to recognize pixels of an input image
// Neural network code is all in the "code" folder




ControlP5 controlP5;

// The pixel data from each image file will be our training set
ArrayList pixelData;

// The size of our image data
int w = 75;
int h = 75;

// How many numbers are we going to try to guess
int total = 72; // 36 interesting, 36 boring
PImage[] trainingImages = new PImage[total];

// The Neural Network
Network nn;         

// How many training cycles have we done
int trainingCount;  

// We will train 5,000 iterations
int maxTrainingIterations = 5000;

// The input image from the user
PImage inputImage;

// states...
int state = 0;
final int WELCOME = 0;
final int TRAINING = 1; 
final int LOAD_FILE = 2;
final int GUESSING = 3;
final int RESULT = 4;

// What is the neural network's guess
float guess = 0;

PFont font;
PFont smallFont;

public void setup() {
  size(450, 450);
  background(0);

  // Load all the images
  loadTrainingImages();

  // Setup network
  nn = new Network(w*h,36);

  // Load the input image
  //inputImage = loadImage("images/2.gif");

  // Set up the font
  font = loadFont("DIN-Bold-20.vlw");
  smallFont = loadFont("DIN-Bold-10.vlw");
  textFont(smallFont);
  
  // Set up the buttons
  controlP5 = new ControlP5(this);
  controlP5.setColorBackground(180);
  controlP5.setColorActive(255);
  controlP5.setColorLabel(0);  
  controlP5.addButton("trainButton",0, (width - 80) / 2, height - 40,80,20).setLabel("TRAIN");  
  
  // Set the initial state
  state = WELCOME;
}

public void draw() {
  background(0);

  switch(state) {
    case WELCOME:
      drawWelcome();
      break;
      
    case TRAINING: 
      train();
      drawTraining();
      break;
      
    case LOAD_FILE:
      // not much to do here, button waits for response
      break;
      
    case GUESSING:
      guess();
      break;
      
    case RESULT:
      drawResult();
      break;      
  }
}

public void drawWelcome() {
  int squareSize = 50;
  
  // boring  
  for(int i = 0; i < (trainingImages.length / 2); i++) {
    image(trainingImages[i], (i % 4) * squareSize, (i / 4) * squareSize, squareSize, squareSize); 
  }
  
  // interesting
  for(int i = 0; i < (trainingImages.length / 2); i++) {
    image(trainingImages[i + (trainingImages.length / 2)], ((i % 4) * squareSize) + 250, (i / 4) * squareSize, squareSize, squareSize); 
  }  
}

public void drawResult() {
  //println(guess);
  
  textFont(font);
  fill(255);
  textAlign(CENTER, TOP);
  text("Your Image", 100, 50);
  text("Better Image", 350, 50);
  imageMode(CENTER);
  image(inputImage, 100, 120);
  image(trainingImages[constrain(round(guess * total), 0, total - 1)], 350, 120);

  text(round(guess * 100) + "% interesting.", width / 2, 300);
  textFont(smallFont);
}


// Load all the images
public void loadTrainingImages() {
  // list the images
  String[] interestingFilenames = listFileNames(sketchPath + "/data/interesting-images"); 
  String[] boringFilenames = listFileNames(sketchPath + "/data/boring-images"); 

  pixelData = new ArrayList();
  // +1 offset to ignore .ds_store hidden file
  // sloppy...
  for (int i = 0; i < total; i++) {
    
    if(i < (total / 2)) {
      println("adding boring " + i + " at " + i);
      trainingImages[i] = loadImage("boring-images/" + boringFilenames[i]);
    }
    else {
      println("adding interesting " + (i - (total / 2)) + " at " + i);      
      trainingImages[i] = loadImage("interesting-images/" + interestingFilenames[i - (total / 2)]);    
    }
    
    float[] binaryPixels = getPixels(trainingImages[i]);
    pixelData.add(binaryPixels);
  }
  
  
}


// This function returns all the files in a directory as an array of Strings  
public String[] listFileNames(String dir) {
  File file = new File(dir);
  if (file.isDirectory()) {
    String names[] = file.list();
    return names;
  } 
  else {
    // If it's not a directory
    return null;
  }
}



// Get an array of floats 0 to 1 from an input image
public float[] getPixels(PImage img) {
  // This isn't terribly optimized, making floating point arrays for pixels that are 1 or 0
  // However, this would theoretically work with grayscale pixels mapped from 0 to 1
  float[] binaryPixels = new float[w*h];
  for (int pix = 0; pix < w*h; pix++) {
    float b = brightness(img.pixels[pix]);
    
    // Each pixel is back or white (1 or 0)
    if (b > 128) binaryPixels[pix] = 1;
    else binaryPixels[pix] = 0;
    
    binaryPixels[pix] = map(b, 0, 255, 0, 1);
    //println(binaryPixels[pix]);
    
  }
  return binaryPixels;
}


// Train the network
public void train() {
  // Adjust this number to make training appear to be faster / slower
  int cyclesPerFrame = 50;

  for (int i = 0; i < cyclesPerFrame; i++) {
    // Pick a number 
    int num = (int) random(total);
    // Look at the pixels for that number
    float[] pixies = (float[]) pixelData.get(num);  
    // Train the network according to those pixels
    //nn.train(pixies, (float)num / total);
    
    //println("training on photo " + num);
    
    // index 0 to 35 is boring, or 0
    int trainingValue = 0;
    
    // index 36 to 71 is interesting
    if (num >= (total / 2)) {
      trainingValue = 1;      
    }
    
    nn.train(pixies, trainingValue);
    
    // Increase the training iteration count
    trainingCount++;
  }
}


// A little welcome message
public void welcome() {
  
}

public void guess() {
  float[] binaryPixels = getPixels(inputImage);
  float result = nn.feedForward(binaryPixels);
  // Here is the result
  guess = result;
  state = RESULT;
  controlP5.addButton("doneButton",0, (width - 80) / 2, height - 40,80,20).setLabel("DONE");
}

// Display info about the training
public void drawTraining() {
  pushMatrix();
  translate(20,10);
  textAlign(LEFT);

  // How much training is complete
  float percentage = (float) trainingCount / maxTrainingIterations;
  // Draw status bar
  float statusBar = percentage*width/2;
  stroke(255);
  noFill();
  rect(5,5,width/2,10);
  fill(255);
  rect(5,5,statusBar,10);

  // Now we'll show what the network is currently guessing for each input image
  fill(255);
  float mse = 0;
  for (int i = 0; i < pixelData.size(); i++) {
    float[] inp = (float[]) pixelData.get(i); 
    float known = (float) i/total;
    float result = nn.feedForward(inp);
    
    int offset = 0;
    if(i >= (total / 2)) {
      offset = 180;
    }
    
    text("My guess for image # " + i + " is " + nf((float)result,1,2), 5 + offset, 65 + (i % (total / 2)) * 10);
    mse += (result - known)*(result - known);
  }
  // How many interations
  text("Total iterations: " + trainingCount,5,30);
  // Root mean squarted error
  float rmse = sqrt(mse/pixelData.size());
  text("Root mean squared error: " + nf(rmse,1,4), 5,43);
  // If we've finished training
  if (percentage >= 1.0f) {
    controlP5.addButton("loadButton",0, (width - 80) / 2, height - 40,80,20).setLabel("LOAD"); 
    state = LOAD_FILE;
  }
  popMatrix();
}

public void trainButton(int theValue) {
  controlP5.remove("trainButton");
  state = TRAINING;
}


public void loadButton(int theValue) {
  controlP5.remove("loadButton");
  println("open load window");
  loadFile();
}

public void doneButton(int theValue) {
    controlP5.addButton("loadButton",0, (width - 80) / 2, height - 40,80,20).setLabel("LOAD"); 
    state = LOAD_FILE;
}


public void loadFile() {
  // Open a new file loader
  JFileChooser loader = new JFileChooser();
  int returnVal = loader.showOpenDialog(this);
  if(returnVal == JFileChooser.APPROVE_OPTION) {
    File file = loader.getSelectedFile();
    // Handle jpg and png
    if(file.getName().endsWith("jpg") || file.getName().endsWith("png") || file.getName().endsWith("gif")) {
      PImage tempImage = loadImage(file.getPath());

      // If image exists
      if(tempImage != null) {
        // crop and resize to match the training thumbnails
        inputImage = cropAndResize(tempImage, 75, 75);
        
        // we're done, change to guess state
        state = GUESSING;
      }
    }
  }
}


public PImage cropAndResize(PImage img, int w, int h) {
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

  static public void main(String args[]) {
    PApplet.main(new String[] { "--bgcolor=#FFFFFF", "interestingness_meter" });
  }
}
