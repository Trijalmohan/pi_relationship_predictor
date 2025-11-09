const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");

let stars = [];
const starCount = 180;

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

for (let i = 0; i < starCount; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.2,
        dx: (Math.random() - 0.5) * 0.1
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";

    stars.forEach(s => {
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();

        s.x += s.dx;
        if (s.x < 0) s.x = canvas.width;
        if (s.x > canvas.width) s.x = 0;
    });

    requestAnimationFrame(draw);
}

draw();
