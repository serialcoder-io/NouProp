function initQuill() {
    const editor = document.querySelector("#editor");
    if (!editor || editor.classList.contains("quill-ready")) return;

    new Quill("#editor", {
        theme: "snow",
        placeholder: "Your message here"
    });

    editor.classList.add("quill-ready");
}

document.addEventListener("DOMContentLoaded", initQuill);
document.addEventListener("click", function () {
    setTimeout(initQuill, 100);
});