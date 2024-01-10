var dragItems = document.querySelectorAll(".draggable-image");
var container = document.querySelector(".image-container");

dragItems.forEach(function(dragItem) {
  var active = false;
  var currentX;
  var currentY;
  var initialX;
  var initialY;
  var xOffset = 0;
  var yOffset = 0;

  dragItem.addEventListener("touchstart", dragStart, false);
  dragItem.addEventListener("touchend", dragEnd, false);
  dragItem.addEventListener("touchmove", drag, false);

  dragItem.addEventListener("mousedown", dragStart, false);
  dragItem.addEventListener("mouseup", dragEnd, false);
  dragItem.addEventListener("mousemove", drag, false);

  function dragStart(e) {
    if (e.type === "touchstart") {
      initialX = e.touches[0].clientX - xOffset;
      initialY = e.touches[0].clientY - yOffset;
    } else {
      initialX = e.clientX - xOffset;
      initialY = e.clientY - yOffset;
    }

    active = true;
  }

  function dragEnd() {
    initialX = currentX;
    initialY = currentY;

    active = false;
  }

  function drag(e) {
    if (active) {
      e.preventDefault();

      if (e.type === "touchmove") {
        currentX = e.touches[0].clientX - initialX;
        currentY = e.touches[0].clientY - initialY;
      } else {
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;
      }

      xOffset = currentX;
      yOffset = currentY;

      setTranslate(currentX, currentY, dragItem);
    }
  }

  function setTranslate(xPos, yPos, el) {
    el.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
  }
});