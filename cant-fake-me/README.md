# CAN'T FAKE ME — Version 2

Built directly on the supplied three-file PWA prototype. This version adds a black/yellow scanner UI, photo-quality metrics, optional card labels, and local scan history.

## Run locally
From the `cant-fake-me` folder: `python3 -m http.server 8000`. Open `http://localhost:8000` on your computer. iPhone camera capture requires HTTPS when deployed.

## Deploy using GitHub Pages
1. Create a public GitHub repository.
2. Upload the files inside `cant-fake-me` to the repository root.
3. Go to Settings > Pages; select Deploy from a branch, main, /(root); save.
4. Open the HTTPS Pages URL in Safari on iPhone.
5. Tap Share > Add to Home Screen > Add.

## Important limitations
This app is NOT a card authenticity detector. Its measurements check resolution and approximate exposure/contrast, not card authenticity. It deliberately always returns INCONCLUSIVE. No image upload or AI service exists. History stores textual results, not photos, in localStorage, and can disappear if browser data is cleared.

## Next engineering milestone
Create a backend with a protected API key, card identification, licensed or otherwise authorized reference imagery, image alignment, visual anomaly checks, and an evidence-backed decision policy. Validate against a labeled genuine/counterfeit dataset before issuing Likely Real or Suspicious assessments. Do not put API keys in frontend HTML.
