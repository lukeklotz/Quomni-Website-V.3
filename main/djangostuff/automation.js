// Get all the gallery images
const galleryImages = document.querySelectorAll('.gallery__image');

// Add a click event listener to each image
galleryImages.forEach((image) => {
  image.addEventListener('click', () => {
    // Add a class to the clicked image to enter full screen mode
    image.classList.add('gallery__image--fullscreen');
    
    // Add a click event listener to the image in full screen mode to exit
    image.addEventListener('click', () => {
      image.classList.remove('gallery__image--fullscreen');
    });
  });
});
