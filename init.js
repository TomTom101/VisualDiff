var i = 0;

function scroll() {
    i += 100;
    if (i > document.height) {
        window.scrollTo(0, 0);
        webkit2png.start();
    } else {
        window.scrollTo(0, i);
        window.setTimeout(scroll, 500)
    }
};
webkit2png.stop();
scroll();
