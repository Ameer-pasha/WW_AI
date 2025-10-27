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
document.getElementById("linkedinWorkForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // ✅ Just show Coming Soon message
    alert("🚀 LinkedIn Automation Coming Soon!");

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
