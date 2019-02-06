dom = {
    spooky : function() {
        const img = document.createElement("img");
        img.src = "https://i.imgur.com/oE5LmW6.jpg";
        img.className = "spooky";
        img.style.position = "absolute";
        img.style.top = "50%";
        img.style.left = "50%";
        img.style.transform = "translate(-50%,-50%)"
        document.body.style.position = "relative";
        document.body.appendChild(img);

        setInterval( function() {
            let spooky = $("img.spooky")
            let opacity = spooky.css("opacity");
            if (opacity == "1")
                spooky.css("opacity", "0")
            else
                spooky.css("opacity", "1")
        }, 100);
    }
}