(() => {
    "use strict";
    let squeaks = 0;
    document.body.onmousedown = (ev) => {
        if (ev.target.tagName == "A") {
            return true;
        }

        squeaks += 1;
        const element = document.createElement("div");
        element.className = "click-doodad";
        if (squeaks > 3) {
            const extraSqueaks = squeaks - 3;
            element.innerText = "squ" + "~".repeat(extraSqueaks) + "💜".repeat(extraSqueaks) + "~".repeat(extraSqueaks) + "ak";
        } else {
            element.innerText = "sque" + "e".repeat(Math.random() * 5) + "ak!" + "!".repeat(Math.random() * 4)
        }
        element.style.left = `calc(${ev.clientX}px - 1.5em)`
        element.style.top = `calc(${ev.clientY}px - 0.5em)`
        document.body.appendChild(element);
        setTimeout(() => {
            document.body.removeChild(element);
            squeaks -= 1;
        }, 1000)
        setTimeout(() => {
            element.style.transform = 'translateY(-50px)';
            element.style.opacity = "0";
        }, 1)
    }
})();
