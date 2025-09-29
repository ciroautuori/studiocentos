const baseURL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "/api/";
export const getImageUrl = (imagePath) => {
  if (!imagePath) return '';
  if (imagePath.startsWith('http')) return imagePath;
  if (imagePath.startsWith('/')) {
    imagePath = imagePath.substring(1);
  }
  return `${baseURL}/${imagePath}`;
};

export const handleImageError = (event, size = '800x450') => {
  const [width, height] = size.split('x').map(Number);
  event.target.src = `https://via.placeholder.com/${width}x${height}?text=Image+Not+Found`;
};
