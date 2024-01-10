function getRandomPosition(min, max) {
  const randX = Math.random() * (max - min) + min;
  const randY = Math.random() * (max - min) + min;
  return [randX, randY];
}

const randomImages = document.querySelectorAll('.draggable-image');

randomImages.forEach((image, index) => {
  const containerWidth = container.clientWidth / 2;
  const containerHeight = container.clientHeight / 2;
  const imageWidth = image.clientWidth;
  const imageHeight = image.clientHeight;

  let overlap = true;
  let randX, randY;

  while (overlap) {
    [randX, randY] = getRandomPosition(containerWidth - imageWidth, containerHeight - imageHeight);

    // Check if the current image overlaps with any previous images
    overlap = false;
    for (let i = 0; i < index; i++) {
      const prevImage = randomImages[i];
      const prevX = parseFloat(prevImage.style.left);
      const prevY = parseFloat(prevImage.style.top);
      const prevWidth = prevImage.clientWidth;
      const prevHeight = prevImage.clientHeight;

      if (
        randX < prevX + prevWidth &&
        randX + imageWidth > prevX &&
        randY < prevY + prevHeight &&
        randY + imageHeight > prevY
      ) {
        overlap = true;
        break;
      }
    }

    // Adjust position to ensure image is within the screen
    const { innerWidth, innerHeight } = window;
    if (randX < 0) randX = 0;
    if (randX + imageWidth > innerWidth) randX = innerWidth - imageWidth;
    if (randY < 0) randY = 50;
    if (randY + imageHeight > innerHeight) randY = innerHeight - imageHeight;
  }

  image.style.left = randX + 'px';
  image.style.top = randY + 'px';
});