# ffmpeg -r 1/5 -i img%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4

ffmpeg -framerate 1 -pattern_type glob -i '/Users/macbook/github/AmazonScraper/products/B07P978C2R/review_images/image1.jpg' -i '/Users/macbook/github/AmazonScraper/products/B07P978C2R/review_images/image2.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
