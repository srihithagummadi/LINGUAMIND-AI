async function generateSummary() {

    let text = document.getElementById("inputText").value;
    let length = parseInt(document.getElementById("lengthSelect").value);

    if(text.trim() === ""){
        alert("Please enter some text!");
        return;
    }

    // Show original in compare view
    document.getElementById("originalText").innerText = text;

    // Dynamic summary based on selected length
    let words = text.split(" ");
    let summary = words.slice(0, length).join(" ") + "...";

    document.getElementById("summaryOutput").innerText = summary;
    document.getElementById("englishOutput").innerText = summary;

    // Translate to Hindi
    let hindi = await translateText(summary, "hi");
    document.getElementById("hindiOutput").innerText = hindi;

    // Translate to Telugu
    let telugu = await translateText(summary, "te");
    document.getElementById("teluguOutput").innerText = telugu;
}


async function translateText(text, targetLang) {
    let response = await fetch(
        `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`
    );
    let data = await response.json();
    return data[0][0][0];
}


// NEW: Download PDF
function downloadPDF() {

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    let original = document.getElementById("originalText").innerText;
    let summary = document.getElementById("summaryOutput").innerText;

    doc.text("LinguaMind AI Summary Report", 10, 10);
    doc.text("Original Text:", 10, 20);
    doc.text(original, 10, 30, { maxWidth: 180 });

    doc.text("Generated Summary:", 10, 70);
    doc.text(summary, 10, 80, { maxWidth: 180 });

    doc.save("LinguaMind_Summary.pdf");
}