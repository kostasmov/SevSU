photos = new Array(18);
path = "photos/";

for (var i = 0; i < 18; i++) {
    photos[i] = path + (i + 1) + ".webp";
}

document.write("<div style=\"display: grid; grid-template-columns: repeat(6, 1fr);\">");
for (var i = 0; i < 18; i += 6) {
    for (var j = i; j < i + 6; j++) {
        document.write("<figure>");
        document.write("<img src=\"" + photos[j] + "\" width=\"100%\" alt=\"Изображение\" title=\"Кермит\"");
        document.write("<figcaption>Подпись " + (j + 1) + "</figcaption>")
        document.write("</figure>");
    }
}
document.write("</div>");