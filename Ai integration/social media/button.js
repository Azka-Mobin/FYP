function shareToTwitter() {
    let adText = document.getElementById('generatedAd').innerText;
    let twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(adText)}`;
    window.open(twitterUrl, '_blank');
}