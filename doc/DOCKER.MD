# Build
sudo docker build -t panda0196/salesforce-poc .

# Run
sudo docker run -p 4444:4444 -e SALES_CLIENT_KEY="XXX" -e SALES_CLIENT_SECRET="XXX" panda0196/salesforce-poc