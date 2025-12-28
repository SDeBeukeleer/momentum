const sharp = require('sharp');
const path = require('path');

const sizes = [192, 512];
const iconsDir = path.join(__dirname, '../public/icons');

async function generateIcons() {
  for (const size of sizes) {
    // Create a simple icon with "M" letter and indigo background
    const svg = `
      <svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#6366f1" rx="${size * 0.2}"/>
        <text
          x="50%"
          y="55%"
          font-family="system-ui, -apple-system, sans-serif"
          font-size="${size * 0.55}"
          font-weight="bold"
          fill="white"
          text-anchor="middle"
          dominant-baseline="middle"
        >M</text>
      </svg>
    `;

    await sharp(Buffer.from(svg))
      .png()
      .toFile(path.join(iconsDir, `icon-${size}.png`));

    console.log(`Created icon-${size}.png`);
  }

  // Also create apple-touch-icon
  const appleSvg = `
    <svg width="180" height="180" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#6366f1"/>
      <text
        x="50%"
        y="55%"
        font-family="system-ui, -apple-system, sans-serif"
        font-size="99"
        font-weight="bold"
        fill="white"
        text-anchor="middle"
        dominant-baseline="middle"
      >M</text>
    </svg>
  `;

  await sharp(Buffer.from(appleSvg))
    .png()
    .toFile(path.join(iconsDir, 'apple-touch-icon.png'));

  console.log('Created apple-touch-icon.png');
}

generateIcons().catch(console.error);
