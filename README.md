# How to run the frontend

# Change Chrome header to allow CORS
## Step 1 - Create a Chrome app shortcut in your Desktop.
## Step 2 - Right Click and click on "Properties".
## Step 3 - Copy the path below and Change the "Target" (Remember to set the correct path to Chrome.exe): 
## "[PATH_TO_CHROME]\chrome.exe" --disable-web-security --disable-gpu --user-data-dir=~/chromeTemp
## Step 4 - Apply changes.



# How to run React App
## Step 1 - Build the dependency
```bash
npm build
```

## Step 2 - Start the frontend
```bash
npm start
```

## Step 3 - Run on testing
```bash
npm test
```

## Step 4 - Build for Production
```bash
npm run build
```