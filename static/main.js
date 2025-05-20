document.getElementById('options').addEventListener('change', function() {
    const selectedOption = this.options[this.selectedIndex];
    const href = selectedOption.getAttribute('data-href');
    if (href) {
        window.location.href = href;
    }
});
