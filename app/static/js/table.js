function count_rows() {
  return document.querySelectorAll('tr:not([style*="display:none"]):not([style*="display: none"])').length;
}

document.querySelectorAll("tbody tr").forEach(function(elem) {
  elem.addEventListener("click", function() {
    elem.classList.toggle('active');
  });
});