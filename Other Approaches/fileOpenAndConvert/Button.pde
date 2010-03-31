class Button {
  String buttonText;
  Button() {
    buttonText = "Load File";
  }
  
  void render() {
    noStroke();
    fill(255);
    rect(width-100,height-40,100,40);
    fill(0);
    text(buttonText,width-100,height-20);
  }
  
  boolean isPressed() {
    if(mouseX > width-100 && mouseX < width && mouseY > height-40 && mouseY < height && mousePressed)
      return true;
    return false;
  }
}
