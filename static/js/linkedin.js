// ========== LinkedIn Modal Logic ==========
const linkedinModal = document.getElementById('linkedinModal');

function openLinkedInModal(event) {
    event.preventDefault();
    linkedinModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeLinkedInModal() {
    linkedinModal.style.display = 'none';
    document.body.style.overflow = '';
}

// ========== Form Submission ==========
document.getElementById("linkedinWorkForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const title = document.getElementById("workTitle").value;
    const description = document.getElementById("workDescription").value;

    try {
        const response = await fetch("/submit-work", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title, description })
        });

        const result = await response.json();

        if (result.status === "success") {
            alert("✅ " + result.message);
        } else {
            alert("❌ " + result.message);
        }

    } catch (error) {
        alert("⚠️ Error while posting. Please try again.");
        console.error(error);
    }

    // Reset and close modal
    document.getElementById("linkedinWorkForm").reset();
    closeLinkedInModal();
});

// ========== Click outside to close ==========
window.addEventListener("click", function(event) {
    if (event.target === linkedinModal) {
        closeLinkedInModal();
    }
});
